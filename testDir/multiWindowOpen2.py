# -*- coding: utf-8 -*- 
# Form implementation generated from reading ui file 'window_process.ui'
#
# Created: Mon Jun 11 15:20:34 2012
#      by: PyQt4 UI code generator 4.7.2
#
# WARNING! All changes made in this file will be lost!
 
from PyQt4 import QtCore, QtGui


class sub_window(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(363, 188)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(22, 120, 121, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(240, 120, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(140, 50, 141, 31))
        self.label.setObjectName("label")
 
        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), Form.close)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.dosumfuction)
        QtCore.QMetaObject.connectSlotsByName(Form)
 
    def dosumfuction(self):
        print "Doing sum fuction"
        print "Function finished"
        print "But window did not close How to close sub window"
       
    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "subwindow", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Do sum function", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Form", "Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "subwindow", None, QtGui.QApplication.UnicodeUTF8))
 
 
class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(407, 258)
        self.pushButton = QtGui.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(40, 170, 131, 31))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtGui.QPushButton(Form)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 170, 93, 31))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(140, 60, 171, 51))
        self.label.setObjectName("label")
 
        self.retranslateUi(Form)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL("clicked()"), Form.close)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.opensubwindow)
        QtCore.QMetaObject.connectSlotsByName(Form)
   
    def opensubwindow(self):
        print "Subwindow starts"
        self.Form = QtGui.QWidget()
        self.sub_window1 = sub_window()
        self.sub_window1.setupUi(self.Form)
        self.Form.show()
       
    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("Form", "Open New Window", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_2.setText(QtGui.QApplication.translate("Form", "close", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Main Window", None, QtGui.QApplication.UnicodeUTF8))
 
 
if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

