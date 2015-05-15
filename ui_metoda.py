# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'metoda.ui'
#
# Created: Mon Apr 13 00:40:32 2015
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(683, 577)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        #self.qwtPlot = QwtPlot(self.centralwidget)
        self.qwtPlot = Qwt5.QwtPlot(self.centralwidget)
        self.qwtPlot.setGeometry(QtCore.QRect(10, 10, 651, 371))
        self.qwtPlot.setObjectName(_fromUtf8("qwtPlot"))
        self.openFile = QtGui.QPushButton(self.centralwidget)
        self.openFile.setGeometry(QtCore.QRect(20, 390, 98, 27))
        self.openFile.setObjectName(_fromUtf8("openFile"))
        self.play = QtGui.QPushButton(self.centralwidget)
        self.play.setGeometry(QtCore.QRect(20, 420, 98, 27))
        self.play.setObjectName(_fromUtf8("play"))
        self.stop = QtGui.QPushButton(self.centralwidget)
        self.stop.setGeometry(QtCore.QRect(20, 450, 98, 27))
        self.stop.setObjectName(_fromUtf8("stop"))
        self.recorder = QtGui.QPushButton(self.centralwidget)
        self.recorder.setGeometry(QtCore.QRect(20, 490, 98, 27))
        self.recorder.setObjectName(_fromUtf8("recorder"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 683, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "FFT", None))
        self.openFile.setText(_translate("MainWindow", "Open File", None))
        self.play.setText(_translate("MainWindow", "Play", None))
        self.stop.setText(_translate("MainWindow", "Stop", None))
        self.recorder.setText(_translate("MainWindow", "Recorder", None))

from PyQt4 import Qwt5
