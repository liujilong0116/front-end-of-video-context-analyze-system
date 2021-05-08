# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddTvUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddTv(object):
    def setupUi(self, AddTv):
        AddTv.setObjectName("AddTv")
        AddTv.resize(315, 140)
        self.label = QtWidgets.QLabel(AddTv)
        self.label.setGeometry(QtCore.QRect(15, 44, 30, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AddTv)
        self.label_2.setGeometry(QtCore.QRect(15, 74, 30, 16))
        self.label_2.setObjectName("label_2")
        self.lineEdit_name = QtWidgets.QLineEdit(AddTv)
        self.lineEdit_name.setGeometry(QtCore.QRect(50, 40, 250, 24))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_url = QtWidgets.QLineEdit(AddTv)
        self.lineEdit_url.setGeometry(QtCore.QRect(50, 70, 250, 24))
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.pushButton_submit = QtWidgets.QPushButton(AddTv)
        self.pushButton_submit.setGeometry(QtCore.QRect(220, 100, 80, 30))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.widget = QtWidgets.QWidget(AddTv)
        self.widget.setGeometry(QtCore.QRect(0, 0, 315, 30))
        self.widget.setMinimumSize(QtCore.QSize(315, 30))
        self.widget.setMaximumSize(QtCore.QSize(315, 30))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setObjectName("gridLayout")
        self.widget_icon = QtWidgets.QWidget(self.widget)
        self.widget_icon.setMinimumSize(QtCore.QSize(20, 20))
        self.widget_icon.setMaximumSize(QtCore.QSize(20, 20))
        self.widget_icon.setObjectName("widget_icon")
        self.gridLayout.addWidget(self.widget_icon, 0, 0, 1, 1)
        self.label_title = QtWidgets.QLabel(self.widget)
        self.label_title.setText("")
        self.label_title.setObjectName("label_title")
        self.gridLayout.addWidget(self.label_title, 0, 1, 1, 1)
        self.pushButton_close = QtWidgets.QPushButton(self.widget)
        self.pushButton_close.setMinimumSize(QtCore.QSize(20, 20))
        self.pushButton_close.setMaximumSize(QtCore.QSize(20, 20))
        self.pushButton_close.setText("")
        self.pushButton_close.setObjectName("pushButton_close")
        self.gridLayout.addWidget(self.pushButton_close, 0, 2, 1, 1)

        self.retranslateUi(AddTv)
        QtCore.QMetaObject.connectSlotsByName(AddTv)

    def retranslateUi(self, AddTv):
        _translate = QtCore.QCoreApplication.translate
        AddTv.setWindowTitle(_translate("AddTv", "添加直播源"))
        self.label.setText(_translate("AddTv", "名称："))
        self.label_2.setText(_translate("AddTv", "地址："))
        self.pushButton_submit.setText(_translate("AddTv", "确认"))

