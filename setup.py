#!/usr/bin/env python
#coding=utf-8

from distutils.core import setup
from linote import __version__

setup(name='linote',
      version=__version__,
      description='A command line evernote for linux.',
      long_description=open('README.md').read(),
      author='solos',
      author_email='solos@solos.so',
      py_modules=['linote'],
      scripts=['linote.py', 'local.py', 'encoding.py'],
      license='MIT',
      platforms=['any'],
      url='https://github.com/solos/linote')
#packages=['distutils', 'distutils.command']
