import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5 import uic
import os
from pathlib import Path
import shutil
from PIL import Image


mode = "folder"  # or "folder"


def ignore_list(path, files):

    filesToIgnore = []

    for fileName in files:

        fullFileName = os.path.join(os.path.normpath(path), fileName)

        if (not os.path.isdir(fullFileName)
            and not fileName.endswith('jpg')
            and not fileName.endswith('jpeg')
            and not fileName.endswith('png')
                and not fileName.endswith('mp4')):
            filesToIgnore.append(fileName)

    return filesToIgnore


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
        if mode == "files":
            self.file_paths = QtWidgets.QFileDialog.getOpenFileNames(
                self, "Select Files")[0]
            print(self.file_paths)
        else:
            self.folder_path = QtWidgets.QFileDialog.getExistingDirectory(
                self, "Select a Folder")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if mode == "files":
            dropped_path = event.mimeData().text()
            lines = []
            db = QtCore.QMimeDatabase()
            for url in event.mimeData().urls():
                mimetype = db.mimeTypeForUrl(url)
                if(mimetype.name() not in ["image/jpeg", "image/jpg", "image/png"]):
                    alert_dialog = QMessageBox.warning(
                        self, "Nope!", "You didn't drop a valid image file!")
                    return
                lines.append(url.toLocalFile())
                self.comepress()
            self.file_paths = lines
            print(self.file_paths)
        else:
            dropped_path = event.mimeData().text()[7:-2]
            print(dropped_path)
            self.folder_path = dropped_path
            self.comepress()

    def comepress(self):
        # Get parent folder path
        self.parent_folder = os.path.abspath(
            os.path.join(self.folder_path, os.pardir))
        # Get folder name
        self.folder_name = os.path.basename(self.folder_path)
        # Destination backup
        backup_destination = os.path.abspath(self.folder_path + "_backup")
        # Backup folder
        shutil.copytree(self.folder_path, backup_destination,
                        ignore=ignore_list)


def main():
    app = QApplication([])
    window = MyGUI()
    app.exec()


if __name__ == "__main__":
    main()
