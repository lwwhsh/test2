# -*- coding: utf-8 -*-
import time
import numpy as np
from PyQt4 import QtCore
import epics
from pvHandler import MakePointForScan


class ThreadScanData(QtCore.QThread, MakePointForScan):
    commSignal = QtCore.pyqtSignal(int)

    ## def __init__(self, send_signal):
    def __init__(self):
        super(ThreadScanData, self).__init__()

        MakePointForScan.__init__(self)

        # 변수 초기화
        self.state = False

    def __del__(self):
        self.state = False

    def set_conf(self, e0=7112.0):
        self.e0 = e0

    def send_data(self):
        """ 입력받은 데이터가 없을 때 """
        if not self.scan_id:
            return

        if __package__ is None:
            print self.scan_id
        else:
            return

    def stop(self):
        self.client.abort()
        self.state = False

    def resume(self):
        self.status = True

    def is_running(self):
        return self.state

    def run(self):
        self.state = True
        self.last_log_fetched = None
        self.last_logged = None

        while not self.client.scanInfo(self.scan_id).isDone():
            if self.state is False:
                break

            self.last_logged = self.client.lastSerial(self.scan_id)

            if self.last_log_fetched != self.last_logged:
                self.last_log_fetched = self.last_logged
                self.commSignal.emit(self.client.scanInfo(self.scan_id).percentage())

            time.sleep(0.1)

        try:
            self.commSignal.emit(self.client.scanInfo(self.scan_id).percentage())
        except:
            pass

        # stop and return to e0.
        epics.caput('mobiis:m2.STOP', 1.0)
        time.sleep(1.0)
        epics.caput('mobiis:m2.VAL', self.e0, wait=True, timeout=120)

        #print self.client.getData(self.scan_id)
        # self.scan_handler.clear()
