from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

class ExpertWindow(QtWidgets.QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("Окно эксперта")
        self.resize(800, 600)

        layout = QtWidgets.QVBoxLayout(self)

        # Список результатов
        self.results_list = QtWidgets.QListWidget()
        layout.addWidget(self.results_list)

        # Кнопка загрузить выбранный результат
        self.load_button = QtWidgets.QPushButton("Загрузить протокол")
        layout.addWidget(self.load_button)

        # Текстовое поле протокола
        self.protocol_text = QtWidgets.QTextEdit()
        layout.addWidget(self.protocol_text)

        # Кнопка сохранить протокол
        self.save_button = QtWidgets.QPushButton("Сохранить протокол")
        layout.addWidget(self.save_button)

        self.load_button.clicked.connect(self.load_protocol)
        self.save_button.clicked.connect(self.save_protocol)

        self.load_results()

    def load_results(self):
        self.results_list.clear()
        results = self.db.get_results_for_expert(self.user_id)
        for r in results:
            item_text = f"ID:{r['result_id']} | Объект: {r['object_name']} | Дата: {r['test_date']}"
            item = QtWidgets.QListWidgetItem(item_text)
            item.setData(QtCore.Qt.UserRole, r['result_id'])
            self.results_list.addItem(item)

    def load_protocol(self):
        selected = self.results_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите результат испытания")
            return
        result_id = selected.data(QtCore.Qt.UserRole)
        protocol = self.db.get_protocol_by_result(result_id)
        if protocol:
            self.protocol_text.setPlainText(protocol['summary'])
        else:
            self.protocol_text.clear()

    def save_protocol(self):
        selected = self.results_list.currentItem()
        if not selected:
            QMessageBox.warning(self, "Ошибка", "Выберите результат испытания")
            return
        result_id = selected.data(QtCore.Qt.UserRole)
        summary = self.protocol_text.toPlainText().strip()
        if not summary:
            QMessageBox.warning(self, "Ошибка", "Поле протокола не может быть пустым")
            return
        self.db.save_protocol(result_id, summary)
        QMessageBox.information(self, "Успех", "Протокол сохранён")
