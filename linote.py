#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Linote.

Usage:
  linote.py sync
  linote.py --version

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

import os
import sys
from path import path

PROJECT_ROOT = path(__file__).parent.abspath()
PROJECT_CONFIG = path(os.environ['HOME']).joinpath('.linote')
sys.path.append(PROJECT_ROOT)
sys.path.append(PROJECT_CONFIG)


import re
import time
import local
import config
import encoding
import cPickle as pickle
import markdown
import lxml.html
import lxml.html.clean
from docopt import docopt
from logger import logger
from docutils.core import publish_parts
import evernote.edam.error.ttypes as Errors
import evernote.edam.notestore.NoteStore as NoteStore
import evernote.edam.type.ttypes as Types
from evernote.edam.notestore import ttypes as ttypes
import thrift.transport.THttpClient as THttpClient
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

__version__ = '0.0.1'

encoding_match = re.compile('encoding=[^>]+')


def check_rate_limit(func):
    def wrapper(self, *args, **kwargs):
        try:
            self.noteStore.getSyncState(self.dev_token)
            return func(self, *args, **kwargs)
        except Errors.EDAMSystemException, e:
            if e.errorCode == Errors.EDAMErrorCode.RATE_LIMIT_REACHED:
                logger.info("Rate limit reached, Retry your request in %d "
                            "seconds" % e.rateLimitDuration)
            logger.info('sleep %s' % e.rateLimitDuration)
            time.sleep(int(e.rateLimitDuration) + 10)
        except Exception, e:
            logger.error(e)
    return wrapper


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

        lndir = '%s/.linote' % os.environ['HOME']
        self.notedir = config.linote_config.get('linote.notedir')
        self.cachefile = '%s/.caches' % lndir

    @check_rate_limit
    def getNotebooks(self):
        return self.noteStore.listNotebooks(self.dev_token)

    @check_rate_limit
    def getNotebookDir(self, notebook):
        if not isinstance(notebook.stack, unicode):
            notebook.stack = notebook.stack.decode('utf8')
        if not isinstance(notebook.name, unicode):
            notebook.name = notebook.name.decode('utf8')
        if notebook.stack:
            parent_dir = path(self.notedir).joinpath(notebook.stack)
            subdir = path(PROJECT_ROOT).joinpath(
                parent_dir).joinpath(notebook.name)

            for fpath in (parent_dir, subdir):
                path(fpath).mkdir_p()
        else:
            subdir = notebook.name
            path(subdir).mkdir_p()
        return subdir

    @check_rate_limit
    def getNotes(self, notebook, limit=512):
        filter = NoteStore.NoteFilter()
        filter.notebookGuid = notebook.guid
        noteList = self.noteStore.findNotes(self.dev_token, filter, 0, limit)
        return noteList.notes

    @check_rate_limit
    def getContent(self, noteId):
        return self.noteStore.getNote(self.dev_token,
                                      noteId, True, False, False, False)

    def checkdir(self, notedir=None):
        notedir = notedir or self.notedir
        if not path(notedir).isdir():
            try:
                path(notedir).mkdir_p()
                return True
            except Exception, e:
                logger.error(e)
                return False
        return True

    def chdir(self, notedir):
        try:
            path(notedir).chdir()
        except Exception, e:
            logger.error(e)

    def format(self, note):
        content = ''
        if note is not None:
            _, content = encoding.html_to_unicode('', note.content)
            content = encoding_match.sub('', content)
        return content

    def clean_note(self, content):
        cleaned = self.cleaner.clean_html(content)
        raw_text = lxml.html.fromstring(cleaned).text_content()
        return raw_text

    def clean_style(self, content):
        cleaned = self.style_cleaner.clean_html(content)
        return cleaned

    def clean(self, content):
        content = content.replace('<br>', '\n').replace('</br>', '\n')
        content = self.clean_note(content)
        return content.encode('utf8')

    def getFilteredSyncChunk(self, afterUSN, maxEntries=256):
        filter = ttypes.SyncChunkFilter(includeNotes=True)
        return self.noteStore.getFilteredSyncChunk(
            self.dev_token, afterUSN, maxEntries, filter)

    def need_to_sync(self, note):
        _updated = note.updated / 1000
        try:
            local_updated = self.local_files[note.guid]['mtime']
        except KeyError:
            local_updated = 0
        if _updated <= local_updated:
            return False
        else:
            return True

    @check_rate_limit
    def process(self, note, subdir):
        print 'updateSequenceNum', note.updateSequenceNum
        logger.info('sync %s %s' % (note.guid, note.title))
        ntitle = note.title.replace('/', '-')
        title = ntitle if len(ntitle) < 200 else ntitle[:200]

        if title.endswith('.md') or title.endswith('.rst'):
            suffix = title.split('.')[-1]
            filename = ('%s/%s-%s.%s' % (subdir, note.guid, title, suffix))
            note_item = self.getContent(note.guid)
            content = self.extract(note_item)
        else:
            filename = ('%s/%s-%s.enml' %
                        (subdir.encode('utf8'),
                         note.guid,
                         title))
            note_item = self.getContent(note.guid)
            content = self.clean(self.format(note_item))

        if not isinstance(filename, unicode):
            filename = filename.decode('utf8')
        path(filename).open("w").write(content)

    def sync(self):
        self.local_files = local.gen_filelist(self.notedir)
        notebooks = self.getNotebooks()
        if not notebooks:
            return
        if not self.checkdir():
            logger.error('notedir not exist and failed to mkdir')
            return
        self.chdir(config.linote_config.get('linote.notedir'))
        for notebook in notebooks:
            subdir = self.getNotebookDir(notebook)
            notes = self.getNotes(notebook)
            if not notes:
                return
            for note in notes:
                if self.need_to_sync(note):
                    self.process(note, subdir)

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
            logger.error(e)
        return source

    def search_filename(self, keywords):
        keywords = keywords.strip().lower().split(' ')
        try:
            files = pickle.loads(
                open(self.cachefile).read())
        except Exception:
            files = local.gen_filelist(self.notedir)

        related = []
        for _id in files:
            fullname = files[_id]['file']
            filename = path(fullname).basename().lower()[37:]
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
        try:
            files = pickle.loads(
                path(self.cachefile).open().read())
        except Exception:
            files = local.gen_filelist()

        related = []
        for _id in files:
            fullname = files[_id]['file']
            try:
                content = path(fullname).open().read()
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


def run():
    ln = Linote(config.linote_config.get('linote.dev_token'),
                config.linote_config.get('linote.notestoreurl'))
    arguments = docopt(__doc__, version=__version__)
    if arguments['sync']:
        ln.sync()


if __name__ == '__main__':
    run()
