from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from add_user_dialog import AddUserDialog
from userdialog import UserDialog

class UserManagementWindow(QtWidgets.QWidget):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Управление пользователями")
        self.resize(700, 400)

        self.layout = QtWidgets.QVBoxLayout()
        self.setLayout(self.layout)

        # Таблица пользователей
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels(['ID', 'Login', 'Имя', 'Фамилия', 'Отчество', 'Роль', 'Пароль'])
        self.layout.addWidget(self.table)

        # Кнопки
        self.buttons_layout = QtWidgets.QHBoxLayout()
        self.btn_add = QtWidgets.QPushButton("Добавить")
        self.btn_edit = QtWidgets.QPushButton("Редактировать")
        self.btn_delete = QtWidgets.QPushButton("Удалить")

        self.buttons_layout.addWidget(self.btn_add)
        self.buttons_layout.addWidget(self.btn_edit)
        self.buttons_layout.addWidget(self.btn_delete)
        self.layout.addLayout(self.buttons_layout)

        # Подключаем слоты
        self.btn_add.clicked.connect(self.add_user)
        self.btn_edit.clicked.connect(self.edit_user)
        self.btn_delete.clicked.connect(self.delete_user)

        # Загружаем пользователей
        self.load_users()

    def load_users(self):
        try:
            self.table.setRowCount(0)
            users = self.db.get_all_users()
            for row_idx, user in enumerate(users):
                self.table.insertRow(row_idx)
                self.table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(user['user_id'])))
                self.table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(user['login']))
                self.table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(user['name']))
                self.table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(user['surname']))
                self.table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(user['patronymic']))
                self.table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(user['role']))
                self.table.setItem(row_idx, 6, QtWidgets.QTableWidgetItem(user['password']))


            self.table.resizeColumnsToContents()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка загрузки", f"Не удалось загрузить пользователей:\n{e}")

    def add_user(self):
        dialog = AddUserDialog(self)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            data = dialog.get_data()
            try:
                cursor = self.db.cursor
                cursor.execute("""
                        INSERT INTO users (login, name, surname, patronymic, role, password)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    """, (
                    data['login'],
                    data['nam'],
                    data['surname'],
                    data['patronymic'],
                    data['role'],
                    data['password']
                ))
                self.db.commit()
                self.load_users()
                QMessageBox.information(self, "Успех", "Пользователь добавлен.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось добавить пользователя:\n{e}")

    def edit_user(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для редактирования.")
            return

        user_id_item = self.table.item(selected, 0)
        if not user_id_item:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить ID пользователя.")
            return

        user_id = int(user_id_item.text())

        dialog = UserDialog(self.db, user_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_users()
            QMessageBox.information(self, "Успех", "Данные пользователя обновлены.")

    def delete_user(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите пользователя для удаления.")
            return

        user_id_item = self.table.item(selected_row, 0)
        if user_id_item is None:
            QMessageBox.warning(self, "Ошибка", "Не удалось получить ID пользователя.")
            return

        user_id = int(user_id_item.text())

        confirm = QMessageBox.question(
            self,
            "Подтверждение",
            f"Вы уверены, что хотите удалить пользователя с ID {user_id}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if confirm == QMessageBox.Yes:
            try:
                self.db.delete_user(user_id)
                self.load_users()
                QMessageBox.information(self, "Успех", "Пользователь успешно удалён.")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Не удалось удалить пользователя:\n{e}")