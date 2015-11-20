import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class SubWindow(QWidget):
    def __init__(self, parent = None):
        super(SubWindow, self).__init__(parent)
        label = QLabel("Sub Window",  self)
    
    def closeEvent(self, event):
        self.deleteLater()
        event.accept()


class MainWindow(QWidget):
    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        openButton = QPushButton("Open Sub Window",  self)
        self.connect(openButton, SIGNAL("clicked()"), self.openSub)
    
    def openSub(self):
        self.sub = SubWindow()
        self.sub.show()
    
    def closeEvent(self, event):
        widgetList = QApplication.topLevelWidgets()
        numWindows = len(widgetList)
        if numWindows > 1:
            event.ignore()
        else:
            event.accept()

app = QApplication(sys.argv)
mainWin =MainWindow()
mainWin.show()
sys.exit(app.exec_())
