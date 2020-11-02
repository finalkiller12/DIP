import sys
from PyQt5.QtCore import Qt, QRectF, QDate, QPoint
from PyQt5.QtGui import QPainter, QColor, QFont
from PyQt5.QtWidgets import QCalendarWidget, QApplication


class CalendarWidget(QCalendarWidget):

    def paintCell(self, painter, rect, date):
        painter.setRenderHint(QPainter.Antialiasing, True)
        self.events = {
            QDate(2020, 10, 24),
            QDate(2020, 10, 15),
            QDate(2020, 11, 3)
        }

        if date in self.events:
            painter.save()
            painter.setBrush(Qt.yellow)
            painter.drawRect(rect)
            painter.setPen(Qt.blue)

            painter.drawText(QRectF(rect), Qt.TextSingleLine | Qt.AlignCenter, str(date.day()))

        else:
            QCalendarWidget.paintCell(self, painter, rect, date)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = CalendarWidget()
    w.show()
    sys.exit(app.exec_())

# from DIP.Calendar import CalendarWidget

# self.calendarWidget = CalendarWidget(self.page_2)
# self.calendarWidget.setGeometry(QtCore.QRect(9, 9, 1181, 451))
# self.calendarWidget.setGridVisible(True)
# self.calendarWidget.setObjectName("calendarWidget")

# from tkinter import *
# from PIL import ImageTk,Image
# import matplotlib.pyplot as plt
# import numpy as np

# root = Tk()
# root.title('Codemy.com - Learn to code!')
# root.geometry('400x200')

# def graph():
#    house_prices = np.random.normal(200000, 25000, 5000)
#    plt.hist(house_prices, 50)
#    plt.show()

# my_button = Button(root, text = "Graph it!" , command = graph)
# my_button.pack()

# root.mainloop()

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'New_stacked.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!
