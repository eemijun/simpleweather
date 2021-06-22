# import simpleweather
# import weather
# from PyQt5 import QtWidgets, QtCore
#
#
# class MyFileBrowser(weather.Ui_SimpleWeather, QtWidgets.QMainWindow):
#
#     resized = QtCore.pyqtSignal('PyQt_PyObject')
#
#     def __init__(self):
#         super(MyFileBrowser, self).__init__()
#         self.setupUi(self)
#         self.setWindowTitle("Duplicate File Finder")
#
#         self.deleted_files = list()
#
#     def set_duplicate_finder(self, dfToSet):
#         self.df = dfToSet