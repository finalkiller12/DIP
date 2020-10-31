import tkinter as tk
from PyQt5.QtCore import *
from pandastable import Table
from tkinter import filedialog
from PyQt5.QtWidgets import QMainWindow, QApplication
from Ui_MainWindow import Ui_MainWindow
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *
import datetime
import math


# import sys
# from PyQt5.QtCore import QProcess
# import numpy as np
# import csv
# from PIL import ImageTk, Image

class MainWindow():
    def __init__(self):
        self.lineEdit = QMainWindow()
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.Enter_Button.clicked.connect(self.showpage1)
        self.ui.pushButton.clicked.connect(self.showpage0)
        self.ui.Exit_Button.clicked.connect(self.Exit)
        self.ui.Exit2_butt.clicked.connect(self.Exit)

        self.ui.Load_Data.clicked.connect(self.getCSV)
        self.ui.Display_Graph_1.clicked.connect(self.Display_1)

        self.ui.calendarWidget.clicked[QDate].connect(self.show_Probabilty)

        self.ui.checkBox_1.stateChanged.connect(self.Uncheck23)
        self.ui.checkBox_2.stateChanged.connect(self.Uncheck13)
        self.ui.checkBox_3.stateChanged.connect(self.Uncheck12)

        # filepath = "python DataFile_db.py"
        # self.ui.Load_Data.clicked.connect(lambda checked, arg=filepath: self.execute(arg))

    def show(self):
        self.main_win.show()

    def loadTemperatureData(self):
        data = pd.read_csv('Overview200.csv')
        df = data.drop_duplicates(subset=['DeviceTimeStamp'])
        df2 = df.loc[df['OTI'] >= 200]
        # removed all non failure data points
        return df2

    def calcInterval(self, df2):
        # calculate interval between failure data points

        found = []
        i = 0
        for index, row in df2.iterrows():
            if i > 0:
                diff = datetime.datetime.strptime(df2.iloc[i].DeviceTimeStamp,
                                                  '%Y-%m-%dT%H:%M') - datetime.datetime.strptime(
                    df2.iloc[i - 1].DeviceTimeStamp, '%Y-%m-%dT%H:%M')

                # less than 1 sec apart = redundant rows
                if diff > datetime.timedelta(seconds=1):
                    found.append([i, diff, index, row.DeviceTimeStamp])
            i += 1

        # only count failures that happened > 1 day apart. multiple failures count as 1 incident
        time_list = []
        for a in found:
            if (a[1] > datetime.timedelta(days=1)):
                # print(a)
                time_list.append(a[1])

        interval = pd.Series(time_list).median().days
        return interval

    def poisson_probs(self, interval):

        pred_yst = 0
        prob_list = []
        for i in range(30):
            pred_today = 1 - pow(math.e, -1 / interval * i)
            prob_list.append(pred_today - pred_yst)
            pred_yst = pred_today

        return prob_list

    def show_Probabilty(self, date):
        df2 = self.loadTemperatureData()
        interval = self.calcInterval(df2)
        pred_probs = self.poisson_probs(interval)

        # assuming transformer failure just happened today :O
        td = QDate.currentDate()
        date_list = []
        # dont count day 0
        for i in range(0, len(pred_probs)):
            d = td.addDays(i)
            date_list.append(d)

        # index defaults to -1 if date is not in date_list
        try:
            dayIndex = date_list.index(date)  # get index of the date
        except:
            dayIndex = -1

        # dont show day 0 prob because its calculated at 0% lol
        if dayIndex > 0:  # date clicked has a probability to display
            self.ui.label_3.setText(date.toString() + ' - ' + str(round(pred_probs[dayIndex] * 100, 2)) + '%')
        else:  # date does not have a probability
            self.ui.label_3.setText(date.toString())

    def showpage0(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def showpage1(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def Exit(self):
        exit()

    def Uncheck23(self):
        if self.ui.checkBox_1.isChecked():
            if self.ui.checkBox_2.isChecked():
                self.ui.checkBox_2.setChecked(False)

            if self.ui.checkBox_3.isChecked():
                self.ui.checkBox_3.setChecked(False)

    def Uncheck13(self):
        if self.ui.checkBox_2.isChecked():
            if self.ui.checkBox_1.isChecked():
                self.ui.checkBox_1.setChecked(False)

            if self.ui.checkBox_3.isChecked():
                self.ui.checkBox_3.setChecked(False)

    def Uncheck12(self):
        if self.ui.checkBox_3.isChecked():
            if self.ui.checkBox_1.isChecked():
                self.ui.checkBox_1.setChecked(False)

            if self.ui.checkBox_2.isChecked():
                self.ui.checkBox_2.setChecked(False)

    def Display_1(self):
        data = pd.read_csv('mvlv-transformer.csv',
                           usecols=['active_power', 'current', 'voltage', 'active_power', 'reactive_power',
                                    'apparent_power'])
        f, axes = plt.subplots(1, 1, figsize=(8, 4))

        if self.ui.checkBox_1.isChecked():
            axes.set_xlabel("Sample Size")
            axes.set_ylabel("Voltage (V)")

            data.head(10000).plot(y=['voltage'], ax=axes)
            plt.show()

        elif self.ui.checkBox_2.isChecked():
            axes.set_xlabel("Sample Size")
            axes.set_ylabel("Current (A)")

            data.head(10000).plot(y=['current'], ax=axes)
            plt.show()

        elif self.ui.checkBox_3.isChecked():
            axes.set_xlabel("Sample Size")
            axes.set_ylabel("Power (W)")

            data.head(10000).plot(y=['active_power'], ax=axes)
            plt.show()

    def getCSV(self):
        root = tk.Tk()
        root.title('PandasTable')
        frame = tk.Frame(root)
        frame.pack(fill='both', expand=True)
        pt = Table(frame)
        pt.show()
        import_file_path = filedialog.askopenfilename()
        pt.importCSV(filename=import_file_path, dialog=True)
        root.mainloop()

    # def Enlarge_2(self):
    # = pd.read_csv('mvlv-transformer.csv',
    # usecols=['active_power', 'current', 'voltage', 'active_power', 'reactive_power',
    # 'apparent_power'])
    # f, axes = plt.subplots(1, 1, figsize=(8, 4))

    # if self.ui.checkBox_1.isChecked():
    # data.head(10000).plot(y=['active_power', 'reactive_power', 'apparent_power'], ax=axes)
    # plt.show()
    # if self.ui.checkBox_2.isChecked():
    # data.head(20000).plot(y=['current'], ax=axes)
    # plt.show()
    # if self.ui.checkBox_3.isChecked():
    # data.head(20000).plot(y=['voltage'], ax=axes)
    # plt.show()

    # def execute(self, filepath):
    # QProcess.startDetached(filepath)

    # def display_Power(self):
    # if self.ui.checkBox.isChecked():
    # if self.ui.checkBox_2.isChecked():
    # self.ui.checkBox_2.setChecked(False)

    # if self.ui.checkBox_3.isChecked():
    # self.ui.checkBox_3.setChecked(False)

    # self.ui.graphicsView_2.setStyleSheet("border-image: url(:/page 2/All 3 Power.jpeg);")
    # self.ui.graphicsView_3.setStyleSheet("border-image: url(:/page2.1/Active.jpeg);")
    # self.ui.checkBox.stateChanged.connect(self.Un_Display_pic)

    # def display_Current(self):
    # if self.ui.checkBox_2.isChecked():
    # if self.ui.checkBox.isChecked():
    # self.ui.checkBox.setChecked(False)

    # if self.ui.checkBox_3.isChecked():
    # self.ui.checkBox_3.setChecked(False)

    # self.ui.graphicsView_2.setStyleSheet("border-image: url(:/page 2.4/Current 20k.jpeg);")
    # self.ui.graphicsView_3.setStyleSheet("border-image: url(:/page 2.3/Current 10k.jpeg);")
    # self.ui.checkBox_2.stateChanged.connect(self.Un_Display_pic)

    # def display_Voltage(self):
    # if self.ui.checkBox_3.isChecked():
    # if self.ui.checkBox.isChecked():
    # self.ui.checkBox.setChecked(False)

    # if self.ui.checkBox_2.isChecked():
    # self.ui.checkBox_2.setChecked(False)

    # self.ui.graphicsView_2.setStyleSheet("border-image: url(:/page 2.6/Voltage 20k.jpeg);")
    # self.ui.graphicsView_3.setStyleSheet("border-image: url(:/page 2.5/Voltage 10k.jpeg);")
    # self.ui.checkBox_3.stateChanged.connect(self.Un_Display_pic)

    # def Un_Display_pic(self):
    # self.ui.graphicsView_3.setStyleSheet("background: ")
    # self.ui.graphicsView_2.setStyleSheet("background: ")
    # self.ui.checkBox.stateChanged.connect(self.display_Power)
    # self.ui.checkBox_2.stateChanged.connect(self.display_Current)
    # self.ui.checkBox_3.stateChanged.connect(self.display_Voltage)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
