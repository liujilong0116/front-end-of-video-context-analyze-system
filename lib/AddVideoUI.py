# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddVideoUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddVideo(object):
    def setupUi(self, AddVideo):
        AddVideo.setObjectName("AddVideo")
        AddVideo.resize(240, 275)
        self.label_image = QtWidgets.QLabel(AddVideo)
        self.label_image.setGeometry(QtCore.QRect(60, 45, 120, 120))
        self.label_image.setMinimumSize(QtCore.QSize(120, 120))
        self.label_image.setText("")
        self.label_image.setObjectName("label_image")
        self.lineEdit_name = QtWidgets.QLineEdit(AddVideo)
        self.lineEdit_name.setGeometry(QtCore.QRect(50, 171, 175, 24))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.label = QtWidgets.QLabel(AddVideo)
        self.label.setGeometry(QtCore.QRect(5, 175, 41, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AddVideo)
        self.label_2.setGeometry(QtCore.QRect(17, 205, 30, 16))
        self.label_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.lineEdit_id = QtWidgets.QLineEdit(AddVideo)
        self.lineEdit_id.setGeometry(QtCore.QRect(50, 201, 175, 24))
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.pushButton_select = QtWidgets.QPushButton(AddVideo)
        self.pushButton_select.setGeometry(QtCore.QRect(15, 230, 80, 30))
        self.pushButton_select.setObjectName("pushButton_select")
        self.pushButton_submit = QtWidgets.QPushButton(AddVideo)
        self.pushButton_submit.setGeometry(QtCore.QRect(145, 230, 80, 30))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.widget = QtWidgets.QWidget(AddVideo)
        self.widget.setGeometry(QtCore.QRect(0, 0, 240, 30))
        self.widget.setMinimumSize(QtCore.QSize(240, 30))
        self.widget.setMaximumSize(QtCore.QSize(240, 30))
        self.widget.setObjectName("widget")
        self.gridLayout = QtWidgets.QGridLayout(self.widget)
        self.gridLayout.setContentsMargins(2, 2, 2, 2)
        self.gridLayout.setSpacing(2)
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

        self.retranslateUi(AddVideo)
        QtCore.QMetaObject.connectSlotsByName(AddVideo)

    def retranslateUi(self, AddVideo):
        _translate = QtCore.QCoreApplication.translate
        AddVideo.setWindowTitle(_translate("AddVideo", "添加视频"))
        self.label.setText(_translate("AddVideo", "视频名："))
        self.label_2.setText(_translate("AddVideo", "编号："))
        self.pushButton_select.setText(_translate("AddVideo", "选择"))
        self.pushButton_submit.setText(_translate("AddVideo", "确认"))

