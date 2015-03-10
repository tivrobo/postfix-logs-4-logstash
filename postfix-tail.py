#!/bin/python

__author__ = 'tiv'

import sys
import time
import re
from os import stat
from os.path import abspath
from stat import ST_SIZE

qdic = {}

class LogTail:
    def __init__(self, logfile):
        self.logfile = abspath(logfile)
        self.f = open(self.logfile,"r")
        file_len = stat(self.logfile)[ST_SIZE]
        self.f.seek(file_len)
        self.pos = self.f.tell()
    def _reset(self):
        self.f.close()
        self.f = open(self.logfile, "r")
        self.pos = self.f.tell()
    def tail(self):
        while 1:
            self.pos = self.f.tell()
            line = self.f.readline()
            if not line:
                if stat(self.logfile)[ST_SIZE] < self.pos:
                    self._reset()
                else:
                    time.sleep(0.1)
                    self.f.seek(self.pos)
            else:
                p = re.compile("^(.*)\/(.*)\[(.*)\]: ([0-9A-F]{10}): (.*)$")
                pline = p.search(line)
                if pline:
                    syslmsg = pline.group(1)
                    postcom = pline.group(2)
                    postpid = pline.group(3)
                    queueid = pline.group(4)
                    message = pline.group(5)
                    qdic.setdefault(queueid,[]).append(postcom.rstrip() + "=" + message.rstrip())
                    p = re.compile("^.*(removed|milter-reject).*$")
                    pline = p.match(message)
                    if pline is not None:
                        line = [queueid]
                        print ";".join(line + qdic[queueid])
                        del qdic[queueid]

objtail = LogTail("/var/log/maillog")
#objtail = LogTail("C:/Data/Temp/maillog.txt")
objtail.tail()