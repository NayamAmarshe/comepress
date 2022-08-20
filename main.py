import fnmatch
import os
import shutil
import sys
from os.path import isdir, join

from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import *


bundle_dir = getattr(
    sys, '_MEIPASS', os.path.abspath(os.path.dirname(__file__)))


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


def include_patterns(*patterns):
    def _ignore_patterns(path, all_names):
        # Determine names which match one or more patterns (that shouldn't be
        # ignored).
        keep = (name for pattern in patterns
                for name in fnmatch.filter(all_names, pattern))
        # Ignore file names which *didn't* match any of the patterns given that
        # aren't directory names.
        dir_names = (name for name in all_names if isdir(join(path, name)))
        return set(all_names) - set(keep) - set(dir_names)

    return _ignore_patterns


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
        uic.loadUi(os.path.abspath(
            os.path.join(bundle_dir, "res/comepress.ui")), self)

        # Remove Titlebar and background
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setStyleSheet("""QToolTip { 
                           border: none; 
                           color: white; 
                           }""")
        self.setWindowIcon(QtGui.QIcon("res/inbox_tray_3d.ico"))
        # BUTTONS
        self.pushButton.clicked.connect(self.browse)

        self.checkBox.clicked.connect(self.checked)
        self.checkBox.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.closeButton.clicked.connect(self.close)
        self.closeButton.setToolTip("Close")
        self.closeButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.minimizeButton.clicked.connect(self.showMinimized)
        self.minimizeButton.setToolTip("Minimize")
        self.minimizeButton.setCursor(QCursor(QtCore.Qt.PointingHandCursor))

        self.setAcceptDrops(True)

        # DEFAULT VARIABLES
        self.backup = True
        self.dragPos = QtCore.QPoint()

        self.show()

    def mousePressEvent(self, event):
        self.dragPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.move(self.pos() + event.globalPos() - self.dragPos)
            self.dragPos = event.globalPos()
            event.accept()

    def checked(self):
        if self.checkBox.isChecked():
            self.backup = True
        else:
            self.backup = False

    def browse(self):
        folder_path = QtWidgets.QFileDialog.getExistingDirectory(
            self, "Select a Folder")
        if folder_path == '':
            return
        self.comepress_folder(folder_path)
        alert_dialog = QMessageBox.information(
            self, "All good!", "Successfully comepressed all files/folders")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        allowed_types = ["image/jpeg", "image/jpg",
                         "image/png", "inode/directory"]
        dropped_files_folders = []
        db = QtCore.QMimeDatabase()

        for url in event.mimeData().urls():
            mimetype = db.mimeTypeForUrl(url)
            if mimetype.name() in allowed_types:
                dropped_files_folders.append(
                    tuple([url.toLocalFile(), mimetype.name()]))

        for file_folder_path in dropped_files_folders:
            if file_folder_path[1] == "inode/directory":
                self.comepress_folder(file_folder_path[0])

            else:
                self.comepress_file(file_folder_path[0])
        alert_dialog = QMessageBox.information(
            self, "All good!", "Successfully comepressed all files/folders")

    def comepress_folder(self, folder_path):
        # Get parent folder path
        parent_folder = os.path.abspath(
            os.path.join(folder_path, os.pardir))
        # Get folder name
        folder_name = os.path.basename(folder_path)
        # Destination backup
        if os.path.isdir(folder_path + "_COMEPRESS"):
            shutil.rmtree(folder_path + "_COMEPRESS")
        backup_destination = os.path.abspath(
            folder_path + "_COMEPRESS")
        # Backup folder
        print(f"backup: {self.backup}")
        if self.backup:
            shutil.copytree(folder_path, backup_destination,
                            ignore=include_patterns("*.png", "*.jpg", "*.jpeg"))

        # Loop through all the files in the folder
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                # If file is an image
                if file.endswith(tuple([".jpg", ".jpeg", ".png"])):
                    # Convert to WebP
                    try:
                        img = Image.open(root + "/" + file)
                        img.save(root + "/" + file.rsplit(".", 1)
                                 [0] + ".webp", "webp")
                        # Remove original file
                        os.remove(root + "/" + file)
                    except:
                        alert_dialog = QMessageBox.information(
                            self, "Error!", "Please check if " + root + "/" + file + " is not corrupt")
                        return

    def comepress_file(self, file_path):
        # GET DETAILS
        parent_folder = os.path.abspath(
            os.path.join(file_path, os.pardir))
        file_name = os.path.basename(file_path)
        destination_path = parent_folder + "/ORIGINAL_" + file_name
        # BACKUP
        if self.backup:
            shutil.copyfile(file_path, destination_path)
        # CONVERT
        try:
            img = Image.open(parent_folder + "/" + file_name)
            img.save(parent_folder + "/" +
                     file_name.rsplit(".", 1)[0] + ".webp", "webp")
            os.remove(parent_folder + "/" + file_name)
        except:
            alert_dialog = QMessageBox.information(
                self, "Error!", "Please check if " + parent_folder + "/" + file_name + " is not corrupt")
            return


def main():
    app = QApplication([])
    app.setWindowIcon(QtGui.QIcon("res/inbox_tray_3d.ico"))
    window = MyGUI()
    app.exec()


if __name__ == "__main__":
    main()
