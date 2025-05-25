# -*- coding: UTF-8 -*-
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog
from PyQt6.QtCore import QDir, QStandardPaths
from PyQt6.QtGui import QAction, QIcon
import pandas as pd
from CandleView import CandleView
import sys

QDir.addSearchPath('images', './images/')


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dataWindow = CandleView()
        self.setCentralWidget(self.dataWindow)

        self.createMenuAndToolBar()

        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

        self.setMinimumSize(800, 600)
        self.setWindowTitle("CandleView")

    def createMenuAndToolBar(self):
        fileOpenAction = self.createAction("&Open", self.open, "Ctrl+O",
                                           "fileopen", "Open data file")
        fileQuitAction = self.createAction("&Quit", self.close,
                                           "Ctrl+Q", "filequit",
                                           "Close the application")

        fileMenu = self.menuBar().addMenu("&File")
        self.addActions(fileMenu, (fileOpenAction, fileQuitAction))

    def createAction(self, text, slot=None, shortcut=None, icon=None,
                     tip=None, checkable=False, signal="triggered"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon("images:/%s.png" % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            getattr(action, signal).connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def addActions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def open(self):
        data_file, _ = QFileDialog.getOpenFileName(self, 'Open File Dialog', QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.DocumentsLocation), 'Comma-Separated Value Files (*.csv);;All Files (*)')
        if data_file:
            df = pd.read_csv(data_file)
            df.loc[:, 'date'] = pd.to_datetime(df['date'])
            self.dataWindow.update_datas(df)
            self.setWindowTitle(data_file)


def main():
    app = QApplication(sys.argv)
    app.setApplicationName("CandleView")
    form = MainWindow()
    form.showMaximized()
    app.exec()


if __name__ == "__main__":
    main()
