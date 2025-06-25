from PyQt5 import QtWidgets, QtCore

class TestResultsDialog(QtWidgets.QDialog):
    def __init__(self, db_connection):
        super().__init__()
        self.db = db_connection
        self.setWindowTitle("Результаты испытаний")
        self.resize(1100, 400)

        layout = QtWidgets.QVBoxLayout()
        self.table = QtWidgets.QTableWidget()
        layout.addWidget(self.table)

        self.setLayout(layout)
        self.load_results()

    def load_results(self):
        cursor = self.db.cursor

        cursor.execute('SELECT * FROM test_results')
        results = cursor.fetchall()
        headers = ["ID", "Объект", "Дата", "Параметры", "Результат", "Эксперт"]
        self.table.setColumnCount(len(headers))
        self.table.setHorizontalHeaderLabels(headers)
        self.table.setRowCount(len(results))

        for row_idx, row in enumerate(results):
            self.table.setItem(row_idx, 0, QtWidgets.QTableWidgetItem(str(row["result_id"])))
            self.table.setItem(row_idx, 1, QtWidgets.QTableWidgetItem(str(row["object_id"])))
            self.table.setItem(row_idx, 2, QtWidgets.QTableWidgetItem(str(row["test_date"])))
            self.table.setItem(row_idx, 3, QtWidgets.QTableWidgetItem(row["parameters"]))
            self.table.setItem(row_idx, 4, QtWidgets.QTableWidgetItem(row["result"]))
            self.table.setItem(row_idx, 5, QtWidgets.QTableWidgetItem(str(row["expert_id"])))

        self.table.resizeColumnsToContents()
        self.table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
