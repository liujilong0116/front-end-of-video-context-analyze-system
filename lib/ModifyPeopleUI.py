# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ModifyPeopleUI.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ModifyPeople(object):
    def setupUi(self, ModifyPeople):
        ModifyPeople.setObjectName("ModifyPeople")
        ModifyPeople.resize(200, 415)
        self.label_image = QtWidgets.QLabel(ModifyPeople)
        self.label_image.setGeometry(QtCore.QRect(20, 44, 160, 200))
        self.label_image.setText("")
        self.label_image.setObjectName("label_image")
        self.label = QtWidgets.QLabel(ModifyPeople)
        self.label.setGeometry(QtCore.QRect(20, 254, 30, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(ModifyPeople)
        self.label_2.setGeometry(QtCore.QRect(20, 284, 30, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(ModifyPeople)
        self.label_3.setGeometry(QtCore.QRect(20, 314, 30, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(ModifyPeople)
        self.label_4.setGeometry(QtCore.QRect(20, 344, 30, 16))
        self.label_4.setObjectName("label_4")
        self.lineEdit_name = QtWidgets.QLineEdit(ModifyPeople)
        self.lineEdit_name.setGeometry(QtCore.QRect(60, 250, 120, 24))
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_position = QtWidgets.QLineEdit(ModifyPeople)
        self.lineEdit_position.setGeometry(QtCore.QRect(60, 280, 120, 24))
        self.lineEdit_position.setObjectName("lineEdit_position")
        self.comboBox_reason = QtWidgets.QComboBox(ModifyPeople)
        self.comboBox_reason.setGeometry(QtCore.QRect(60, 310, 120, 24))
        self.comboBox_reason.setObjectName("comboBox_reason")
        self.dateEdit_date = QtWidgets.QDateEdit(ModifyPeople)
        self.dateEdit_date.setGeometry(QtCore.QRect(60, 340, 120, 24))
        self.dateEdit_date.setObjectName("dateEdit_date")
        self.pushButton_select = QtWidgets.QPushButton(ModifyPeople)
        self.pushButton_select.setGeometry(QtCore.QRect(20, 370, 80, 30))
        self.pushButton_select.setObjectName("pushButton_select")
        self.pushButton_submit = QtWidgets.QPushButton(ModifyPeople)
        self.pushButton_submit.setGeometry(QtCore.QRect(105, 370, 80, 30))
        self.pushButton_submit.setObjectName("pushButton_submit")
        self.widget = QtWidgets.QWidget(ModifyPeople)
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

        self.retranslateUi(ModifyPeople)
        QtCore.QMetaObject.connectSlotsByName(ModifyPeople)

    def retranslateUi(self, ModifyPeople):
        _translate = QtCore.QCoreApplication.translate
        ModifyPeople.setWindowTitle(_translate("ModifyPeople", "修改信息"))
        self.label.setText(_translate("ModifyPeople", "姓名："))
        self.label_2.setText(_translate("ModifyPeople", "职位："))
        self.label_3.setText(_translate("ModifyPeople", "原因："))
        self.label_4.setText(_translate("ModifyPeople", "时间："))
        self.pushButton_select.setText(_translate("ModifyPeople", "选择"))
        self.pushButton_submit.setText(_translate("ModifyPeople", "确认"))

