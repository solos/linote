#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import local
import config
import encoding
import cPickle as pickle
import markdown
import lxml.html
import lxml.html.clean
from docutils.core import publish_parts
import evernote.edam.error.ttypes as Errors
import thrift.transport.THttpClient as THttpClient
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

__version__ = '0.0.1'

encoding_match = re.compile('encoding=[^>]+')


class Linote(object):

    def __init__(self, dev_token, note_store_url):
        self.dev_token = dev_token
        self.noteStoreUrl = note_store_url
        noteStoreHttpClient = THttpClient.THttpClient(self.noteStoreUrl)
        noteStoreProtocol = TBinaryProtocol(noteStoreHttpClient)
        self.noteStore = NoteStore.Client(noteStoreProtocol)
        self.style_cleaner = lxml.html.clean.Cleaner(
            safe_attrs_only=True,
            safe_attrs=set(['href', 'src', 'style', 'title', 'alt']))

        self.cleaner = lxml.html.clean.Cleaner(
            scripts=True,
            javascript=True,
            comments=True,
            style=True,
            links=True,
            meta=True,
            page_structure=True,
            processing_instructions=True,
            embedded=True,
            frames=True,
            forms=True,
            annoying_tags=True,
            remove_tags=None,
            allow_tags=None,
            kill_tags=None,
            remove_unknown_tags=True,
            safe_attrs_only=True,
            safe_attrs=frozenset(['abbr', 'accept', 'accept-charset']),
            add_nofollow=False,
            host_whitelist=(),
            whitelist_tags=set(['embed', 'iframe']),
            _tag_link_attrs={'a': 'href', 'applet': ['code', 'object']}
        )

    def getNotebooks(self):
        return self.noteStore.listNotebooks(self.dev_token)

    def getNotebookDir(self, notebook):
        if notebook.stack:
            parent_dir = notebook.stack
            subdir = '%s/%s' % (parent_dir, notebook.name)
            if not os.path.isdir(parent_dir):
                os.mkdir(parent_dir)
            if not os.path.isdir(subdir):
                os.makedirs(subdir)
        else:
            subdir = notebook.name
            if not os.path.isdir(subdir):
                os.makedirs(subdir)
        return subdir

    def getNotes(self, notebook, limit=256):
        filter = NoteStore.NoteFilter()
        filter.notebookGuid = notebook.guid
        noteList = self.noteStore.findNotes(self.dev_token, filter, 0, limit)
        return noteList.notes

    def getContent(self, noteId):
        return self.noteStore.getNote(self.dev_token,
                                      noteId, True, False, False, False)

    def checkdir(self, notedir=None):
        if not notedir:
            notedir = config.notedir
        if not os.path.isdir(notedir):
            try:
                os.mkdir(notedir)
                return True
            except Exception, e:
                print e
                return False
        return True

    def chdir(self, notedir):
        try:
            os.chdir(notedir)
        except Exception, e:
            print e

    def format(self, note):
        _, content = encoding.html_to_unicode('', note.content)
        content = encoding_match.sub('', content)
        return content

    def clean(self, content):
        content = content.replace('<br>', '\n').replace('</br>', '\n')
        content = self.clean_note(content)
        return content.encode('utf8')

    def process(self, note, subdir):
        _id = note.guid
        _updated = note.updated / 1000
        try:
            local_updated = self.local_files[_id]['mtime']
        except KeyError:
            local_updated = 0
        if _updated < local_updated:
            return
        print note.guid, note.title
        ntitle = note.title.replace('/', '-')
        title = ntitle if len(ntitle) < 200 else ntitle[:200]

        if title.endswith('.md') or title.endswith('.rst'):
            suffix = title.split('.')[-1]
            filename = ('%s/%s-%s.%s' % (subdir, note.guid, title, suffix))
            note_item = self.getContent(note.guid)
            content = self.extract(note_item)
            open(filename, 'w').write(content)
        else:
            filename = ('%s/%s-%s.enml' % (subdir, note.guid, title))
            note_item = self.getContent(note.guid)
            content = self.clean(self.format(note_item))
            open(filename, 'w').write(content)

    def sync(self):
        self.local_files = local.gen_filelist()
        notebooks = self.getNotebooks()
        if not self.checkdir():
            print 'notedir not exist and failed to mkdir'
            return
        self.chdir(config.notedir)
        for notebook in notebooks:
            subdir = self.getNotebookDir(notebook)
            notes = self.getNotes(notebook)
            for note in notes:
                self.process(note, subdir)

    def check(self):
        try:
            print 'check'
            print self.noteStore.getSyncState(self.dev_token)
            return True
        except Errors.EDAMSystemException, e:
            print e
            if e.errorCode == Errors.EDAMErrorCode.RATE_LIMIT_REACHED:
                print "Rate limit reached, Retry your request in %d seconds" \
                    % e.rateLimitDuration
                return False
            else:
                return True

    def make_note(self, note_title, note_content, notebookGuid=None):
        '''make note'''
        note = Types.Note()
        note.title = note_title
        note.content = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<!DOCTYPE en-note SYSTEM "http://xml.evernote.com/pub/enml2.dtd">'
            '<en-note> %s </en-note>' % note_content)
        if notebookGuid:
            note.notebookGuid = notebookGuid
        return note

    def create(self, note):
        '''create note'''
        return self.noteStore.createNote(self.dev_token, note)

    def delete(self):
        '''todo: delete'''
        pass

    def extract(self, note):
        content = self.format(note)
        tree = lxml.html.fromstring(content)
        source = ''
        try:
            code_element = tree.xpath('//div[@style="display:none"]')[0]
            source = lxml.html.tostring(code_element)
        except Exception, e:
            print e
        return source

    def search_filename(self, keywords):
        keywords = keywords.strip().lower().split(' ')
        lndir = '%s/.linote' % os.environ['HOME']
        cachefile = '%s/.caches' % lndir
        try:
            files = pickle.loads(open(cachefile).read())
        except Exception:
            files = local.gen_filelist()

        related = []
        for _id in files:
            fullname = files[_id]['file']
            filename = os.path.basename(fullname).lower()[37:]
            is_related = True
            for keyword in keywords:
                if keyword not in filename.lower():
                    is_related = False
                    break
            if is_related:
                print _id, fullname
                related.append((_id, fullname))
        return related

    def search_content(self, keywords):
        keywords = keywords.strip().lower().split(' ')
        lndir = '%s/.linote' % os.environ['HOME']
        cachefile = '%s/.caches' % lndir
        try:
            files = pickle.loads(open(cachefile).read())
        except Exception:
            files = local.gen_filelist()

        related = []
        for _id in files:
            fullname = files[_id]['file']
            #filename = os.path.basename(fullname).lower()[37:]
            try:
                content = open(fullname, 'r').read()
            except:
                continue
            is_related = True
            for keyword in keywords:
                if keyword not in content:
                    is_related = False
                    break
            if is_related:
                print _id, fullname
                related.append((_id, fullname))
        return related

    def clean_note(self, content):
        cleaned = self.cleaner.clean_html(content)
        raw_text = lxml.html.fromstring(cleaned).text_content()
        return raw_text

    def clean_style(self, content):
        cleaned = self.style_cleaner.clean_html(content)
        return cleaned

    def make_mdnote(self, md_source):
        source_segment = '''<div style="display:none">%s</div>''' % md_source
        html = markdown.markdown(md_source)
        note = '%s\n%s' % (html, source_segment)
        return self.clean_style(note)

    def make_rstnote(self, rst_source):
        source_segment = '''<div style="display:none">%s</div>''' % rst_source
        html = publish_parts(rst_source, writer_name='html')['html_body']
        note = '%s\n%s' % (html, source_segment)
        return self.clean_style(note)

if __name__ == '__main__':
    ln = Linote(config.dev_token, config.noteStoreUrl)
    #ln.sync()
    related = ln.search_filename('pylons authkit')
    related = ln.search_content('pylons authkit')
    note_title = 'test'
    note_content = 'content test'
    note = ln.make_note(note_title, note_content)
    ln.create(note)
