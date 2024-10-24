import sys
import requests
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QComboBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.dates import DateFormatter
from datetime import datetime

class WeatherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.city_label = QLabel("Enter City name: ", self)
        self.city_input = QLineEdit(self)
        self.get_weather_button = QPushButton("Get Weather", self)
        self.temperature_label = QLabel(self)
        self.emoji_label = QLabel(self)
        self.description_label = QLabel(self)
        self.dark_mode_button = QPushButton("Toggle Dark Mode", self)
        self.unit_selector = QComboBox(self)  # Add unit selector
        self.is_dark_mode = False  # Track dark mode state

        # Matplotlib Figure for the weather chart
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Weather App")

        vbox = QVBoxLayout()

        # Adding options for temperature units
        self.unit_selector.addItems(["Celsius", "Fahrenheit", "Kelvin"])
        self.unit_selector.setCurrentIndex(0)  # Default to Celsius

        vbox.addWidget(self.city_label)
        vbox.addWidget(self.city_input)
        vbox.addWidget(self.unit_selector)  # Add unit selector to the layout
        vbox.addWidget(self.get_weather_button)
        vbox.addWidget(self.temperature_label)
        vbox.addWidget(self.emoji_label)
        vbox.addWidget(self.description_label)
        vbox.addWidget(self.canvas)  # Add Matplotlib canvas for weather chart
        vbox.addWidget(self.dark_mode_button)

        self.setLayout(vbox)

        self.city_label.setAlignment(Qt.AlignCenter)
        self.city_input.setAlignment(Qt.AlignCenter)
        self.temperature_label.setAlignment(Qt.AlignCenter)
        self.emoji_label.setAlignment(Qt.AlignCenter)
        self.description_label.setAlignment(Qt.AlignCenter)

        self.city_label.setObjectName("city_label")
        self.city_input.setObjectName("city_input")
        self.get_weather_button.setObjectName("get_weather_button")
        self.temperature_label.setObjectName("temperature_label")
        self.emoji_label.setObjectName("emoji_label")
        self.description_label.setObjectName("description_label")
        self.dark_mode_button.setObjectName("dark_mode_button")

        self.setStyleSheet("""
            QLabel, QPushButton{
               font-family: calibri;
            }  
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 20px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """)

        # Connect buttons to their respective functions
        self.get_weather_button.clicked.connect(self.get_weather)
        self.dark_mode_button.clicked.connect(self.toggle_dark_mode)

    def get_weather(self):
        Api_Key = "4ab5db0f85437e8f79c305f95c7e896f"
        city = self.city_input.text()
        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={Api_Key}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            if data['cod'] == 200:
                self.display_weather(data)
                self.plot_weather_chart(city, Api_Key)  # Plot the weather chart

        except requests.exceptions.RequestException as req_error:
            self.display_error(f"Request Error:\n{req_error}")

    def display_weather(self, data):
        self.temperature_label.setStyleSheet("font-size: 75px")
        temp_kelvin = data["main"]["temp"]

        # Convert temperature based on the selected unit
        selected_unit = self.unit_selector.currentText()
        if selected_unit == "Celsius":
            temp = temp_kelvin - 273.15
            temp_str = f"{temp: .1f}ºC"
        elif selected_unit == "Fahrenheit":
            temp = (temp_kelvin - 273.15) * 9/5 + 32
            temp_str = f"{temp: .1f}ºF"
        else:
            temp_str = f"{temp_kelvin: .1f}K"

        weather_icon = data["weather"][0]["icon"]
        icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
        self.set_weather_icon(icon_url)

        weather_conditions = data["weather"][0]["description"]
        self.temperature_label.setText(temp_str)
        self.description_label.setText(weather_conditions)

    def set_weather_icon(self, icon_url):
        image = QPixmap()
        image.loadFromData(requests.get(icon_url).content)
        self.emoji_label.setPixmap(image)

    def display_error(self, message):
        self.temperature_label.setStyleSheet("font-size: 30px")
        self.temperature_label.setText(message)
        self.emoji_label.clear()
        self.description_label.clear()

    def toggle_dark_mode(self):
        common_styles = """
            QLabel, QPushButton{
                font-family: calibri;
            }  
            QLabel#city_label{
                font-size: 40px;
                font-style: italic;
            }
            QLineEdit#city_input{
                font-size: 20px;
            }
            QPushButton#get_weather_button{
                font-size: 30px;
                font-weight: bold;
            }
            QLabel#temperature_label{
                font-size: 75px;
            }
            QLabel#emoji_label{
                font-size: 100px;
            }
            QLabel#description_label{
                font-size: 50px;
            }
        """
        
        if not self.is_dark_mode:
            # Apply dark mode styles
            self.setStyleSheet(f"""
                {common_styles}
                QWidget {{
                    background-color: #2c2c2c;
                    color: white;
                }}
                QPushButton {{
                    background-color: #444444;
                    color: white;
                }}
                QLabel#city_label, QLineEdit#city_input, QLabel#temperature_label, QLabel#emoji_label, QLabel#description_label {{
                    color: white;
                }}
            """)
            self.dark_mode_button.setText("Toggle Light Mode")
            self.is_dark_mode = True
        else:
            # Revert to light mode
            self.setStyleSheet(f"""
                {common_styles}
                QWidget {{
                    background-color: white;
                    color: black;
                }}
                QPushButton {{
                    background-color: #f0f0f0;
                    color: black;
                }}
                QLabel#city_label, QLineEdit#city_input, QLabel#temperature_label, QLabel#emoji_label, QLabel#description_label {{
                    color: black;
                }}
            """)
            self.dark_mode_button.setText("Toggle Dark Mode")
            self.is_dark_mode = False

    def plot_weather_chart(self, city, api_key):
        """Fetch hourly weather data and plot a temperature chart."""
        url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&appid={api_key}"
        response = requests.get(url)
        data = response.json()

        if data["cod"] == "200":
            hours = []
            temperatures = []

            for item in data["list"][:8]:  # Plot the next 8 hours
                dt = datetime.strptime(item["dt_txt"], "%Y-%m-%d %H:%M:%S")
                hours.append(dt)  # Convert to datetime objects
                temp_kelvin = item["main"]["temp"]
                temp_celsius = temp_kelvin - 273.15
                temperatures.append(temp_celsius)

            # Clear the previous plot
            self.figure.clear()

            # Create the plot
            ax = self.figure.add_subplot(111)
            ax.plot(hours, temperatures, marker='o')
            ax.set_xlabel('Date and Time')
            ax.set_ylabel('Temperature (°C)')
            ax.set_title(f'8-Hour Temperature Forecast for {city}')

            # Format the x-axis to show date and 12-hour time (with AM/PM)
            ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d %I:%M %p'))
            ax.tick_params(axis='x', rotation=45)

            self.figure.tight_layout()
            # Refresh the canvas
            self.canvas.draw()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()
    sys.exit(app.exec())
