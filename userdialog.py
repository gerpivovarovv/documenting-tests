from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox

class UserDialog(QtWidgets.QDialog):
    def __init__(self, db, user_id=None):
        super().__init__()
        self.db = db
        self.user_id = user_id

        self.setWindowTitle("Добавить пользователя" if user_id is None else "Редактировать пользователя")
        self.setFixedSize(350, 300)

        layout = QtWidgets.QFormLayout()

        self.login_input = QtWidgets.QLineEdit()
        self.nam_input = QtWidgets.QLineEdit()
        self.surname_input = QtWidgets.QLineEdit()
        self.patronymic_input = QtWidgets.QLineEdit()
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        self.role_combo = QtWidgets.QComboBox()
        self.role_combo.addItems(['engineer', 'expert', 'admin'])

        layout.addRow("Логин:", self.login_input)
        layout.addRow("Имя:", self.nam_input)
        layout.addRow("Фамилия:", self.surname_input)
        layout.addRow("Отчество:", self.patronymic_input)
        layout.addRow("Пароль:", self.password_input)
        layout.addRow("Роль:", self.role_combo)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        btns.accepted.connect(self.accept)
        btns.rejected.connect(self.reject)

        layout.addRow(btns)
        self.setLayout(layout)

        if user_id is not None:
            self.load_user_data()

    def load_user_data(self):
        user = self.db.get_user_by_id(self.user_id)
        if user:
            self.login_input.setText(user['login'])
            self.nam_input.setText(user['name'])
            self.surname_input.setText(user['surname'])
            self.patronymic_input.setText(user['patronymic'])
            self.password_input.setText(user['password'])
            idx = self.role_combo.findText(user['role'])
            if idx >= 0:
                self.role_combo.setCurrentIndex(idx)

    def accept(self):
        login = self.login_input.text().strip()
        name = self.nam_input.text().strip()
        surname = self.surname_input.text().strip()
        patronymic = self.patronymic_input.text().strip()
        password = self.password_input.text().strip()
        role = self.role_combo.currentText()

        if not login or not password or not name or not surname:
            QMessageBox.warning(self, "Ошибка", "Заполните все обязательные поля (логин, имя, фамилия, пароль)")
            return

        if self.user_id is None:
            if self.db.get_user(login) is not None:
                QMessageBox.warning(self, "Ошибка", "Пользователь с таким логином уже существует")
                return
            self.db.add_user(login, name, surname, patronymic, password, role)
        else:
            self.db.update_user(self.user_id, login, name, surname, patronymic, password, role)

        super().accept()