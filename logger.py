#!/usr/bin/python
#coding=utf-8

import config
import logging
from logging.handlers import TimedRotatingFileHandler
from path import path

#loggerName = config.LOG_NAME
loggerName = config.linote_config.get('logging.log_name')
#basic_log_path = config.BASIC_LOG_PATH
basic_log_path = config.linote_config.get('logging.basic_log_path')
filename = config.linote_config.get('logging.log_filename')
#filename = config.LOG_FILENAME

extname = path(filename).ext or 'log'
logfile = '%s/%s.%s' % (basic_log_path,
                        path(filename).splitext()[0],
                        extname)

path(basic_log_path).mkdir_p()

formatter = logging.Formatter(
    '%(asctime)s %(levelname)s %(filename)s %(message)s')

fileTimeHandler = TimedRotatingFileHandler(logfile, "D", 1)
fileTimeHandler.suffix = "%Y%m%d.log"
fileTimeHandler.setFormatter(formatter)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(loggerName)
logger.addHandler(fileTimeHandler)
logger.propagate = False
