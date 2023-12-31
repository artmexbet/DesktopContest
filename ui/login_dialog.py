# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login_dialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_LoginDialog(object):
    def setupUi(self, LoginDialog):
        LoginDialog.setObjectName("LoginDialog")
        LoginDialog.resize(320, 291)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(LoginDialog.sizePolicy().hasHeightForWidth())
        LoginDialog.setSizePolicy(sizePolicy)
        self.gridLayout = QtWidgets.QGridLayout(LoginDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(LoginDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.login_line = QtWidgets.QLineEdit(LoginDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.login_line.setFont(font)
        self.login_line.setObjectName("login_line")
        self.verticalLayout.addWidget(self.login_line)
        self.label_2 = QtWidgets.QLabel(LoginDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.password_line = QtWidgets.QLineEdit(LoginDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.password_line.setFont(font)
        self.password_line.setInputMethodHints(QtCore.Qt.ImhHiddenText|QtCore.Qt.ImhNoAutoUppercase|QtCore.Qt.ImhNoPredictiveText|QtCore.Qt.ImhSensitiveData)
        self.password_line.setText("")
        self.password_line.setEchoMode(QtWidgets.QLineEdit.Password)
        self.password_line.setClearButtonEnabled(False)
        self.password_line.setObjectName("password_line")
        self.verticalLayout.addWidget(self.password_line)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.submit_btn = QtWidgets.QPushButton(LoginDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.submit_btn.setFont(font)
        self.submit_btn.setObjectName("submit_btn")
        self.verticalLayout.addWidget(self.submit_btn)
        self.label_3 = QtWidgets.QLabel(LoginDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.register_btn = QtWidgets.QPushButton(LoginDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.register_btn.setFont(font)
        self.register_btn.setObjectName("register_btn")
        self.verticalLayout.addWidget(self.register_btn)
        self.status = QtWidgets.QLabel(LoginDialog)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.status.setFont(font)
        self.status.setStyleSheet("color: rgb(255, 0, 0);")
        self.status.setText("")
        self.status.setAlignment(QtCore.Qt.AlignCenter)
        self.status.setObjectName("status")
        self.verticalLayout.addWidget(self.status)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)

        self.retranslateUi(LoginDialog)
        QtCore.QMetaObject.connectSlotsByName(LoginDialog)

    def retranslateUi(self, LoginDialog):
        _translate = QtCore.QCoreApplication.translate
        LoginDialog.setWindowTitle(_translate("LoginDialog", "Вход"))
        self.label.setText(_translate("LoginDialog", "Логин"))
        self.label_2.setText(_translate("LoginDialog", "Пароль"))
        self.submit_btn.setText(_translate("LoginDialog", "Войти"))
        self.label_3.setText(_translate("LoginDialog", "Нет аккаунта? - Зарегистрируйся!"))
        self.register_btn.setText(_translate("LoginDialog", "Регистрация"))
