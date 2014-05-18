[![Build Status](https://travis-ci.org/solos/linote.png?branch=master)](https://travis-ci.org/solos/linote)
[![Downloads](https://pypip.in/d/linote/badge.png)](https://pypi.python.org/pypi/linote)
# linote

#About

A command line evernote for linux (Under development).

##Getting Started (Easy Way)

1. Get it from pypi `pip install linote`. This will get you the latest stable version

##Getting Started (Hard Way - AKA to get latest and greatest version)

0. `git clone https://github.com/solos/linote.git && cd linote`
1. Run `python install -r requirements.txt`
2. Upon success run `python setup.py install` in source folder
3. Run `python linote.py` to start syncing. If your `~/.linote/config.ini` does not exist it will be copied from config.ini.sample.
4. Edit the defaults in `~/.linote/config.ini` to show correct parameters. 

## About config developer and noteStore url

  - If you use evernote, please visit https://www.evernote.com/api/DeveloperToken.action to generate a developer token and noteStore url.
  - If you use yinxiang, please visit https://app.yinxiang.com/api/DeveloperToken.action instead.
  - After you got the developer token and noteStore url, please replace the settings in config.py.sample.
    - `mkdir ~/.linote && touch ~/.linote/__init__.py`  
    - modify developer token and noteStore url in the config.py.sample file.
    - `cp config.py.sample ~/.linote/config.py`  # need change to use other config files
