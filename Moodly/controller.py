from PyQt5.QtWidgets import QApplication
import PyQt5.QtCore
from . import view
import os
import sys
from PyQt5 import QtGui
from .logic import *
from .style import *
from .resource import *


def main():

    app=QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont(":/fonts/Raleway.ttf")
    qssApply(app)

    obj=Configure()
    obj.getConfig()

    w=view.mainWindow(obj)
    sys.exit(app.exec_())


def qssApply(app):
    app.setStyleSheet(qss)
