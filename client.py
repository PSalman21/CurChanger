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
