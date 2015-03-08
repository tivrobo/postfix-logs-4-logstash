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
                """print, return or otherwise manipulate
                the tailed line"""
                p = re.compile("([0-9A-F]{10})\:")
                qid = p.findall(line)
                if len(qid) >= 1:
                    queueid = qid[0]
                    qdic.setdefault(queueid,[]).append(line.rstrip())
                p = re.compile("([0-9A-F]{10})\: (?:removed|milter-reject)")
                qid = p.findall(line)
                if len(qid) >= 1:
                    queueid = qid[0]
                    pretty = ""
                    for i in qdic[queueid]:
                        pretty.join(i)
                    del qdic[queueid]


objtail = LogTail(str(sys.argv[1]))
objtail.tail()