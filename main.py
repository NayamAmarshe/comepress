from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import os
from pathlib import Path

import sys


class MyGUI(QMainWindow):
    def __init__(self):
        super(MyGUI, self).__init__()
        uic.loadUi("comepress.ui", self)
        # Remove Titlebar and background
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # Get button
        self.pushButton.clicked.connect(self.browse)
        self.setAcceptDrops(True)
        self.show()

    def browse(self):
        self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select Folder")
        print(self.folder_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        dropped_path = event.mimeData().text()[7:-2]
        if os.path.isdir(dropped_path):
            self.folder_path = dropped_path
        else:
            alert_dialog = QMessageBox.warning(
                self, "NOT A FOLDER", "Please drop a folder here, not a file.")

    def convert(self):
        for root, dirs, files in os.walk():
            for file in files:
                if file.endswith(".txt"):
                    print(os.path.join(root, file))


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec()


if __name__ == "__main__":
    main()
