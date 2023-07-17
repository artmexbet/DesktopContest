import json

import requests
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QDialog, QMessageBox, QFileDialog, QTextEdit

from ui.code_review_dialog import Ui_CodeReviewDialog
from ui.login_dialog import Ui_LoginDialog
from ui.register_dialog import Ui_RegisterDialog
from ui.save_tests_dialog import Ui_Dialog
from utillities import SavedData, Network, CustomListWidgetItem


class SaveTestDialog(QDialog, Ui_Dialog):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.save_btn.clicked.connect(self.save)
        self.add_row_btn.clicked.connect(self.add_row)
        self.remove_row_btn.clicked.connect(lambda: self.tableWidget.setRowCount(self.tableWidget.rowCount() - 1))

    def add_row(self):
        self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 0, QTextEdit())
        self.tableWidget.setCellWidget(self.tableWidget.rowCount() - 1, 1, QTextEdit())
        self.tableWidget.resizeRowsToContents()

    def save(self):
        temp = {"tests": []}
        for row in range(self.tableWidget.rowCount()):
            print(row)
            temp["tests"].append({"input": self.tableWidget.cellWidget(row, 0).toPlainText(),
                                  "output": self.tableWidget.cellWidget(row, 1).toPlainText()})
        filename, res = QFileDialog.getSaveFileName(self, "Выберите файл", "", "JSON *.json")
        if not filename:
            return
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(temp, f, ensure_ascii=False, indent=4)


class RegisterDialog(QDialog, Ui_RegisterDialog):
    def __init__(self, config: SavedData):
        super().__init__()
        self.setupUi(self)

        self.config = config
        self.is_ok = False

        self.register_btn.clicked.connect(self.register)

    def register(self):
        login, password, name, email = self.login, self.password, self.name, self.email
        if not login or not password or not name or not email:
            self.status.setText("Все поля должны быть заполнены")
            return
        response = requests.post(f"{self.config.server}/reg",
                                 json={"login": login, "password": password, "name": self.name, "email": self.email})
        if response.status_code != 200:
            self.status.setText(response.json()["status"])
            return

        self.response = response.json()
        QMessageBox.information(self, "Итог", "Регистрация успешно выполнена")
        self.close()

    @property
    def password(self) -> str:
        return self.password_line.text()

    @property
    def login(self) -> str:
        return self.login_line.text()

    @property
    def name(self) -> str:
        return self.name_line.text()

    @property
    def email(self) -> str:
        return self.email_line.text()


class LoginDialog(QDialog, Ui_LoginDialog):
    def __init__(self, config: SavedData):
        super().__init__()
        self.setupUi(self)

        self.config = config

        self.is_logined = False
        self.response = {}

        self.submit_btn.clicked.connect(self.submit)
        self.register_btn.clicked.connect(self.register)

    def submit(self):
        login = self.login
        password = self.password
        if login and password:
            response = requests.post(f"{self.config.server}/login",
                                     json={"login": login, "password": password})
            if response.status_code != 200:
                self.status.setText("Неверный логин или пароль")
                self.close()
                return
            self.response = response.json()
            self.config.data["jwt_refresh"] = self.response["jwt_refresh"]
            self.is_logined = True
            self.close()
        else:
            self.status.setText("Логин и пароль должны быть заполнены")

    def register(self):
        reg_form = RegisterDialog(self.config)
        reg_form.exec_()

        if not reg_form.is_ok:
            return

        self.config.data["jwt_refresh"] = reg_form.response["jwt_refresh"]
        self.is_logined = True
        self.close()

    @property
    def password(self) -> str:
        return self.password_line.text()

    @property
    def login(self) -> str:
        return self.login_line.text()


class CodeReviewDialog(QDialog, Ui_CodeReviewDialog):
    def __init__(self, network: Network, task_id):
        super().__init__()
        self.setupUi(self)

        solves = network.get_solves(task_id)
        for solve in solves:
            item = CustomListWidgetItem(solve["id"], solve)
            if solve["verdict"] == "OK":
                item.setBackground(QColor(0, 255, 0, 128))
            elif "Error" in solve["verdict"] or "Time limit" in solve["verdict"]:
                item.setBackground(QColor(255, 0, 0, 128))
            self.solves_list_widget.addItem(item)

        self.solves_list_widget.currentItemChanged.connect(self.on_item_changed)

    def on_item_changed(self, item):
        self.verdict_label.setText(f'Вердикт: {item.custom_data["verdict"]}')
        self.code_view.setText(item.custom_data["code"])
        self.time_label.setText(f'Время выполнения: {item.custom_data["time"]}мс')
