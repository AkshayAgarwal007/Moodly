from PyQt5.QtWidgets import QApplication
import PyQt5.QtCore
from . import view
import sys
from PyQt5 import QtGui
from .logic import *
from .style import *
from .resource import *


def main():

    app=QApplication(sys.argv)
    QtGui.QFontDatabase.addApplicationFont(":/fonts/Raleway.ttf")
    qssApply(app)

    if config_check() == False:
        obj=Configure()

    else :
        obj=Configure()
        obj.getConfig()

    w=view.mainWindow(obj)
    sys.exit(app.exec_())


def config_check():
    fname=os.path.join(os.path.dirname(__file__), 'moodly.sqlite')
    return(os.path.isfile(fname))


def qssApply(app):
    app.setStyleSheet(qss)
