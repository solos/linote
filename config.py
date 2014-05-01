from path import path
from utils import get_config

dst = path('~/.linote/config.ini').expanduser()

if not dst.exists():
    dst.parent.makedirs_p()
    path('config.ini.sample').copy(dst)

linote_config = get_config(path('~/.linote/config.ini').expanduser())
