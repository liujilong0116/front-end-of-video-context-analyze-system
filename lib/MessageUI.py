# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MessageUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Message(object):
    def setupUi(self, Message):
        Message.setObjectName("Message")
        Message.resize(260, 150)
        self.label = QtWidgets.QLabel(Message)
        self.label.setGeometry(QtCore.QRect(28, 45, 200, 50))
        self.label.setText("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.pushButton_confirm = QtWidgets.QPushButton(Message)
        self.pushButton_confirm.setGeometry(QtCore.QRect(90, 110, 80, 30))
        self.pushButton_confirm.setObjectName("pushButton_confirm")
        self.widget = QtWidgets.QWidget(Message)
        self.widget.setGeometry(QtCore.QRect(0, 0, 260, 30))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.label_title = QtWidgets.QLabel(self.widget)
        self.label_title.setText("")
        self.label_title.setObjectName("label_title")
        self.gridLayout.addWidget(self.label_title, 0, 1, 1, 1)
        self.widget_icon = QtWidgets.QWidget(self.widget)
        self.widget_icon.setMinimumSize(QtCore.QSize(20, 20))
        self.widget_icon.setMaximumSize(QtCore.QSize(20, 20))
        self.widget_icon.setObjectName("widget_icon")
        self.gridLayout.addWidget(self.widget_icon, 0, 0, 1, 1)
        self.pushButton_close = QtWidgets.QPushButton(self.widget)
        self.pushButton_close.setMinimumSize(QtCore.QSize(20, 20))
        self.pushButton_close.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_close.setText("")
        self.pushButton_close.setObjectName("pushButton_close")
        self.gridLayout.addWidget(self.pushButton_close, 0, 2, 1, 1)

        self.retranslateUi(Message)
        QtCore.QMetaObject.connectSlotsByName(Message)

    def retranslateUi(self, Message):
        _translate = QtCore.QCoreApplication.translate
        Message.setWindowTitle(_translate("Message", "提示"))
        self.pushButton_confirm.setText(_translate("Message", "确认"))

