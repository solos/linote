#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import stat

local_files = {}


def gen_filelist():
    walktree('notes', statfile)
    return local_files


def walktree(dirname, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(dirname):
        pathname = os.path.join(dirname, f)
        mode = os.stat(pathname).st_mode
        if stat.S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif stat.S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname


def statfile(file):
    filename = os.path.basename(file)
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
    print filelist
