import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtCore import QProcess

from DIP.Ui_MainWindow import Ui_MainWindow

class MainWindow():
    def __init__(self):
        self.lineEdit = QMainWindow()
        self.main_win = QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.main_win)

        self.ui.Enter_Button.clicked.connect(self.showpage1)
        self.ui.Next_butt.clicked.connect(self.showpage2)

        filepath = "python DataFile_db.py"
        self.ui.Load_Data.clicked.connect(lambda checked, arg=filepath: self.execute(arg))

        self.ui.Prev_butt.clicked.connect(self.showpage0)
        self.ui.pushButton.clicked.connect(self.showpage1)

        self.ui.Exit_Button.clicked.connect(self.Exit)
        self.ui.Exit2_butt.clicked.connect(self.Exit)

    def show(self):
        self.main_win.show()

    def showpage0(self):
        self.ui.stackedWidget.setCurrentIndex(0)

    def showpage1(self):
        self.ui.stackedWidget.setCurrentIndex(1)

    def showpage2(self):
        self.ui.stackedWidget.setCurrentIndex(2)

    def execute(self, filepath):
        QProcess.startDetached(filepath)

    def Exit(self):
        exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
