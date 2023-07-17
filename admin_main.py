from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QFileDialog
import sys
import json

from dialogs import LoginDialog, SaveTestDialog
from utillities import SavedData, LoginManager, Network
from ui.admin_main_window import Ui_AdminMainWindow


class MainWindow(QMainWindow, Ui_AdminMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.config = SavedData()
        if not self.config.server:
            self.get_server()

        login_form = LoginDialog(self.config)
        login_form.exec_()
        if not login_form.is_logined:
            exit(0)

        self.login_manager = LoginManager(self.config)
        self.network = Network(self.login_manager)

        self.languages_list = None
        self.courses_list = None

        self.image_path = None
        self.tests = None

        self.to_course()

        self.to_course_btn.clicked.connect(self.to_course)
        self.to_lessons_btn.clicked.connect(self.to_lessons)
        self.to_tasks_btn.clicked.connect(self.to_tasks)

        self.add_picture.clicked.connect(self.choose_image)
        self.create_course_btn.clicked.connect(self.create_course)
        self.create_lesson_btn.clicked.connect(self.create_lesson)
        self.add_tests_btn.clicked.connect(self.choose_tests)
        self.create_task_btn.clicked.connect(self.create_task)
        self.create_tests.clicked.connect(self.create_tests_action)

        self.task_course_box.currentIndexChanged.connect(self.on_current_course_changed)

    def create_tests_action(self):
        dialog = SaveTestDialog()
        dialog.exec_()

    def choose_tests(self):
        filename, res = QFileDialog.getOpenFileName(self, "Выберите тесты", "", "JSON *.json")

        if not filename:
            return

        with open(filename, encoding="utf-8") as f:
            tests = f.read()

        js_tests = json.loads(tests)
        if "tests" not in js_tests:
            self.statusbar.showMessage("Неверный формат тестов! В словаре должен быть ключ tests")
            return
        if any("input" not in test or "output" not in test for test in js_tests["tests"]):
            self.statusbar.showMessage("Неверный формат тестов! Под ключом tests должен лежать список тестов в "
                                       "формате {'input': ..., 'output': ...}")
            return
        self.tests = tests

    def on_current_course_changed(self):
        self.task_lesson_box.clear()

        course = self.task_course_box.currentData()
        lessons = course["lessons"]
        if not lessons:
            self.statusbar.showMessage("Выберите курс с хотя бы одним уроком!")
            return

        for lesson in lessons:
            self.task_lesson_box.addItem(lesson["name"], lesson)

    def choose_image(self):
        filename, res = QFileDialog.getOpenFileName(self, "Выберите картинку", "", "Изображения *.png *.jpg")

        if not filename:
            return

        self.image_path = filename
        self.add_picture.setText(f"Выбрана картинка: {self.image_path}")

    def create_course(self):
        course_name = self.course_title_line.text()
        if not course_name:
            self.statusbar.showMessage("Необходимо указать имя курса")
            return

        course_description = self.course_description_line.toPlainText()
        language = self.language_box.currentData()

        if self.image_path is None:
            self.statusbar.showMessage("Необходимо прикрепить картинку!")
            return

        resp = self.network.add_course(course_name, course_description, language["id"], self.image_path)
        self.statusbar.showMessage(resp["status"])
        self.course_title_line.clear()
        self.course_description_line.clear()

    def create_lesson(self):
        if not self.courses_list:
            self.statusbar.showMessage("Сначала необходимо создать хотя бы один курс")
            return

        lesson_name = self.lesson_name_line.text()
        if not lesson_name:
            self.statusbar.showMessage("Необходимо указать имя урока")

        lesson_description = self.lesson_description_edit.toPlainText()
        resp = self.network.add_lesson(lesson_name, lesson_description, self.course_box.currentData()["id"])
        print(resp)
        self.statusbar.showMessage(resp["status"])
        self.lesson_name_line.clear()
        self.lesson_description_edit.clear()

    def create_task(self):
        if not self.courses_list:
            self.statusbar.showMessage("Сначала необходимо создать хотя бы один курс")
            return

        course = self.task_course_box.currentData()
        if not course["lessons"]:
            self.statusbar.showMessage("Сначала создайте уроки для этого курса или выберите другой")
            return

        lesson = self.task_lesson_box.currentData()
        if not lesson:
            self.statusbar.showMessage("Выберите курс!")
            return

        task_name = self.task_title_line.text()
        if not task_name:
            self.statusbar.showMessage("Введите название!")
            return

        task_condition = self.task_condition_line.toPlainText()
        if not task_condition:
            self.statusbar.showMessage("Введите условие!")
            return

        if self.tests is None:
            self.statusbar.showMessage("Добавьте тесты!")
            return

        time_limit = self.time_limit.value()

        resp = self.network.add_task(task_name, task_condition, time_limit, lesson["id"], self.tests)
        print(resp)
        self.statusbar.showMessage(resp["status"])

        self.tests = None
        self.task_condition_line.clear()
        self.task_title_line.clear()

    def to_course(self):
        self.stackedWidget.setCurrentWidget(self.add_courses_page)
        self.language_box.clear()
        self.languages_list = self.network.languages

        for language in self.languages_list:
            self.language_box.addItem(language["name"], language)

        if not self.languages_list:
            self.statusbar.showMessage("Создайте хотя бы один язык в базе данных!")

    def to_lessons(self):
        self.stackedWidget.setCurrentWidget(self.add_lessons_page)
        self.course_box.clear()
        self.courses_list = self.network.courses

        for course in self.courses_list:
            self.course_box.addItem(course["name"], course)

        if not self.courses_list:
            self.statusbar.showMessage("Создайте хотя бы один курс!")

    def to_tasks(self):
        self.stackedWidget.setCurrentWidget(self.add_task_page)
        self.task_course_box.clear()
        self.task_lesson_box.clear()
        self.courses_list = self.network.courses

        for course in self.courses_list:
            self.task_course_box.addItem(course["name"], course)

        if not self.courses_list:
            self.statusbar.showMessage("Создайте хотя бы один курс и добавьте к нему урок!")
            return

        for lesson in self.courses_list[0]["lessons"]:
            self.task_lesson_box.addItem(lesson["name"], lesson)

        if not self.courses_list[0]["lessons"]:
            self.statusbar.showMessage("В данном курсе нет уроков!")

    def get_server(self):
        server, is_ok = QInputDialog.getText(self, "Ввод", "Введите адрес сервера")
        while not is_ok:
            server, is_ok = QInputDialog.getText(self, "Ввод", "Введите адрес сервера")
        self.config.data["server"] = server
        self.config.commit()


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.excepthook = except_hook
    sys.exit(app.exec_())
