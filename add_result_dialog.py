from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox

class AddResultDialog(QtWidgets.QDialog):
    def __init__(self, db, user_id):
        super().__init__()
        self.db = db
        self.user_id = user_id

        self.setWindowTitle("Добавить результат испытания")
        layout = QtWidgets.QFormLayout()

        # Комбобокс объектов
        self.object_combo = QtWidgets.QComboBox()
        self.objects = []
        self.load_objects()
        layout.addRow("Объект испытания:", self.object_combo)

        # Комбобокс объектов экспертов
        self.expert_combo = QtWidgets.QComboBox()
        self.experts = []
        self.load_experts()
        layout.addRow("Эксперт:", self.expert_combo)

        # Остальные поля
        self.date_input = QtWidgets.QDateEdit(QtCore.QDate.currentDate())
        self.date_input.setCalendarPopup(True)
        self.params_input = QtWidgets.QTextEdit()
        self.result_input = QtWidgets.QTextEdit()

        layout.addRow("Дата испытания:", self.date_input)
        layout.addRow("Параметры:", self.params_input)
        layout.addRow("Результат:", self.result_input)

        btns = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        layout.addRow(btns)
        self.setLayout(layout)

        btns.accepted.connect(self.save)
        btns.rejected.connect(self.reject)

    # Загрузка объектов
    def load_objects(self):
        cursor = self.db.cursor
        cursor.execute("SELECT object_id, name FROM test_objects")
        self.objects = cursor.fetchall()

        for obj in self.objects:
            self.object_combo.addItem(obj['name'], obj['object_id'])

    # Загрузка списка эксмпертов
    def load_experts(self):
        cursor = self.db.cursor
        cursor.execute("SELECT user_id, name, surname, patronymic FROM users WHERE role = 'expert'")
        self.experts = cursor.fetchall()

        for expert in self.experts:
            self.expert_combo.addItem(f'{expert['name']} {expert['surname']} {expert['patronymic']}', expert['user_id'])

    # Сохранение объектов
    def save(self):
        object_id = self.object_combo.currentData()
        test_date = self.date_input.date().toString("yyyy-MM-dd")
        parameters = self.params_input.toPlainText().strip()
        result = self.result_input.toPlainText().strip()
        expert_id = self.expert_combo.currentData()

        if not object_id or not parameters or not result:
            QMessageBox.warning(self, "Ошибка", "Заполните все поля.")
            return

        cursor = self.db.cursor
        cursor.execute("""
            INSERT INTO test_results (object_id, test_date, parameters, result, expert_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (object_id, test_date, parameters, result, expert_id))
        self.db.commit()
        self.accept()
