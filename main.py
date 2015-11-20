# -*- coding: utf-8 -*-

import sys, time
from PyQt4 import QtGui, QtCore
from main_ui import Ui_MainWindow
from monitorSet import monitorWidget
from roiSet import roiWidget


class mainForm(QtGui.QMainWindow):
    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.monWidget = monitorWidget(self.ui.widgetMonitor)
        self.roiWidget = roiWidget(self.ui.widgetROI)

    # 프로그램을 닫으려 할때
    def closeEvent(self, event):
        reply = QtGui.QMessageBox.warning(self,
            u'프로그램 종료', u"진행중인 모든 데이터 송·수신을 중지합니다.\n"
                        u"프로그램을 종료하시겠습니까?",
            QtGui.QMessageBox.Yes | QtGui.QMessageBox.No,
            QtGui.QMessageBox.No)
        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        elif reply == QtGui.QMessageBox.No:
            event.ignore()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = mainForm()
    myapp.show()
    sys.exit(app.exec_())
