#-*- coding: utf-8 -*-
__author__ = 'root'

import epics
from scan import *
import sys, time

def monitorM3():
    while True:
        print epics.caget('mobiis:m3.RBV')
        time.sleep(1)
        print epics.caget('G:BEAMCURRENT')


class MakePointoForScan():
    def __init__(self):
        self.id = None

        self.client = ScanClient('localhost', port=4810)

        print self.client

    def putTable(self):
        self.cmds = [ Comment("Example"),
                      Loop('m2', 0, 10, 1,
                            [ Set('cnt', 1),
                              Wait('cnt', 0, comparison='='),
                              Log(devices=['m2RBV', 'beam', 'io']) ],
                      completion=True,
                      readback='m2RBV') ]

        print 'cmds', self.cmds

        self.id = self.client.submit(self.cmds, 'py')

        print 'id:', self.id

    def monitorScans(self):
        self.last_log_fetched = None
        self.last_logged = None

        while not self.client.scanInfo(self.id).isDone():
            self.last_logged = self.client.lastSerial(self.id)

            if self.last_log_fetched != self.last_logged:
                self.last_log_fetched = self.last_logged
                print '----- CHANGED-----'

            time.sleep(1)
            print '+++++ Not Changed +++'


if __name__ == '__main__':
    runScan = MakePointoForScan()
    runScan.putTable()
    time.sleep(1)
    runScan.monitorScans()
