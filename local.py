#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import stat
import cPickle as pickle
from pathlib import *

local_files = {}

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))


def gen_filelist():
    walktree(Path(PROJECT_ROOT).join('notes'), statfile)
    files = pickle.dumps(local_files)
    lndir = '%s/.linote' % os.environ['HOME']
    cachefile = '%s/.caches' % lndir
    try:
        Path(lndir).mkdir(parents=True)
    except OSError:
        if not Path(lndir).exists():
            raise
    Path(cachefile).open('w').write(unicode(files))
    return local_files


def walktree(dirname, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for pathname in Path(dirname).iterdir():
        if Path(pathname).is_dir():
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif Path(pathname).is_file():
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname


def statfile(file):
    #filename = os.path.basename(file)
    filename = Path(file).parts[-1]
    if not filename.endswith('.enml') or filename.count('-') < 4:
        return
    try:
        _id = '-'.join(filename.split('-')[:5])
    except Exception, e:
        print e
        return
    fstat = os.stat(file)
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
