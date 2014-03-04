#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import utils
import local
import config
import encoding
import cPickle as pickle
import evernote.edam.error.ttypes as Errors
import thrift.transport.THttpClient as THttpClient
import evernote.edam.notestore.NoteStore as NoteStore
from thrift.protocol.TBinaryProtocol import TBinaryProtocol

__version__ = '0.0.1'


class Linote(object):

    def __init__(self, dev_token, note_store_url):
        self.dev_token = dev_token
        self.noteStoreUrl = note_store_url
        noteStoreHttpClient = THttpClient.THttpClient(self.noteStoreUrl)
        noteStoreProtocol = TBinaryProtocol(noteStoreHttpClient)
        self.noteStore = NoteStore.Client(noteStoreProtocol)

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
        content = utils.encoding_match.sub('', content)
        content = content.replace('<br>', '\n').replace('</br>', '\n')
        content = utils.clean_note(content)
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
            #todo: extract source code and write file
            content = self.getContent(note.guid)
            open(filename, 'w').write(content)
        else:
            filename = ('%s/%s-%s.enml' % (subdir, note.guid, title))
            note_item = self.getContent(note.guid)
            #extract html and update note
            content = self.format(note_item)
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
            print 'hello'
            return True
        except Errors.EDAMSystemException, e:
            print e
            if e.errorCode == Errors.EDAMErrorCode.RATE_LIMIT_REACHED:
                print "Rate limit reached, Retry your request in %d seconds" \
                    % e.rateLimitDuration
                return False
            else:
                return True

    def create(self):
        '''todo: create'''
        pass

    def delete(self):
        '''todo: delete'''
        pass

    def search_filename(self, keywords):
        keywords = keywords.strip().lower().split(' ')
        lndir = '%s/.linote' % os.environ['HOME']
        cachefile = '%s/.caches' % lndir
        try:
            files = pickle.loads(open(cachefile).read())
        except Exception:
            files = local.gen_filelist()

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

    def search_content(self, keywords):
        pass

if __name__ == '__main__':
    ln = Linote(config.dev_token, config.noteStoreUrl)
    ln.sync()
    ln.search_filename('pylons authkit')
