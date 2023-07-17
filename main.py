import sys
from threading import Thread
from time import sleep

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog, QTableWidgetItem

from dialogs import LoginDialog, CodeReviewDialog
from ui.main_window import Ui_MainWindow
from utillities import CustomListWidgetItem, SavedData, LoginManager, Network


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

        self.current_lesson = self.network.get_lesson(self.lessons_list_widget.currentItem().custom_data["id"])
        self.current_lesson["tasks"].sort(key=lambda x: x["order"])

        self.reload_task_list()

        self.stackedWidget.setCurrentWidget(self.tasks_page)

    def reload_task_list(self):
        self.tasks_list_widget.clear()
        for task in self.current_lesson["tasks"]:
            # solves = self.network.get_solves(task["id"])
            item = CustomListWidgetItem(task["name"], task)
            if "is_solved" in task:
                if task["is_solved"]:
                    item.setBackground(QColor(0, 255, 0, 128))
                else:
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
        self.input_label.setText(self.current_task["tests"][0]["input"])
        self.output_label.setText(self.current_task["tests"][0]["output"])
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
            args=(self.network, self, response["solve_id"], self.current_task["time_limit"]),
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


def check_task_status(network: Network, win: MainWindow, solve_id, wait_time: int):
    sleep(wait_time * 3)
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
