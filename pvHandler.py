#-*- coding: utf-8 -*-
__author__ = 'root'

import sys, time
from PyQt4 import QtGui, QtCore
import epics
from scan import *
# from ui import Ui_Form


class threadScanData(QtCore.QThread):
    # def __init__(self, send_signal):
    def __init__(self):
        super(threadScanData, self).__init__()
        self.scan_handler = None
        #self.send_signal = send_signal

        # 변수 초기화
        self.state = False
        self.scan_id = None
        self.interval = 1000
        self.location = 0

    def __del__(self):
        self.state = False

    def set_conf(self, scan_id, interval, scan_handler, location):
        self.scan_id = scan_id
        self.interval = interval
        self.scan_handler = scan_handler
        self.location = location

    def send_data(self):
        """ 입력받은 데이터가 없을 때 """
        if not self.scan_id:
            return

        if __package__ is None:
            print self.scan_id
        else:
            self.scan_handler.send_data(self.scan_id)
            #self.send_signal.emit(self.scan_id, self.location)
            print 'aa'

    def stop(self):
        self.state = False

    def is_running(self):
        return self.state

    def run(self):
        self.state = True

        self.last_log_fetched = None
        self.last_logged = None

        # while not self.client.scanInfo(self.scan_id).isDone():
        while not self.scan_handler.scanInfo(self.scan_id).isDone():
            if self.state is False:
                break

            # self.last_logged = self.client.lastSerial(self.scan_id)
            self.last_logged = self.scan_handler.lastSerial(self.scan_id)

            if self.last_log_fetched != self.last_logged:
                self.last_log_fetched = self.last_logged
                print '----- CHANGED----- %d' % (self.last_logged)

            time.sleep(0.025)

        print self.scan_handler.getData(self.scan_id)


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

        print 'CMDS : %s' % (self.cmds)

        self.id = self.client.submit(self.cmds, 'py')

        self.monThread = threadScanData()
        self.monThread.set_conf(self.id, 1.0, self.client, 1.0)
        self.monThread.start()

        print 'SCAN ID : %d' % (self.id)

    def monitorScans(self):
        self.last_log_fetched = None
        self.last_logged = None

        while not self.client.scanInfo(self.id).isDone():
            self.last_logged = self.client.lastSerial(self.id)

            if self.last_log_fetched != self.last_logged:
                self.last_log_fetched = self.last_logged

            time.sleep(1.0)


if __name__ == '__main__':
    runScan = MakePointoForScan()
    runScan.putTable()
    # for local test.
    runScan.monitorScans()
