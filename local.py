#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import stat
import cPickle as pickle
from path import path

local_files = {}

PROJECT_ROOT = path(__file__).dirname().abspath()


def gen_filelist():
    notes_path = path(PROJECT_ROOT).joinpath('notes')
    if path(notes_path).exists():
        for pathname in path(
                path(PROJECT_ROOT).joinpath('notes')).walkfiles():
            statfile(pathname)
    files = pickle.dumps(local_files)
    lndir = '%s/.linote' % os.environ['HOME']
    cachefile = '%s/.caches' % lndir
    path(lndir).mkdir_p()
    path(cachefile).open("w").write(unicode(files))
    return local_files


def statfile(file):
    filename = path(file).basename()
    if not filename.endswith('.enml') or filename.count('-') < 4:
        return
    try:
        _id = '-'.join(filename.split('-')[:5])
    except Exception, e:
        print e
        return
    fstat = path(file).stat()
    mtime = int(fstat.st_mtime)
    ctime = int(fstat.st_ctime)
    local_files[_id] = {
        'file': file,
        'mtime': mtime,
        'ctime': ctime
    }

if __name__ == '__main__':
    filelist = gen_filelist()
    for i in filelist:
        print filelist[i]['file']
