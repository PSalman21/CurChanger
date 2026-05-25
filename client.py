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
