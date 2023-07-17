import json
import os

import requests
from PyQt5.QtWidgets import QListWidgetItem


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

    def get_lesson(self, lesson_id):
        response = requests.get(f"{self.server}/lessons/{lesson_id}", headers=self.login_manager.access_head).json()
        response["tasks"].sort(key=lambda x: x["order"])
        return response

    def add_course(self, name: str, description: str, language_id: str, pic_path: str):
        response = requests.post(
            f"{self.server}/courses",
            data={"name": name, "description": description, "language_id": language_id, "is_public": True},
            files={"pic": open(pic_path, "rb")},
            headers=self.login_manager.access_head
        ).json()
        return response

    def add_lesson(self, name, description, course_id):
        response = requests.post(
            f"{self.server}/lessons",
            json={"name": name, "description": description, "course_id": course_id},
            headers=self.login_manager.access_head
        ).json()
        return response

    def add_task(self, name, condition, time_limit, lesson_id, tests):
        response = requests.post(
            f"{self.server}/tasks",
            data={
                "lesson_id": lesson_id,
                "name": name,
                "task_condition": condition,
                "tests": tests,
                "time_limit": time_limit
            },
            headers=self.login_manager.access_head
        ).json()
        return response

    @property
    def courses(self):
        return requests.get(f"{self.server}/courses", headers=self.login_manager.access_head).json()["courses"]

    @property
    def languages(self):
        return requests.get(f"{self.server}/languages", headers=self.login_manager.access_head).json()["languages"]
