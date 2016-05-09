#!/usr/bin/python2.7

# -*- coding: UTF-8 -*-

import traceback
import os, sys
# sys.path.append("python_package/xlrd/lib/python")
# sys.path.append("python_package/xlwt/lib")



# # for thrift
# 
# import sys, glob
# sys.path.append('gen-py')


# for thread
import thread
import time

# for log
from  log_config import *



class TestThriftServer:
    #def __init__(self, ip_add, port, md_gui):
    def __init__(self, ip_add, port):
        self.ip = ip_add
        self.port = port

    def Ping(self):
        try:
            ret_error="test ping"
            #ret_error = self.client.Ping("python")
            log.info('Ping(), return:{}'.format(ret_error))
        except Exception:
            log.info(('Get Exception Ping()%s'))

    def PingThread(self):
        while 1:
            log.info('"test from py thread"')
            time.sleep(2)


    def Start(self):
        # Create two threads as follows
        try:
            thread.start_new_thread( self.PingThread, () )
        except:
            log.info ("Error: unable to start thread")




if __name__ == "__main__":
    try:
        values = ['192.168.2.104', 39001]
        thrift_client = TestThriftServer(*values)
        thrift_client.Start()

        while 1:
            time.sleep(5)
            log.info("main heart beat...")
    except Exception:
        log.error("Got exception on TestThriftServer:%s", traceback.format_exc() )

    raw_input("press Enter to exit")

