# linote

#About

A command line evernote for linux (Under development).

##Getting Started (Hard Way)

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
