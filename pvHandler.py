#-*- coding: utf-8 -*-
__author__ = 'root'

import sys, time
import numpy as np
from math import sqrt
from PyQt4 import QtGui, QtCore
import epics
from scan import *

XAFS_K2E = 3.809980849311092

def etok(energy):
    return np.sqrt(energy/XAFS_K2E)

def ktoe(k):
    return k*k*XAFS_K2E

class threadScanData(QtCore.QThread, MakePointForScan):
    commSignal = QtCore.pyqtSignal(int)

    def __init__(self, send_signal):
        ## super(threadScanData, self).__init__()
        super(serialReceiveThread, self).__init__(parent) # __init__(parent)가 아니면 메인에서 본 위젯의 시그널을 받을 수 없음.

        MakePointForScan.__init__(self)

        self.send_signal = send_signal
        self.scan_handler = None

        # 변수 초기화
        self.state = False
        self.scan_id = None
        self.interval = 1000
        self.location = 0

    def __del__(self):
        self.state = False

    def set_conf(self, scan_id, interval, scan_handler, location, e0=7112.0):
        self.scan_id = scan_id
        self.interval = interval
        self.scan_handler = scan_handler
        self.location = location
        self.e0 = e0

    def send_data(self):
        """ 입력받은 데이터가 없을 때 """
        if not self.scan_id:
            return

        if __package__ is None:
            print self.scan_id
        else:
            self.scan_handler.send_data(self.scan_id)

    def stop(self):
        self.state = False

    def is_running(self):
        return self.state

    def run(self):
        self.state = True
        self.last_log_fetched = None
        self.last_logged = None

        while not self.scan_handler.scanInfo(self.scan_id).isDone():
            if self.state is False:
                break

            self.last_logged = self.scan_handler.lastSerial(self.scan_id)

            if self.last_log_fetched != self.last_logged:
                self.last_log_fetched = self.last_logged
                self.send_signal.emit(self.scan_handler.scanInfo(self.scan_id).percentage())

            time.sleep(0.1)

        try:
            self.send_signal.emit(self.scan_handler.scanInfo(self.scan_id).percentage())
        except:
            pass

        # stop and return to e0.
        epics.caput('mobiis:m2.STOP', 1.0)
        time.sleep(1.0)
        epics.caput('mobiis:m2.VAL', self.e0, wait=True, timeout=120)

        # for test.
        self.stop()

        print self.scan_handler.getData(self.scan_id)
        # self.scan_handler.clear()

##class MakePointForScan(QtGui.QWidget):
class MakePointForScan():
    ## commSignal = QtCore.pyqtSignal(int)

    ## def __init__(self, parent):
    def __init__(self):
        ## super(MakePointForScan, self).__init__(parent) # __init__(parent)가 아니면 메인에서 본 위젯의 시그널을 받을 수 없음.

        self.id = None
        self.client = ScanClient('localhost', port=4810)

    def putTable(self, doubleE0, reg_setting, selectRegion):
        """
        Generate SCAN commands. see Kay kasemir documents(www.github.com)
        self.cmds = [ Comment("Example"),
                      Loop('m2', 0, 10, 1,
                            [ Set('cnt', 1),
                              Wait('cnt', 0, comparison='='),
                              Log(devices=['m2RBV', 'beam', 'io']) ],
                      completion=True,
                      readback='m2RBV') ]
        """

        self.e0Ui = doubleE0
        self.region = reg_setting
        self.regionSelectUi = selectRegion
        self.e0Value = self.e0Ui.value()

        # TODO: User comment.
        cmds = [ Comment("Set") ]

        for i in range(self.regionSelectUi.currentIndex()+2):
            li = list(self.region[i])

            # check k or eV and if eV step
            if i < 3 or (i > 2 and li[4].currentIndex() is 0):
                # 1st set expose time
                cmds.append(Set('tp', li[3].value()))

                dd1 = Loop('m2', li[0].value()+self.e0Value,
                           li[1].value()+self.e0Value, li[2].value(),
                           [ Delay(0.01),
                             Set('cnt', 1),
                             Wait('cnt', 0),
                             Log(devices=['m2RBV', 'beam', 'io'])
                           ],
                           completion=True, readback='m2RBV')

                cmds.append(dd1)

            # add k step. Matt Newvill equation!
            else:
                npts = 1 + int(0.1 + abs(etok(li[1].value()) - etok(li[0].value())) / li[2].value())
                en_arr = list(np.linspace(etok(li[0].value()), etok(li[1].value()), npts))

                # k to eV and add E0 Value
                ev_arr = [ self.e0Value + ktoe(e) for e in en_arr]

                # 1st set expose time
                cmds.append(Set('tp', li[3].value()))

                for i in ev_arr:
                    cmds.append(Set('m2', i, completion=True, readback='m2RBV', tolerance=0.0001))
                    cmds.append(Delay(0.01))
                    cmds.append(Set('cnt', 1))
                    cmds.append(Wait('cnt', 0))
                    cmds.append(Log(devices=['m2RBV', 'beam', 'io']))

        # set file name to comment in the scan description.
        self.id = self.client.submit(cmds, 'py')

        ##self.monThread = threadScanData(self.commSignal)
        ##self.monThread.set_conf(self.id, 1.0, self.client, 1.0, self.e0Value)
        ##self.monThread.start()

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
    runScan = MakePointForScan()
    runScan.putTable()
    # for local test.
    runScan.monitorScans()
