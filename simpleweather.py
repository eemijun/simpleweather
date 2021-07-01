import json
import requests
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import config  # to get API Key
import datetime
from weather import Ui_SimpleWeather
cities = []


def get_weather(city_info):
    weather_info_str = requests.get(f'https://api.openweathermap.org/data/2.5/onecall?lat={city_info["coord"]["lat"]}&lon={city_info["coord"]["lon"]}&units={"imperial"}&appid={config.app_id}')
    return weather_info_str.json()


class MainWindow(QMainWindow, Ui_SimpleWeather):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.setFixedSize(651, 685)

        # self.threadpool = QThreadPool()

        app_id = config.app_id  # Open Weather API Key

        self.pushButton.clicked.connect(self.read_weather)
        self.lineEdit.returnPressed.connect(self.find_city)
        self.but_test1.clicked.connect(self.read_weather)
        # self.comboBox.currentIndexChanged.connect(self.select_city)
        self.comboBox.setLineEdit(self.lineEdit)

        self.show()

    def read_weather(self):
        weather_info = cities[self.comboBox.currentIndex()]
        r = get_weather(weather_info)
        day_labels = [self.day_1, self.day_2, self.day_3, self.day_4, self.day_5,
                      self.day_6, self.day_7, self.day_8]
        day_imgs = [self.day_1_img, self.day_2_img, self.day_3_img, self.day_4_img, self.day_5_img,
                      self.day_6_img, self.day_7_img, self.day_8_img]
        day_infos = [self.day_1_info, self.day_2_info, self.day_3_info, self.day_4_info, self.day_5_info,
                    self.day_6_info, self.day_7_info, self.day_8_info]
        count = 0

        self.city_title.setText("Weather in " + weather_info['name'])

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
        if 'alerts' in r:
            self.alert_lbl.setText("Alert- " + str(r['alerts'][0]['event']))
        else:
            self.alert_lbl.setText("Alerts - ")

        for days in r['daily']:
            day_labels[count].setText(str((datetime.datetime.fromtimestamp(
                    int(days['dt'])
                ).strftime('%m-%d'))))
            day_infos[count].setText(str(int(days['temp']['day'])) + "\n" + str(int(days['temp']['night'])))
            if days['weather'][0]['id'] <= 232:
                pixmap = QPixmap('icons_png\\11d@2x.png')
            elif 300 <= days['weather'][0]['id'] <= 321:
                pixmap = QPixmap('icons_png\\09d@2x.png')
            elif 500 <= days['weather'][0]['id'] <= 531:
                pixmap = QPixmap('icons_png\\10d@2x.png')
            elif 600 <= days['weather'][0]['id'] <= 622:
                pixmap = QPixmap('icons_png\\13d@2x.png')
            elif 701 <= days['weather'][0]['id'] <= 781:
                pixmap = QPixmap('icons_png\\50d@2x.png')
            elif days['weather'][0]['id'] == 800:
                pixmap = QPixmap('icons_png\\01d@2x.png')
            elif 801 <= days['weather'][0]['id'] <= 804:
                pixmap = QPixmap('icons_png\\04d@2x.png')
            day_imgs[count].setPixmap(pixmap)
            count += 1
        self.find_city()  # Fix issue where second city input gave blank value

    def find_city(self):
        cities.clear()
        self.comboBox.clear()
        city = self.lineEdit.text()
        print("city __ " + self.lineEdit.text())
        self.textEdit.append("Searching for " + city)  # for testing
        with open('cities_list.json', encoding="utf8") as f:
            r = json.load(f)
        for dict_city in r:
            if dict_city['name'] == city:
                self.comboBox.addItem(dict_city['name'] + ", " + dict_city['state'] + " " + dict_city['country'])
                cities.append(dict_city.copy())
                self.textEdit.append("adding to dict " + str(dict_city.copy()))

    # def select_city(self, city):
    #     if len(cities) == 0:
    #         return
    #     else:
    #         self.textEdit.append("Selected " + str(city))  # for testing
    #         print(cities[self.comboBox.currentIndex()])


if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()