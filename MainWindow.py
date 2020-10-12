import tkinter as tk
from pandastable import Table
from tkinter import filedialog
from PyQt5.QtWidgets import QMainWindow, QApplication
from DIP.Ui_MainWindow import Ui_MainWindow
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import *

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
        self.ui.Next_butt.clicked.connect(self.showpage2)

        self.ui.checkBox.stateChanged.connect(self.display_Power)
        self.ui.checkBox_2.stateChanged.connect(self.display_Current)
        self.ui.checkBox_3.stateChanged.connect(self.display_Voltage)

        self.ui.Load_Data.clicked.connect(self.getCSV)
        self.ui.Enlarge_Graph_1.clicked.connect(self.Enlarge_1)
        self.ui.Enlarge_Graph_2.clicked.connect(self.Enlarge_2)

        self.ui.Prev_butt.clicked.connect(self.showpage0)
        self.ui.pushButton.clicked.connect(self.showpage1)

        self.ui.Exit_Button.clicked.connect(self.Exit)
        self.ui.Exit2_butt.clicked.connect(self.Exit)

        # filepath = "python DataFile_db.py"
        # self.ui.Load_Data.clicked.connect(lambda checked, arg=filepath: self.execute(arg))
    def show(self):
        self.main_win.show()

    def showpage0(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def showpage1(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def showpage2(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    # def execute(self, filepath):
    # QProcess.startDetached(filepath)

    def display_Power(self):
        if self.ui.checkBox.isChecked():
            if self.ui.checkBox_2.isChecked():
                self.ui.checkBox_2.setChecked(False)

            if self.ui.checkBox_3.isChecked():
                self.ui.checkBox_3.setChecked(False)

        self.ui.graphicsView_2.setStyleSheet("border-image: url(:/page 2/All 3 Power.jpeg);")
        self.ui.graphicsView_3.setStyleSheet("border-image: url(:/page2.1/Active.jpeg);")
        #self.ui.checkBox.stateChanged.connect(self.Un_Display_pic)

    def display_Current(self):
        if self.ui.checkBox_2.isChecked():
            if self.ui.checkBox.isChecked():
                self.ui.checkBox.setChecked(False)

            if self.ui.checkBox_3.isChecked():
                self.ui.checkBox_3.setChecked(False)

        self.ui.graphicsView_2.setStyleSheet("border-image: url(:/page 2.3/Current 10k.jpeg);")
        self.ui.graphicsView_3.setStyleSheet("border-image: url(:/page 2.4/Current 20k.jpeg);")
        #self.ui.checkBox_2.stateChanged.connect(self.Un_Display_pic)

    def display_Voltage(self):
        if self.ui.checkBox_3.isChecked():
            if self.ui.checkBox.isChecked():
                self.ui.checkBox.setChecked(False)

            if self.ui.checkBox_2.isChecked():
                self.ui.checkBox_2.setChecked(False)

        self.ui.graphicsView_2.setStyleSheet("border-image: url(:/page 2.6/Voltage 20k.jpeg);")
        self.ui.graphicsView_3.setStyleSheet("border-image: url(:/page 2.5/Voltage 10k.jpeg);")
        #self.ui.checkBox_3.stateChanged.connect(self.Un_Display_pic)

    #def Un_Display_pic(self):
        #self.ui.graphicsView_3.setStyleSheet("background: ")
        #self.ui.graphicsView_2.setStyleSheet("background: ")
        #self.ui.checkBox.stateChanged.connect(self.display_Power)
        #self.ui.checkBox_2.stateChanged.connect(self.display_Current)
        #self.ui.checkBox_3.stateChanged.connect(self.display_Voltage)

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

    def Exit(self):
        exit()

    # create a button for this
    def Enlarge_1(self):
        data = pd.read_csv('mvlv-transformer.csv',
                           usecols=['active_power', 'current', 'voltage', 'active_power', 'reactive_power',
                                    'apparent_power'])
        f, axes = plt.subplots(1, 1, figsize=(8, 4))

        if self.ui.checkBox.isChecked():
            data.head(10000).plot(y=['active_power'], ax=axes)
            plt.show()

        if self.ui.checkBox_2.isChecked():
            data.head(10000).plot(y=['current'], ax=axes)
            plt.show()

        if self.ui.checkBox_3.isChecked():
            data.head(10000).plot(y=['voltage'], ax=axes)
            plt.show()

    def Enlarge_2(self):
        data = pd.read_csv('mvlv-transformer.csv',
                           usecols=['active_power', 'current', 'voltage', 'active_power', 'reactive_power',
                                    'apparent_power'])
        f, axes = plt.subplots(1, 1, figsize=(8, 4))

        if self.ui.checkBox.isChecked():
            data.head(10000).plot(y=['active_power', 'reactive_power', 'apparent_power'], ax=axes)
            plt.show()
        if self.ui.checkBox_2.isChecked():
            data.head(20000).plot(y=['current'], ax=axes)
            plt.show()
        if self.ui.checkBox_3.isChecked():
            data.head(20000).plot(y=['voltage'], ax=axes)
            plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
