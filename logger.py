#!/usr/bin/python
#coding=utf-8

import config
import logging
import os
from logging.handlers import TimedRotatingFileHandler
from pathlib import *

loggerName = config.LOG_NAME
basic_log_path = config.BASIC_LOG_PATH
filename = config.LOG_FILENAME
if Path(filename).suffix == '':
    logfile = '%s/%s.log' % (basic_log_path, filename)
else:
    logfile = '%s/%s' % (basic_log_path, filename)

if not Path(basic_log_path).exists():
    Path(basic_log_path).mkdir(parents=True)

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

fileTimeHandler = TimedRotatingFileHandler(logfile, "D", 1)
fileTimeHandler.suffix = "%Y%m%d.log"
fileTimeHandler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(loggerName)
logger.addHandler(fileTimeHandler)
logger.propagate = False
