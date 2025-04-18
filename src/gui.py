import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton,
    QLabel, QMessageBox, QSpacerItem, QSizePolicy
)

from PyQt5.QtGui import QFont, QPalette, QColor, QIcon, QPixmap
from weather_api import get_weather, get_weather_forecast
from PyQt5.QtCore import Qt

API_KEY = "30dec169b35cd183df01398d269b2cf9"  


class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Погода")
        self.setFixedSize(550, 750) 
        self.setWindowIcon(QIcon("oblako.png"))

        

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#0A181C"))
        self.setPalette(palette)

        self.layout = QVBoxLayout()
        
        self.layout.setSpacing(15)

        self.logo_label = QLabel()
        self.logo_label.setPixmap(QPixmap("oblako.png").scaledToWidth(200, Qt.SmoothTransformation))
        self.logo_label.setAlignment(Qt.AlignCenter)


        self.title_label = QLabel("Предсказатель \n погоды по коленочкам")
        self.title_label.setFont(QFont("Arial", 25, QFont.Bold))
        self.title_label.setStyleSheet("color: #95C4D8; " )
        self.title_label.setAlignment(Qt.AlignCenter)

        
        self.layout.addWidget(self.logo_label)
        self.layout.addWidget(self.title_label)

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Введите город...")
        self.city_input.setFont(QFont("Arial", 12))
        self.city_input.setStyleSheet("padding: 8px; border-radius: 6px; border: 5px solid #3C2A71; color:DFEDF3; text-align: center;")
        # self.city_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.get_weather_button = QPushButton("Показать погоду")
        self.get_weather_button.setFont(QFont("Arial", 12))
        self.get_weather_button.setStyleSheet("""
            QPushButton {
                background-color: #95c4d8;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #1c6391;
            }
        """)
        self.get_weather_button.clicked.connect(self.show_weather)

        self.get_forecast_button = QPushButton("Прогноз на 3 дня")
        self.get_forecast_button.setFont(QFont("Arial", 12))
        self.get_forecast_button.setStyleSheet("""
            QPushButton {
                background-color: #3C2A71;
                color: white;
                padding: 10px;
                border: none;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #281C4B;
            }
            QPushButton:pressed {
                background-color: #20173C;
            }
        """)
        self.get_forecast_button.clicked.connect(self.show_forecast)

        self.result_label = QLabel("")
        self.result_label.setFont(QFont("Arial", 13))
        self.result_label.setStyleSheet("color: #34495e;")
        self.result_label.setWordWrap(True)
        self.result_label.setAlignment(Qt.AlignCenter)

        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.city_input)
        self.layout.addWidget(self.get_weather_button)
        self.layout.addWidget(self.get_forecast_button)
        self.layout.addWidget(self.result_label)
        self.layout.addSpacerItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        self.setLayout(self.layout)

    def show_weather(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Ошибка", "Введите название города.")
            return

        weather = get_weather(city, API_KEY)
        if weather:
            self.result_label.setText(
                f"🌍 {weather['city']}\n🌡 Температура: {weather['temperature']}°C\n☀️ {weather['description'].capitalize()}"
            )
            self.result_label.setStyleSheet("color: #DFEDF3;")
        else:
            self.result_label.setText("⚠️ Не удалось получить данные.")

    def show_forecast(self):
        city = self.city_input.text().strip()
        if not city:
            QMessageBox.warning(self, "Ошибка", "Введите название города.")
            return

        forecast = get_weather_forecast(city, API_KEY)
        if forecast:
            forecast_text = ""
            for day in forecast:
                forecast_text += f"\n{day['date']} - {day['temperature']}°C, {day['description'].capitalize()}"
            self.result_label.setText(forecast_text)
            self.result_label.setStyleSheet("color: #DFEDF3;")
        else:
            self.result_label.setText("⚠️ Не удалось получить прогноз.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = WeatherApp()
    window.show()
    sys.exit(app.exec_())
