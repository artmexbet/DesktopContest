# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_RegisterDialog(object):
    def setupUi(self, RegisterDialog):
        RegisterDialog.setObjectName("RegisterDialog")
        RegisterDialog.resize(300, 353)
        self.gridLayout = QtWidgets.QGridLayout(RegisterDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.login_line = QtWidgets.QLineEdit(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.login_line.setFont(font)
        self.login_line.setObjectName("login_line")
        self.verticalLayout.addWidget(self.login_line)
        self.label_2 = QtWidgets.QLabel(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.password_line = QtWidgets.QLineEdit(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.password_line.setFont(font)
        self.password_line.setCursor(QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.password_line.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.password_line.setText("")
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setClearButtonEnabled(False)
        self.password_line.setObjectName("password_line")
        self.verticalLayout.addWidget(self.password_line)
        self.label_3 = QtWidgets.QLabel(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.name_line = QtWidgets.QLineEdit(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.name_line.setFont(font)
        self.name_line.setInputMethodHints(QtCore.Qt.ImhNone)
        self.name_line.setText("")
        self.name_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.name_line.setClearButtonEnabled(False)
        self.name_line.setObjectName("name_line")
        self.verticalLayout.addWidget(self.name_line)
        self.label_4 = QtWidgets.QLabel(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.email_line = QtWidgets.QLineEdit(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.email_line.setFont(font)
        self.email_line.setInputMethodHints(QtCore.Qt.ImhNone)
        self.email_line.setText("")
        self.email_line.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.email_line.setClearButtonEnabled(False)
        self.email_line.setObjectName("email_line")
        self.verticalLayout.addWidget(self.email_line)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.register_btn = QtWidgets.QPushButton(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.register_btn.setFont(font)
        self.register_btn.setObjectName("register_btn")
        self.verticalLayout.addWidget(self.register_btn)
        self.status = QtWidgets.QLabel(RegisterDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.status.setFont(font)
        self.status.setStyleSheet("color: rgb(255, 0, 0);")
        self.status.setText("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")
        self.verticalLayout.addWidget(self.status)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(RegisterDialog)
        QtCore.QMetaObject.connectSlotsByName(RegisterDialog)

    def retranslateUi(self, RegisterDialog):
        _translate = QtCore.QCoreApplication.translate
        RegisterDialog.setWindowTitle(_translate("RegisterDialog", "Регистрация"))
        self.label.setText(_translate("RegisterDialog", "Логин"))
        self.label_2.setText(_translate("RegisterDialog", "Пароль"))
        self.label_3.setText(_translate("RegisterDialog", "Имя"))
        self.label_4.setText(_translate("RegisterDialog", "Email"))
        self.register_btn.setText(_translate("RegisterDialog", "Регистрация"))
