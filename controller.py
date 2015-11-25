from PyQt5.QtWidgets import QApplication
import PyQt5.QtCore
import view
import sys
from PyQt5 import QtGui
from logic import *
from style import *
from resource import *


def main():

    app=QApplication(sys.argv)

    QtGui.QFontDatabase.addApplicationFont(":/fonts/Raleway.ttf")   #add custom fonts

    qssApply(app)

    if config_check() == False:
        obj=Configure()

    else :
        obj=Configure()
        obj.getConfig()



    w=view.mainWindow(obj)

    sys.exit(app.exec_())



def config_check():                             #Check whether the sqlite file exists or not(returns True or False)
    fname=os.getcwd()+ '\moodly.sqlite'
    return(os.path.isfile(fname))



def qssApply(app):                              #Load and Apply custom stylesheet(external)
    #ssFile="moodly.stylesheet"
    #with open(ssFile,"r") as fh:
    #app.setStyleSheet(fh.read())
    app.setStyleSheet(qss)


if __name__=="__main__":
    main()
