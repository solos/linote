# linote

#about

A command line evernote for linux (not finished yet).


## Config developer and noteStore url

  - If you use evernote, please visit https://www.evernote.com/api/DeveloperToken.action to generate a developer token and noteStore url.
  - If you use yinxiang, please visit https://app.yinxiang.com/api/DeveloperToken.action instead.
  - After you got the developer token and noteStore url, please replace the settings in config.py.sample.
    - `mkdir ~/.linote && touch ~/.linote/__init__.py`  
    - modify developer token and noteStore url in the config.py.sample file.
    - `cp config.py.sample ~/.linote/config.py`  # need change to use other config files
