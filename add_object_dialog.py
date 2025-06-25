from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

class AddObjectDialog(QtWidgets.QDialog):
    def __init__(self, db):
        super().__init__()
        self.db = db
        self.setWindowTitle("Добавление объекта")
        self.setModal(True)
        layout = QtWidgets.QFormLayout()

        self.name_input = QtWidgets.QLineEdit()
        self.category_input = QtWidgets.QLineEdit()
        self.date_input = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.desc_input = QtWidgets.QTextEdit()

        layout.addRow("Название:", self.name_input)
        layout.addRow("Категория:", self.category_input)
        layout.addRow("Дата получения:", self.date_input)
        layout.addRow("Описание:", self.desc_input)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        layout.addRow(btns)
        self.setLayout(layout)

        btns.accepted.connect(self.save)
        btns.rejected.connect(self.reject)

    # добавление объекта
    def save(self):
        name = self.name_input.text().strip()
        category = self.category_input.text().strip()
        date = self.date_input.date().toString("yyyy-MM-dd")
        description = self.desc_input.toPlainText().strip()

        if not name:
            QMessageBox.warning(self, "Ошибка", "Название обязательно.")
            return

        self.db.add_test_object(name, category, date, description)
        QMessageBox.information(self, "Успех", "Объект успешно удалён.")
        self.accept()
