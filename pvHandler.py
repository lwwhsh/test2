# -*- coding: utf-8 -*-

import time
import numpy as np
from scan import *


XAFS_K2E = 3.809980849311092

def etok(energy):
    return np.sqrt(energy/XAFS_K2E)

def ktoe(k):
    return k*k*XAFS_K2E


class MakePointForScan():
    def __init__(self):
        self.scan_id = None
        self.client = ScanClient('localhost', port=4810)

    def putTable(self, doubleE0, reg_setting, selectRegion):
        """
        Generate SCAN commands. see Kay kasemir documents(www.github.com)
        self.cmds = [ Comment("Example"),
                      Loop('m2', 0, 10, 1,
                            [ Set('cnt', 1),
                              Wait('cnt', 0, comparison='='),
                              Log(devices=['m2RBV', 'beam', 'io'])
                            ],
                      completion=True,
                      readback='m2RBV') ]
        """

        self.e0Ui = doubleE0
        self.region = reg_setting
        self.regionSelectUi = selectRegion
        self.e0Value = self.e0Ui.value()

        # TODO: Add User comments.
        cmds = [ Comment("Set") ]
        # count mode set to manual
        cmds.append(Set('cont', 0))

        for i in range(self.regionSelectUi.currentIndex()+2):
            li = list(self.region[i])

            # check k or eV and if eV step
            if i < 3 or (i > 2 and li[4].currentIndex() is 0):
                # 1st set expose time to scaler
                cmds.append(Set('tp', li[3].value()))

                dd1 = Loop('m2', li[0].value()+self.e0Value,
                           li[1].value()+self.e0Value-li[2].value(), li[2].value(),
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
                # delete last value
                ev_arr.pop()

                # 1st set expose time to scaler
                cmds.append(Set('tp', li[3].value()))

                for i in ev_arr:
                    cmds.append(Set('m2', i, completion=True, readback='m2RBV',
                                    tolerance=0.001))
                    cmds.append(Delay(0.01))
                    cmds.append(Set('cnt', 1))
                    cmds.append(Wait('cnt', 0))
                    cmds.append(Log(devices=['m2RBV', 'beam', 'io']))

        # count mode set to auto mode and DCM move to e0 angle
        cmds.append(Set('cont', 1))
        cmds.append(Set('m2', self.e0Value, completion=True, readback='m2RBV',
                        tolerance=0.001))

        # TODO: set file name to comment in the scan description.
        if self.state is False:
            self.scan_id = self.client.submit(cmds, 'py-START')
        else:
            self.client.submit(cmds, 'py-added')

    def monitorScans(self):
        self.last_log_fetched = None
        self.last_logged = None

        while not self.client.scanInfo(self.scan_id).isDone():
            self.last_logged = self.client.lastSerial(self.scan_id)

            if self.last_log_fetched != self.last_logged:
                self.last_log_fetched = self.last_logged

            time.sleep(1.0)


if __name__ == '__main__':
    runScan = MakePointForScan()
    runScan.putTable()
    # for local test.
    runScan.monitorScans()

# 우리나라 대한민국