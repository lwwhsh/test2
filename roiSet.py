# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from roi_ui import Ui_roiWidget
import epics
import sqlite3
from threadScanData import ThreadScanData

e0Name     = 'mobiis:m2'
BEAM       = 'G:BEAMCURRENT'
COUNT_NAME = 'HFXAFS:scaler1'


class RoiWidget(QtGui.QWidget):
    def __init__(self, parent = None):
        super(RoiWidget, self).__init__(parent) # __init__(parent) for send signal to main

        # GUI construction
        self.ui = Ui_roiWidget()
        self.ui.setupUi(self)

        # define signal for GUI user operation----------------------------------------
        self.makeElementList()
        self.connect(self.ui.elements, SIGNAL("currentIndexChanged(int)"),
                     self.onEdgeChoice)
        self.connect(self.ui.doubleE0, SIGNAL("valueChanged(double)"),
                     self.updateElementList)
        self.connect(self.ui.btnE0, SIGNAL("clicked()"),
                     self.moveE0)
        self.connect(self.ui.btnStartScan, SIGNAL("clicked()"),
                     self.startScan)
        self.connect(self.ui.btnStopScan, SIGNAL("clicked()"),
                     self.stopScan)

        # region calculation----------------------------------------------------------
        self.reg_settings = []
        self.reg_settings.append(
            (self.ui.doublePre1Start,  self.ui.doublePre1Stop,
             self.ui.doublePre1Step,   self.ui.doublePre1Time,
             self.ui.labelPre1Units))
        self.reg_settings.append(
            (self.ui.doublePre2Start,  self.ui.doublePre2Stop,
             self.ui.doublePre2Step,   self.ui.doublePre2Time,
             self.ui.labelPre2Units))
        self.reg_settings.append(
            (self.ui.doubleXANESStart, self.ui.doubleXANESStop,
             self.ui.doubleXANESStep,  self.ui.doubleXANESTime,
             self.ui.labelXANESUnits))
        self.reg_settings.append(
            (self.ui.doubleXAFS1Start, self.ui.doubleXAFS1Stop,
             self.ui.doubleXAFS1Step,  self.ui.doubleXAFS1Time,
             self.ui.XAFS1Units))
        self.reg_settings.append(
            (self.ui.doubleXAFS2Start, self.ui.doubleXAFS2Stop,
             self.ui.doubleXAFS2Step,  self.ui.doubleXAFS2Time,
             self.ui.XAFS2Units))
        self.reg_settings.append(
            (self.ui.doubleXAFS3Start, self.ui.doubleXAFS3Stop,
             self.ui.doubleXAFS3Step,  self.ui.doubleXAFS3Time,
             self.ui.XAFS3Units))

        # Setup default ROI index(XAFS2)----------------------------------------------
        self.ui.selectRegion.currentIndexChanged.connect(self.regionChanged)
        self.regionChanged(self.ui.selectRegion.currentIndex())

        # Setup current energy to E0 value--------------------------------------------
        try:
            self.ui.doubleE0.setValue(epics.caget(e0Name+'.RBV', timeout=10))
        except:
            pass

        self.updateElementList()

        self.ui.progressBar.setValue(0.0)

        # Try connect to SCAN SERVER!
        try:
            self.scan_handle = ThreadScanData()

        except Exception as e:
            print e
            QMessageBox.warning(self, "Oops SCAN server",
                                " Scan server not connected please restart this program ",
                                QMessageBox.Ok)

        self.scan_handle.commSignal.connect(self.showData)

    def makeElementList(self):
        con = sqlite3.connect("xrayref.db")
        cursor = con.cursor()
        cursor.execute("SELECT element FROM xray_levels WHERE iupac_symbol='K'")
        elementName = cursor.fetchall()
        cursor.close()
        con.close()

        for i, in elementName:
            self.ui.elements.addItem(i)

    def onEdgeChoice(self, evt=None):
        con = sqlite3.connect('xrayref.db')
        cursor = con.cursor()
        sqlStr = "SELECT absorption_edge FROM xray_levels WHERE element='%s' AND iupac_symbol='K'" %(self.ui.elements.itemText(evt))
        cursor.execute(sqlStr)
        e0val = cursor.fetchall()
        cursor.close()
        con.close()

        a = e0val.pop(0)
        self.ui.doubleE0.setValue(float(a[0]))

    def updateElementList(self, evt=7112.0):
        con = sqlite3.connect("xrayref.db")
        cursor = con.cursor()
        try:
            sqlStr = "SELECT element FROM xray_levels WHERE absorption_edge='%s' AND iupac_symbol='K'" \
                     %(self.ui.doubleE0.value())
            cursor.execute(sqlStr)
            elementName = cursor.fetchall()

            a = elementName.pop(0)
            if isinstance(a[0], unicode):
                index = self.ui.elements.findText(a[0])
                if index is not -1:
                    self.ui.elements.setCurrentIndex(index)
        except:
            pass
        finally:
            cursor.close()
            con.close()

    def regionChanged(self, value):
        for r in self.reg_settings[:value+2]:
            for i, a in enumerate(r):
                a.setEnabled(True)

        for r in self.reg_settings[value+2:]:
            for i, a in enumerate(r):
                a.setEnabled(False)

    def startScan(self):
        try:
            self.scan_handle.putTable(self.ui.doubleE0,
                                      self.reg_settings,
                                      self.ui.selectRegion)
        except Exception as e:
            print e

        self.scan_handle.set_conf(e0=self.ui.doubleE0.value())

        # if is not scanning. start new scan.
        if self.scan_handle.state is False:
            self.scan_handle.resume()
            self.scan_handle.start()

    def stopScan(self):
        try:
            self.scan_handle.stop()
        except Exception as e:
            print e

    def moveE0(self):
        quit_msg = """Are you sure you want move to e0?
                   You need energy calibration after move e0!!"""
        reply = QtGui.QMessageBox.question(self, 'Move e0 Message',
                         quit_msg, QtGui.QMessageBox.Yes, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            try:
                epics.caput(e0Name, self.ui.doubleE0.value(), wait=False)
            except Exception as e:
                print e
        else:
            pass

    def showData(self, data):
        self.ui.progressBar.setValue(data)


# this module run
if '__main__' == __name__:
    application = QtGui.QApplication(sys.argv)
    test = RoiWidget()
    test.show()
    sys.exit(application.exec_())

# 우리나라 대한민국