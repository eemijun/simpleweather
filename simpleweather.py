import json
import requests
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5 import QtCore
from PyQt5.QtGui import QPixmap
import config  # to get API Key
import datetime
cities = []

from weather import Ui_SimpleWeather


def get_weather(city_info):
    weather_info_str = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={city_info["coord"]["lat"]}&lon={city_info["coord"]["lon"]}&units={"imperial"}&appid={config.app_id}')
    r = weather_info_str.json()


class MainWindow(QMainWindow, Ui_SimpleWeather):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        # self.threadpool = QThreadPool()

        app_id = config.app_id  # Open Weather API Key

        self.pushButton.clicked.connect(self.read_weather)
        self.lineEdit.returnPressed.connect(self.find_city)
        self.but_test1.clicked.connect(self.read_weather)
        self.comboBox.currentTextChanged.connect(self.select_city)
        self.comboBox.setLineEdit(self.lineEdit)

        self.show()

    def read_weather(self, weather_info):

        day_labels = [self.day_1, self.day_2 , self.day_3, self.day_4 , self.day_5,
                      self.day_6, self.day_7, self.day_8]
        count = 0

        self.city_title.setText("Weather in " + weather_info['name'])

        with open('sam_all.json', encoding="utf8") as f:
            r = json.load(f)
        # with open('sam_all.json', 'w') as f:
        #     json.dump(r, f)

        self.temp_num_lbl.setText(str(r['current']['temp']))
        self.temp_min_num_lbl.setText(str(datetime.datetime.fromtimestamp(
                    int(r['current']['sunrise'])
                ).strftime('%H:%M:%S')))  # change from Unix to readable
        self.temp_max_num_lbl.setText((datetime.datetime.fromtimestamp(
                    int(r['current']['sunset'])
                ).strftime('%H:%M:%S')))
        self.pre_num_lbl.setText((str(r['current']['pressure'])))
        self.hum_num_lbl.setText((str(r['current']['humidity'])))
        self.dec_num_lbl.setText((r['current']['weather'][0]['main']))
        self.lon_num_lbl.setText((str(r['lon'])))
        self.lat_num_lbl.setText((str(r['lat'])))
        self.tmz_num_lbl.setText(str(r['timezone']))
        self.alert_lbl.setText("Alert- " + str(r['alerts'][0]['event']))
        for days in r['daily']:
            label2 = QLabel(str(days['weather'][0]['main']))
            pixmap = QPixmap('icons_png\\13d@2x.png')
            self.gridLayout.addWidget(label2)
            label2.setPixmap(pixmap)
            label2.setAlignment(QtCore.Qt.AlignHCenter)

        for days in r['daily']:
            label = QLabel(str(days['temp']['day']) + "\n" + str(days['temp']['night']))
            self.gridLayout.addWidget(label)
            label.setAlignment(QtCore.Qt.AlignHCenter)
            day_labels[count].setText(str((datetime.datetime.fromtimestamp(
                    int(days['dt'])
                ).strftime('%m-%d'))))
            count += 1

        # datetime.datetime.fromtimestamp(
        #                  int(r['current']['sunrise'])
        #                 ).strftime('%Y-%m-%d %H:%M:%S'))

    def find_city(self):
        self.comboBox.clear()
        city = self.lineEdit.text()
        self.textEdit.append("Searching for " + city)  # for testing
        with open('cities_list.json', encoding="utf8") as f:
            r = json.load(f)
        for dict_city in r:
            if dict_city['name'] == city:
                self.comboBox.addItem(dict_city['name'] + ", " + dict_city['state'] + " " + dict_city['country'])
                cities.append(dict_city.copy())
                self.textEdit.append("adding to dict " + str(dict_city.copy()))

    def select_city(self, city):
        if len(cities) == 0:
            return
        else:
            self.textEdit.append("Selected " + str(city))  # for testing
            print(cities[self.comboBox.currentIndex()])
            self.read_weather(cities[self.comboBox.currentIndex()])


if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()