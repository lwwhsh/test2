# -*- conding: utf-8 -*-
import sys
from PyQt4 import QtGui, QtCore
from ui import Ui_monitorWidget
from epics import PV
import epics

beampv  = 'G:BEAMCURRENT'
m1pospv = 'mobiis:m1'
m2pospv = 'mobiis:m2'
cntpv   = 'HFXAFS:scaler1'

class monitorWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(monitorWidget, self).__init__(parent) # __init__(parent) for main

        self.cntName = cntpv
        
        # GUI construction
        self.ui = Ui_monitorWidget()
        self.ui.setupUi(self)
        
        # SR beamcurrent & motor position monitor...
        self.beamPV =  PV(beampv)
        self.m1PosPV = PV(m1pospv+'.RBV')
        self.m2PosPV = PV(m2pospv+'.RBV')
        
        self.beamPV.add_callback(self.beamCallbackFunc)
        self.m1PosPV.add_callback(self.m1CallbackFunc)
        self.m2PosPV.add_callback(self.m2CallbackFunc)
        
        # for counter...
        self.countPV = PV(self.cntName+'_calc2')
        scalerAttrs = ('calc1','calc2','calc3','calc4',
                       'calc5','calc6','calc7','calc8')
        self.scalerDev = epics.Device(prefix=self.cntName+'_', delim='',
                                      attrs=scalerAttrs, mutable=False)
        epics.poll()
        
        try:
            epics.poll(0.001, 1.0)
            val = self.scalerDev.get_all()
            self.ui.IoCnt.display(val['calc2'])
            self.ui.ItCnt.display(val['calc3'])
            self.ui.IfCnt.display(val['calc4'])
            self.ui.IrCnt.display(val['calc5'])
        except: pass
        
        self.countPV.add_callback(self.countersCallbackFunc, run_now=True)
        
    def beamCallbackFunc(self, pvname=None, value=None, **kw):
        self.ui.beamCurrent.display(round(value, 2))

    def m1CallbackFunc(self, pvname=None, value=None, **kw):
        self.ui.M1Pos.display(round(value, 2))

    def m2CallbackFunc(self, pvname=None, value=None, **kw):
        self.ui.M2Pos.display(round(value, 2))

    def countersCallbackFunc(self, value=None, **kw):
        epics.poll()
        val = self.scalerDev.get_all()
        self.ui.IoCnt.display(value)
        self.ui.ItCnt.display(val['calc3'])
        self.ui.IfCnt.display(val['calc4'])
        self.ui.IrCnt.display(val['calc5'])
        
        
# this module run
if '__main__' == __name__:
    application = QtGui.QApplication(sys.argv)
    test = monitorWidget()
    test.show()
    
    sys.exit(application.exec_())

