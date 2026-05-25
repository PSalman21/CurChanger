import sys
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt

API_URL = "http://127.0.0.1:8000"

class CurrencyConverter(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Конвертер валют")
        self.setFixedSize(400, 300)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        self.amount_input = QLineEdit()
        self.amount_input.setPlaceholderText("Введите сумму")
        layout.addWidget(self.amount_input)
        
        self.from_combo = QComboBox()
        self.from_combo.addItems(["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])
        layout.addWidget(self.from_combo)
        
        self.to_combo = QComboBox()
        self.to_combo.addItems(["USD", "EUR", "RUB", "GBP", "JPY", "CNY"])
        layout.addWidget(self.to_combo)
        
        self.convert_btn = QPushButton("Конвертировать")
        self.convert_btn.clicked.connect(self.convert)
        layout.addWidget(self.convert_btn)
        
        self.result_label = QLabel("Результат появится здесь")
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        self.status_label = QLabel("Статус: Готов")
        self.status_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.status_label)

        self.check_server()
    
    def check_server(self):
        try:
            response = requests.get(f"{API_URL}/", timeout=2)
            self.status_label.setText("Статус: Подключен")
        except:
            self.status_label.setText("Статус: Сервер не запущен")
            self.convert_btn.setEnabled(False)

    def convert(self):
        try:
            amount = float(self.amount_input.text())
            if amount <= 0:
                QMessageBox.warning(self, "Ошибка", "Сумма должна быть положительной")
                return
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверная сумма")
            return
        
        try:
            response = requests.post(f"{API_URL}/convert", json={
                "from_currency": self.from_combo.currentText(),
                "to_currency": self.to_combo.currentText(),
                "amount": amount
            })
            
            if response.status_code == 200:
                data = response.json()
                self.result_label.setText(
                    f"{data['amount']} {data['from_currency']} = "
                    f"{data['converted_amount']} {data['to_currency']}\n"
                    f"Курс: 1 {data['from_currency']} = {data['rate']} {data['to_currency']}"
                )
            else:
                error = response.json().get("detail", "Неизвестная ошибка")
                QMessageBox.warning(self, "Ошибка", error)
                
        except requests.ConnectionError:
            QMessageBox.critical(self, "Ошибка", "Нет соединения с сервером")
        
