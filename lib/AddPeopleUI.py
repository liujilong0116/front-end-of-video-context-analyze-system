# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AddPeopleUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddPeople(object):
    def setupUi(self, AddPeople):
        AddPeople.setObjectName("AddPeople")
        AddPeople.resize(200, 410)
        self.lineEdit_name = QtWidgets.QLineEdit(AddPeople)
        self.lineEdit_name.setGeometry(QtCore.QRect(60, 250, 120, 24))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.label = QtWidgets.QLabel(AddPeople)
        self.label.setGeometry(QtCore.QRect(20, 254, 30, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AddPeople)
        self.label_2.setGeometry(QtCore.QRect(20, 284, 30, 16))
        self.label_2.setTextFormat(QtCore.Qt.AutoText)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(AddPeople)
        self.label_3.setGeometry(QtCore.QRect(20, 344, 30, 16))
        self.label_3.setObjectName("label_3")
        self.dateEdit_date = QtWidgets.QDateEdit(AddPeople)
        self.dateEdit_date.setGeometry(QtCore.QRect(60, 340, 120, 24))
        self.dateEdit_date.setObjectName("dateEdit_date")
        self.pushButton_select = QtWidgets.QPushButton(AddPeople)
        self.pushButton_select.setGeometry(QtCore.QRect(20, 370, 75, 24))
        self.pushButton_select.setObjectName("pushButton_select")
        self.comboBox_reason = QtWidgets.QComboBox(AddPeople)
        self.comboBox_reason.setGeometry(QtCore.QRect(60, 310, 120, 24))
        self.comboBox_reason.setObjectName("comboBox_reason")
        self.label_4 = QtWidgets.QLabel(AddPeople)
        self.label_4.setGeometry(QtCore.QRect(20, 314, 30, 16))
        self.label_4.setTextFormat(QtCore.Qt.AutoText)
        self.label_4.setObjectName("label_4")
        self.lineEdit_position = QtWidgets.QLineEdit(AddPeople)
        self.lineEdit_position.setGeometry(QtCore.QRect(60, 280, 120, 24))
        self.lineEdit_position.setObjectName("lineEdit_position")
        self.label_image = QtWidgets.QLabel(AddPeople)
        self.label_image.setGeometry(QtCore.QRect(20, 44, 160, 200))
        self.label_image.setText("")
        self.label_image.setObjectName("label_image")
        self.pushButton_submit = QtWidgets.QPushButton(AddPeople)
        self.pushButton_submit.setGeometry(QtCore.QRect(105, 370, 75, 24))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.widget = QtWidgets.QWidget(AddPeople)
        self.widget.setGeometry(QtCore.QRect(0, 0, 200, 30))
        self.widget.setMinimumSize(QtCore.QSize(200, 30))
        self.widget.setMaximumSize(QtCore.QSize(200, 30))
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

        self.retranslateUi(AddPeople)
        QtCore.QMetaObject.connectSlotsByName(AddPeople)

    def retranslateUi(self, AddPeople):
        _translate = QtCore.QCoreApplication.translate
        AddPeople.setWindowTitle(_translate("AddPeople", "添加人员"))
        self.label.setText(_translate("AddPeople", "姓名："))
        self.label_2.setText(_translate("AddPeople", "职位："))
        self.label_3.setText(_translate("AddPeople", "时间："))
        self.pushButton_select.setText(_translate("AddPeople", "选择"))
        self.label_4.setText(_translate("AddPeople", "原因："))
        self.pushButton_submit.setText(_translate("AddPeople", "确认"))

