from PyQt5 import QtWidgets

class AddUserDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Добавить пользователя")
        self.setModal(True)
        self.resize(300, 300)

        layout = QtWidgets.QFormLayout()

        self.login_input = QtWidgets.QLineEdit()
        self.nam_input = QtWidgets.QLineEdit()
        self.surname_input = QtWidgets.QLineEdit()
        self.patronymic_input = QtWidgets.QLineEdit()
        self.role_input = QtWidgets.QComboBox()
        self.role_input.addItems(['admin', 'engineer', 'expert'])
        self.password_input = QtWidgets.QLineEdit()
        self.password_input.setEchoMode(QtWidgets.QLineEdit.Password)

        layout.addRow("Логин:", self.login_input)
        layout.addRow("Имя:", self.nam_input)
        layout.addRow("Фамилия:", self.surname_input)
        layout.addRow("Отчество:", self.patronymic_input)
        layout.addRow("Роль:", self.role_input)
        layout.addRow("Пароль:", self.password_input)

        self.button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        layout.addRow(self.button_box)

        self.setLayout(layout)

        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    # Загрузка пользователей
    def get_data(self):
        return {
            "login": self.login_input.text(),
            "nam": self.nam_input.text(),
            "surname": self.surname_input.text(),
            "patronymic": self.patronymic_input.text(),
            "role": self.role_input.currentText(),
            "password": self.password_input.text(),
        }