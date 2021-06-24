import json

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import config  #to get API Key

from weather import Ui_SimpleWeather


class MainWindow(QMainWindow, Ui_SimpleWeather):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        #self.threadpool = QThreadPool()

        app_id = config.app_id #Open Weather API Key

        self.pushButton.clicked.connect(self.read_weather)

        self.show()

    def read_weather(self):
        with open('sam_data.json', encoding="utf8") as f:
            r = json.load(f)
        self.temp_num_lbl.setText(str(r['main']['temp']))
        self.temp_min_num_lbl.setText(str(r['main']['temp_min']))
        self.temp_max_num_lbl.setText((str(r['main']['temp_max'])))
        self.pre_num_lbl.setText((str(r['main']['pressure'])))
        self.hum_num_lbl.setText((str(r['main']['humidity'])))
        self.dec_num_lbl.setText((r['weather'][0]['main']))
        self.lon_num_lbl.setText((str(r['coord']['lon'])))
        self.lat_num_lbl.setText((str(r['coord']['lat'])))
        self.tmz_num_lbl.setText((str(r['timezone'])))
        self.lineEdit.setText(r['name'])

    def find_city(self):
        with open('sam_data.json', encoding="utf8") as f:
             r = json.load(f)
        self.textEdit.setText(json.dumps(r, indent=4))

        # with open('cities.json', encoding="utf8") as f:
        #     r = json.load(f)
        # for i in range(12):
        #     self.textEdit.append(r[i]['country'])


if __name__ == '__main__':

    app = QApplication([])
    window = MainWindow()
    app.exec_()