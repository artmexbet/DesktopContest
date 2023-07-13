import os
import sys
import json
from threading import Thread
from time import sleep

import requests
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QMessageBox, QListWidgetItem, QFileDialog
from ui.main_window import Ui_MainWindow
from ui.login_dialog import Ui_LoginDialog
from ui.register_dialog import Ui_RegisterDialog
from ui.code_review_dialog import Ui_CodeReviewDialog


class CustomListWidgetItem(QListWidgetItem):
    def __init__(self, item_text, custom_data=None):
        super().__init__(item_text)
        self.custom_data = custom_data


class SavedData:
    def __init__(self):
        if os.path.exists("config.json"):
            with open("config.json", encoding="utf-8") as f:
                self.data = json.load(f)
        else:
            self.data = {"server": "", "login": "", "jwt_refresh": ""}
            self.commit()

    def __getattr__(self, item):
        return self.data.get(item, None)

    def commit(self):
        with open("config.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)


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


class LoginManager:
    def __init__(self, config: SavedData):
        self.server = f"{config.server}"
        self.jwt_refresh = config.jwt_refresh
        self.refresh_head = {"Authorization": "Bearer {}".format(self.jwt_refresh)}

    @property
    def access_head(self) -> dict:
        jwt_access = requests.get(self.server + "/refresh", headers=self.refresh_head).json()["jwt_access"]
        return {"Authorization": f"Bearer {jwt_access}"}

    @property
    def user_info(self) -> dict:
        return requests.get(self.server + "/auth", headers=self.access_head).json()["info"]


class Network:
    def __init__(self, login_manager: LoginManager):
        self.login_manager = login_manager
        self.server = login_manager.server

    def send_task(self, body, task_id):
        response = requests.post(f"{self.server}/tasks/{task_id}", json=body, headers=self.login_manager.access_head)
        js = response.json()
        return js

    def check_solve(self, solve_id):
        response = requests.get(f"{self.server}/solves/{solve_id}", headers=self.login_manager.access_head).json()
        return response

    def get_solves(self, task_id):
        response = requests.get(f"{self.server}/tasks/{task_id}/solves", headers=self.login_manager.access_head).json()
        return response["solves"]

    def get_task(self, task_id):
        response = requests.get(f"{self.server}/tasks/{task_id}", headers=self.login_manager.access_head).json()
        return response

    @property
    def courses(self):
        return requests.get(f"{self.server}/courses", headers=self.login_manager.access_head).json()["courses"]


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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Получение данных от сервера и логинг
        self.config = SavedData()
        if not self.config.server:
            self.get_server()

        login_form = LoginDialog(self.config)
        login_form.exec_()
        if not login_form.is_logined:
            exit(0)

        self.login_manager = LoginManager(self.config)
        self.network = Network(self.login_manager)

        # Получение курсов для списка
        self.courses_list = self.network.courses
        for course in self.courses_list:
            item = CustomListWidgetItem(course["name"], course)
            item.setToolTip(course["description"])
            self.courses_list_widget.addItem(item)

        self.current_course = None
        self.current_lesson = None
        self.current_task = None

        self.current_filename = None

        # Привязки
        self.open_course_btn.clicked.connect(self.open_course)
        self.courses_list_widget.doubleClicked.connect(self.open_course)

        self.back_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(
            self.stackedWidget.currentIndex() - 1 if self.stackedWidget.currentIndex() - 1 >= 0 else 0))
        self.forward_btn.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(
            self.stackedWidget.currentIndex() + 1 if self.stackedWidget.currentIndex() + 1 <= 2 else 2))

        self.open_lesson_btn.clicked.connect(self.open_lesson)
        self.lessons_list_widget.doubleClicked.connect(self.open_lesson)
        self.tasks_list_widget.clicked.connect(self.open_task)

        self.add_file_btn.clicked.connect(self.add_file)
        self.send_task_btn.clicked.connect(self.send_task)
        self.check_solves_btn.clicked.connect(self.check_solves)

        self.stackedWidget.setCurrentWidget(self.courses_page)

        self.scrollArea.dropEvent = self.on_drop_event
        self.scrollArea.dragEnterEvent = self.on_drag_enter_event

    def on_drag_enter_event(self, e):
        if self.current_task is None:
            e.ignore()
            return

        mdata = e.mimeData()
        if mdata.hasUrls() and mdata.text().split(".")[-1] in ("py", ):
            e.accept()
        else:
            e.ignore()

    def on_drop_event(self, e):
        filename = e.mimeData().text().strip("file:///")
        self.current_filename = filename
        self.filepath_label.setText(f"Выбранный файл: {filename}")
        self.update_code()

    def check_solves(self):
        if self.current_task is None:
            return
        dialog = CodeReviewDialog(self.network, self.current_task["id"])
        dialog.exec_()

    def open_course(self):
        self.current_course = self.courses_list_widget.currentItem().custom_data

        self.lessons_list_widget.clear()

        for lesson in self.current_course["lessons"]:
            item = CustomListWidgetItem(lesson["name"], lesson)
            item.setToolTip(lesson["description"])
            self.lessons_list_widget.addItem(item)

        self.stackedWidget.setCurrentWidget(self.lessons_page)

    def open_lesson(self):
        if self.current_course is None:
            return

        self.current_lesson = self.lessons_list_widget.currentItem().custom_data
        self.current_lesson["tasks"].sort(key=lambda x: x["order"])

        self.reload_task_list()

        self.stackedWidget.setCurrentWidget(self.tasks_page)

    def reload_task_list(self):
        self.tasks_list_widget.clear()
        for task in self.current_lesson["tasks"]:
            solves = self.network.get_solves(task["id"])
            item = CustomListWidgetItem(task["name"], task)
            if solves and any(solve["verdict"] == "OK" for solve in solves):
                item.setBackground(QColor(0, 255, 0, 128))
            elif solves and all("Error" in solve["verdict"] or "Time limit" in solve["verdict"] for solve in solves):
                item.setBackground(QColor(255, 0, 0, 128))
            self.tasks_list_widget.addItem(item)

    def open_task(self):
        if self.current_lesson is None:
            return

        self.current_task = self.tasks_list_widget.currentItem().custom_data
        self.task_title_label.setText(self.current_task["name"])
        self.timelimit_label.setText(f"Максимальное время выполнения: {self.current_task['time_limit']}")
        self.task_condition_label.setText(self.current_task["task_condition"])
        self.filepath_label.setText("Загрузите файл (можно drag'n'drop)")
        self.current_filename = None
        self.verdict_label.setText("")
        self.code_browser.clear()

    def add_file(self):
        if self.current_task is None:
            return

        filename, res = QFileDialog.getOpenFileName(self, "Открыть файл", "", "Python files *.py")
        if not filename:
            return
        self.filepath_label.setText(f"Выбранный файл: {filename}")
        self.current_filename = filename
        self.update_code()

    def send_task(self):
        if self.current_task is None:
            return

        if self.current_filename is None and not self.code_browser.toPlainText():
            self.verdict_label.setText("Вы должны сначала прикрепить файл!")
            return

        body = {"code": self.code_browser.toPlainText()}
        response = self.network.send_task(body, self.current_task["id"])
        self.verdict_label.setText(response["status"])

        thread = Thread(
            target=check_task_status,
            args=(self.network, self, response["solve_id"]),
            name=response["solve_id"]
        )
        thread.start()

    def update_code(self):
        with open(self.current_filename, encoding="utf-8") as f:
            code = f.read()
        self.code_browser.setMarkdown(f"```python\n{code}\n```")

    def get_server(self):
        server, is_ok = QInputDialog.getText(self, "Ввод", "Введите адрес сервера")
        while not is_ok:
            server, is_ok = QInputDialog.getText(self, "Ввод", "Введите адрес сервера")
        self.config.data["server"] = server
        self.config.commit()


def check_task_status(network: Network, win: MainWindow, solve_id):
    sleep(3)
    resp = network.check_solve(solve_id)
    win.verdict_label.setText(resp["verdict"])
    win.reload_task_list()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
