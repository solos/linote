import kaptan
import sys
from path import path
from util import get_config

if not path('config.ini').exists():
    path('config.ini.sample').copy('~/.linote/config.ini')

linote_config = get_config(path('~/.linote/config.ini').expanduser())
