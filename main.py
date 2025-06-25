# Производственная практика ПП02 по модулю ПМ02. ПМ.02 Осуществление интеграции
# программных модулей
# Название: Система учета испытаний.
# Разработал: Пивоваров Герман Борисович, ТДБ-61
# Дата: 17.06.2025
# Язык: Python, MySQL
# Краткое описание:
# Данное программное обеспечение предназначено для организации работы отдела тестирования ПО
# Задание:
# Разработать ПО, которое должно обеспечивать:
# - сиcтема авторизации;
# - управление данными об объектах испытаний;
# - учет результатов тестирования;
# - работа с протоколами и заключениями.


import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from db import DB
from user_management_window import UserManagementWindow
from engineer_window import EngineerWindow
from expert_window import ExpertWindow


class LoginWindow(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Вход в систему")
        self.setFixedSize(300, 150)

        layout = QtWidgets.QFormLayout()

        self.login_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        layout.addRow("Логин:", self.login_input)
        layout.addRow("Пароль:", self.password_input)

        self.login_btn = QtWidgets.QPushButton("Войти")
        self.login_btn.clicked.connect(self.try_login)

        layout.addWidget(self.login_btn)
        self.setLayout(layout)

    # Аутентификация
    def try_login(self):
        login = self.login_input.text().strip()
        password = self.password_input.text().strip()

        user = self.db.get_user(login)
        if user is None or user['password'] != password:
            QMessageBox.warning(self, "Ошибка", "Неверный логин или пароль")
            return

        role = user['role']
        if role == 'engineer':
            self.main_window = EngineerWindow(self.db, user['user_id'])
        elif role == 'admin':
            self.main_window = UserManagementWindow(self.db)
        elif role == 'expert':
            self.main_window = ExpertWindow(self.db, user['user_id'])
        else:
            QMessageBox.warning(self, "Ошибка", "Неизвестная роль пользователя")
            return
        self.main_window.show()
        self.close()


app = QtWidgets.QApplication(sys.argv)
db = DB()
login_window = LoginWindow(db)
login_window.show()
sys.exit(app.exec_())