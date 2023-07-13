# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.15.3
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 763)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.stackedWidget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stackedWidget.setEnabled(True)
        self.stackedWidget.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.stackedWidget.setObjectName("stackedWidget")
        self.courses_page = QtWidgets.QWidget()
        self.courses_page.setObjectName("courses_page")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.courses_page)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.courses_list_widget = QtWidgets.QListWidget(self.courses_page)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.courses_list_widget.setFont(font)
        self.courses_list_widget.setObjectName("courses_list_widget")
        self.gridLayout_4.addWidget(self.courses_list_widget, 0, 0, 1, 1)
        self.open_course_btn = QtWidgets.QPushButton(self.courses_page)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.open_course_btn.setFont(font)
        self.open_course_btn.setObjectName("open_course_btn")
        self.gridLayout_4.addWidget(self.open_course_btn, 1, 0, 1, 1)
        self.stackedWidget.addWidget(self.courses_page)
        self.lessons_page = QtWidgets.QWidget()
        self.lessons_page.setObjectName("lessons_page")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.lessons_page)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.lessons_list_widget = QtWidgets.QListWidget(self.lessons_page)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.lessons_list_widget.setFont(font)
        self.lessons_list_widget.setObjectName("lessons_list_widget")
        self.gridLayout_3.addWidget(self.lessons_list_widget, 0, 0, 1, 1)
        self.open_lesson_btn = QtWidgets.QPushButton(self.lessons_page)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.open_lesson_btn.setFont(font)
        self.open_lesson_btn.setObjectName("open_lesson_btn")
        self.gridLayout_3.addWidget(self.open_lesson_btn, 1, 0, 1, 1)
        self.stackedWidget.addWidget(self.lessons_page)
        self.tasks_page = QtWidgets.QWidget()
        self.tasks_page.setObjectName("tasks_page")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.tasks_page)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.tasks_list_widget = QtWidgets.QListWidget(self.tasks_page)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.tasks_list_widget.setFont(font)
        self.tasks_list_widget.setObjectName("tasks_list_widget")
        self.horizontalLayout.addWidget(self.tasks_list_widget)
        self.scrollArea = QtWidgets.QScrollArea(self.tasks_page)
        self.scrollArea.setMinimumSize(QtCore.QSize(700, 0))
        self.scrollArea.setAcceptDrops(True)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContentsOnFirstShow)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 698, 688))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.task_title_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.task_title_label.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.task_title_label.setFont(font)
        self.task_title_label.setText("")
        self.task_title_label.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignTop)
        self.task_title_label.setObjectName("task_title_label")
        self.verticalLayout.addWidget(self.task_title_label)
        self.timelimit_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.timelimit_label.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.timelimit_label.setFont(font)
        self.timelimit_label.setText("")
        self.timelimit_label.setAlignment(QtCore.Qt.AlignCenter)
        self.timelimit_label.setObjectName("timelimit_label")
        self.verticalLayout.addWidget(self.timelimit_label)
        self.task_condition_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.task_condition_label.setFont(font)
        self.task_condition_label.setText("")
        self.task_condition_label.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.task_condition_label.setObjectName("task_condition_label")
        self.verticalLayout.addWidget(self.task_condition_label)
        self.code_browser = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.code_browser.setFont(font)
        self.code_browser.setUndoRedoEnabled(True)
        self.code_browser.setReadOnly(False)
        self.code_browser.setObjectName("code_browser")
        self.verticalLayout.addWidget(self.code_browser)
        self.filepath_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.filepath_label.setMaximumSize(QtCore.QSize(16777215, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.filepath_label.setFont(font)
        self.filepath_label.setAlignment(QtCore.Qt.AlignCenter)
        self.filepath_label.setObjectName("filepath_label")
        self.verticalLayout.addWidget(self.filepath_label)
        self.add_file_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.add_file_btn.setFont(font)
        self.add_file_btn.setCheckable(True)
        self.add_file_btn.setChecked(True)
        self.add_file_btn.setAutoDefault(False)
        self.add_file_btn.setDefault(False)
        self.add_file_btn.setFlat(False)
        self.add_file_btn.setObjectName("add_file_btn")
        self.verticalLayout.addWidget(self.add_file_btn)
        self.send_task_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.send_task_btn.setFont(font)
        self.send_task_btn.setCheckable(True)
        self.send_task_btn.setChecked(False)
        self.send_task_btn.setAutoDefault(False)
        self.send_task_btn.setDefault(False)
        self.send_task_btn.setFlat(False)
        self.send_task_btn.setObjectName("send_task_btn")
        self.verticalLayout.addWidget(self.send_task_btn)
        self.verdict_label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
        self.verdict_label.setMaximumSize(QtCore.QSize(16777215, 100))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.verdict_label.setFont(font)
        self.verdict_label.setScaledContents(False)
        self.verdict_label.setAlignment(QtCore.Qt.AlignCenter)
        self.verdict_label.setWordWrap(True)
        self.verdict_label.setObjectName("verdict_label")
        self.verticalLayout.addWidget(self.verdict_label)
        self.check_solves_btn = QtWidgets.QPushButton(self.scrollAreaWidgetContents)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.check_solves_btn.setFont(font)
        self.check_solves_btn.setCheckable(True)
        self.check_solves_btn.setChecked(False)
        self.check_solves_btn.setAutoDefault(False)
        self.check_solves_btn.setDefault(False)
        self.check_solves_btn.setFlat(False)
        self.check_solves_btn.setObjectName("check_solves_btn")
        self.verticalLayout.addWidget(self.check_solves_btn)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.horizontalLayout.addWidget(self.scrollArea)
        self.stackedWidget.addWidget(self.tasks_page)
        self.gridLayout.addWidget(self.stackedWidget, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.back_btn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.back_btn.setFont(font)
        self.back_btn.setObjectName("back_btn")
        self.horizontalLayout_2.addWidget(self.back_btn)
        self.forward_btn = QtWidgets.QPushButton(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.forward_btn.setFont(font)
        self.forward_btn.setObjectName("forward_btn")
        self.horizontalLayout_2.addWidget(self.forward_btn)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stackedWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Контест"))
        self.open_course_btn.setText(_translate("MainWindow", "Открыть"))
        self.open_lesson_btn.setText(_translate("MainWindow", "Открыть"))
        self.filepath_label.setText(_translate("MainWindow", "Filepath"))
        self.add_file_btn.setText(_translate("MainWindow", "Загрузить файл"))
        self.send_task_btn.setText(_translate("MainWindow", "Отправить на проверку"))
        self.verdict_label.setText(_translate("MainWindow", "Вердикт"))
        self.check_solves_btn.setText(_translate("MainWindow", "Предыдущие решения"))
        self.back_btn.setText(_translate("MainWindow", "|< Назад"))
        self.forward_btn.setText(_translate("MainWindow", "Вперёд >|"))
