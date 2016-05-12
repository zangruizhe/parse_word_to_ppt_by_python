#!/usr/local/bin/python2.7
# -*- coding: UTF-8 -*-
# create logger
#----------------------------------------------------------------------
import logging

log = logging.getLogger('python_logger')
log.setLevel(logging.DEBUG)

# create formatter and add it to the handlers
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# 2015-08-28 17:01:57,662 - simple_example - ERROR - error message

# formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(filename)s:%(lineno)-4d: %(message)s')
formatter = logging.Formatter('%(asctime)s %(levelname)-2s [%(filename)s: %(lineno)d] %(message)s')

#save log to file
fh = logging.FileHandler('log.txt', 'w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
log.addHandler(fh)

# send log to console
# create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(formatter)
# add the handlers to the logger
log.addHandler(ch)
#----------------------------------------------------------------------

log.debug("test debug log")
log.info("test info log")
log.warning("test warning log")
log.error("test error log")


