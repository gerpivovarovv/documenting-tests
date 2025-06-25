from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QMessageBox
from add_object_dialog import AddObjectDialog
from add_result_dialog import AddResultDialog
from test_result_dialog import TestResultsDialog


class EngineerWindow(QtWidgets.QWidget):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id
        self.setWindowTitle("Рабочее место инженера")
        self.resize(800, 500)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Таблица объектов испытаний
        self.table = QtWidgets.QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(['ID', 'Название', 'Категория', 'Дата получения', 'Описание'])
        layout.addWidget(self.table)

        # Кнопки
        btn_layout = QtWidgets.QHBoxLayout()
        self.btn_add_object = QtWidgets.QPushButton("Добавить объект")
        self.btn_add_result = QtWidgets.QPushButton("Внести результат")
        self.view_results_btn = QtWidgets.QPushButton("Просмотреть результаты")
        btn_layout.addWidget(self.view_results_btn)
        btn_layout.addWidget(self.btn_add_object)
        btn_layout.addWidget(self.btn_add_result)

        layout.addLayout(btn_layout)

        self.btn_add_object.clicked.connect(self.add_object)
        self.view_results_btn.clicked.connect(self.show_results)
        self.btn_add_result.clicked.connect(self.add_result)

        self.load_objects()

    def load_objects(self):
        self.table.setRowCount(0)
        objects = self.db.get_all_test_objects()
        for i, obj in enumerate(objects):
            self.table.insertRow(i)
            self.table.setItem(i, 0, QtWidgets.QTableWidgetItem(str(obj['object_id'])))
            self.table.setItem(i, 1, QtWidgets.QTableWidgetItem(obj['name']))
            self.table.setItem(i, 2, QtWidgets.QTableWidgetItem(obj['category'] or ""))
            self.table.setItem(i, 3, QtWidgets.QTableWidgetItem(str(obj['received_date'] or "")))
            self.table.setItem(i, 4, QtWidgets.QTableWidgetItem(obj['description'] or ""))

    def add_object(self):
        dialog = AddObjectDialog(self.db)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            self.load_objects()

    def add_result(self):
        row = self.table.currentRow()
        if row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите объект для внесения результата.")
            return
        dialog = AddResultDialog(self.db, self.user_id)
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            QMessageBox.information(self, "Успех", "Результат успешно добавлен.")

    def show_results(self):
        dialog = TestResultsDialog(self.db)
        dialog.exec_()