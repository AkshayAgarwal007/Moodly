from PyQt5.QtWidgets import (QMainWindow, QLineEdit, QComboBox, QCheckBox, QLabel,QWidget, QPushButton, QMessageBox,
			     QDesktopWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QProgressBar, QFrame, QTabWidget,
			     QScrollArea,QAction, qApp,QStatusBar,QFileDialog,QSystemTrayIcon, QMenu,QApplication)
from PyQt5.QtGui import QIcon, QPixmap,QImage
from PyQt5.QtCore import QBasicTimer,QTimer,pyqtSignal
from PyQt5 import QtCore
from PyQt5.QtCore import QEvent
import time
import datetime
from PyQt5 import QtGui
from PyQt5.QtGui import QClipboard
from .resource import*
from functools import partial
import os
from .logic import Notify
import re
from .models import *
import sys
import subprocess
import pygame



class mainWindow(QMainWindow):

	def __init__(self,obj):
		super().__init__()
		self.setObjectName('Window1')
		self.obj=obj
		self.set=0
		self.initUI()

	def initUI(self):
		self.resize(820,500)
		self.setWindowTitle('Moodly 1.0 Alpha - Configure')
		self.setWindowIcon(QIcon(':/Assets/moodly.gif'))
		self.setFixedSize(820,500)
		self.center()

		self.sysTray=QWidget()
		self.tray = SystemTrayIcon(QIcon(':/Assets/moodly.gif'),self.sysTray)
		self.tray.show()
		self.tray.trigger.connect(self.showApp)
		self.tray.qtrigger.connect(self.closeApp)
		self.tray.uptrigger.connect(self.updateNow)
		self.setWidget()

		self.show()


	def setWidget(self):
		if self.obj.configured==0:
			self.setCentralWidget(configureWidget(self))
		elif self.obj.configured==1:
			self.setCentralWidget(setupWidget(self))
		elif self.obj.configured==2:
			self.setStyleSheet('''#Window1{background-color: light gray;}''')
			self.setWindowTitle('Moodly 1.0 Alpha')
			self.setMenuBar()
			self.tabWidget = tabWidget(self)
			self.setCentralWidget(self.tabWidget)

			self.tray.updateAction.setEnabled(True)
			self.statusBar = QStatusBar()
			self.setStatusBar(self.statusBar)
			self.statusBar.hide()
			self.statusLbl1 = QLabel()
			self.statusLbl2 = QLabel()
			self.statusLbl2.setAlignment(QtCore.Qt.AlignRight)

			self.statusBar.addWidget(self.statusLbl1)
			self.statusBar.addWidget(self.statusLbl2,QtCore.Qt.AlignRight)

			self.updateTimer()
			self.notifTimer()
			self.i_thread = {}
			self.nt=0


	def showApp(self):
		if self.isMinimized():
			self.showNormal()

		self.show()
		self.activateWindow()

	def closeApp(self):
		self.tray.hide()
		qApp.quit()


	def showStatus(self,msg,id_):
		if id_ == 0:
			self.statusLbl1.setText(msg)
		else:
			self.statusLbl2.setText(msg)

		self.statusBar.show()


	def hideStatus(self,id_):
		if id_==0:
			self.statusLbl1.setText('')
		else:
			self.statusLbl2.setText('')

		if self.statusLbl1.text() == '' and self.statusLbl2.text()=='':
			self.statusBar.hide()


	def updateTimer(self):
		self.current_timer = QTimer()
		delay = int(re.findall(r'\d+', self.obj.upIntval)[0])
		delay = delay*60*60*1000
		self.current_timer.timeout.connect(self.updater)
		self.current_timer.setSingleShot(True)
		if self.set==0:
			self.updater()
		else:
			self.current_timer.start(delay)


	def notifTimer(self):
		if self.obj.nIntval=="Turn Off":
			self.notifier = False
		else:
			delay = int(re.findall(r'\d+', self.obj.nIntval)[0])*60*60
			self.timer1 = QTimer()
			self.timer1.timeout.connect(partial(self.quickNotify))
			self.timer1.setSingleShot(True)
			self.timer1.start(10*60*1000)
			self.notifier= True


	def quickNotify(self):
		if self.obj.n !=0 and self.obj.updating==False:
			str_ = str(self.obj.n)
			self.tray.display_notify("Moodly","You have %s unread notifications"%str_,1)
		self.notifTimer()


	def quickStatus(self,i):
		if self.obj.updating==False:
			if 	i==0:
				self.showStatus('Next Update Scheduled at %s'%str(self.obj.scheduled))
				self.timer2 = QTimer()
				self.timer2.timeout.connect(partial(self.quickStatus,1))
				self.timer2.setSingleShot(True)
				self.timer2.start(6000)

			elif i==1:
				delay = int(re.findall(r'\d+', self.obj.upIntval)[0])*60*60
				self.showStatus('Last Update Scheduled at %s'%str(self.obj.scheduled-datetime.timedelta(0,delay))+'Failed')
				self.timer2 = QTimer()
				self.timer2.timeout.connect(partial(self.quickStatus,2))
				self.timer2.setSingleShot(True)
				self.timer2.start(6000)

			else:
				self.showStatus('Last Successful Update ')
				self.timer2 = QTimer()
				self.timer2.timeout.connect(self.hideStatus)
				self.timer2.setSingleShot(True)
				self.timer2.start(6000)
				self.statusTimer()


	def updater(self):
		self.obj.updating = True
		self.showStatus('Updating Moodly.....',0)
		self.thread=updateThread(self.obj)
		self.thread.finished.connect(self.tabUpdater)
		self.thread.start()


	def closeEvent(self, event):
		self.hide()
		event.ignore()
		self.tray.display_notify('Moodly','Moodly running in notification tray.',1)

	def center(self):
		qr = self.frameGeometry()
		cp = QDesktopWidget().availableGeometry().center()
		qr.moveCenter(cp)
		self.move(qr.topLeft())

	def setMenuBar(self):
		exitAction = QAction(QIcon(':/Assets/close.png'), '&Exit', self)
		exitAction.setShortcut('Ctrl+Q')
		exitAction.triggered.connect(self.closeApp)

		self.alreadyOpen = 0

		configAction = QAction(QIcon(':/Assets/setting.png'), '&Configure', self)
		configAction.triggered.connect(self.changeConfig)
		configAction.setShortcut('Ctrl+Shift+C')

		updateAction = QAction(QIcon(':/Assets/sync.png'), '&Update Now', self)
		updateAction.triggered.connect(self.updateNow)
		updateAction.setShortcut('Ctrl+U')

		menubar = self.menuBar()
		fileMenu = menubar.addMenu('&File')
		fileMenu.addAction(configAction)
		fileMenu.addAction(updateAction)
		fileMenu.addAction(exitAction)

	def updateNow(self):
		if self.obj.updating==False:
			self.current_timer.stop()
			self.current_timer.deleteLater()
			self.updater()

		else:
			pygame.init()
			pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'sounds/message.wav'))
			pygame.mixer.music.play()
			reply = QMessageBox.question(self,'Moodly',"An update is already in progress. ", QMessageBox.Ok)
			if reply == QMessageBox.Ok:
				pass


	def changeConfig(self):
		if self.alreadyOpen is 0:
			self.tab = reConfigureWidget(self.tabWidget)
			self.tabWidget.addTab(self.tab,QIcon(':/Assets/setting.png'),'Configure')
			self.tabWidget.setTabToolTip(self.tabWidget.indexOf(self.tab),'Configure')
			self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tab))
			self.alreadyOpen=1
		else:
			self.tabWidget.setCurrentIndex(self.tabWidget.indexOf(self.tab))


	def verify(self):
		self.obj.saveConfig(1)
		self.thread=WorkThread(self.obj)
		self.thread.finished.connect(self.notify)
		self.thread.start()
		self.set=1
		self.setWidget()


	def notify(self):
		self.setWidget()
		self.tray.display_notify("Moodly",self.obj.status_msg[0],self.obj.status_msg[1])


	def tabUpdater(self):
		self.set=1
		self.tabWidget.tab1.updater()
		self.tabWidget.tab2.updater()
		for tab in self.tabWidget.tab:
			tab.updater()
		self.obj.updating = False
		self.c_timer = QTimer()
		self.c_timer.timeout.connect(partial(self.hideStatus,0))
		self.c_timer.setSingleShot(True)
		self.showStatus('Update Completed',0)
		self.c_timer.start(5000)
		self.tray.display_notify("Moodly",self.obj.status_msg[0],self.obj.status_msg[1])
		self.updateTimer()

	def itemsWriter(self,fileName,id1,id2):
		nt=self.getIndex()
		self.i_thread[nt] = itemsWriterThread(fileName,id1,id2,nt,self.obj)
		self.i_thread[nt].finished.connect(partial(self.del_i_thread,self.i_thread[nt].id3))
		self.i_thread[nt].start()


	def del_i_thread(self,id3):
		self.i_thread[id3]=0


	def getIndex(self):
		if self.nt==0:
			return self.nt
		else:
			for i in range(0,self.nt):
				if self.i_thread[i]==0:
					return i
			self.nt+=1
			return self.nt


	def configWriter(self,text1,text2,combo1,combo2):
		self.sid3=self.showStatus('Configuring...',1)
		self.c_thread = configWriterThread(self.obj,text1,text2,combo1,combo2)
		self.c_thread.finished.connect(self.reConfigModify)
		self.c_thread.start()


	def reConfigModify(self):
		if self.alreadyOpen==1:
				self.tab.status_label.setText(self.obj.config_status)
		self.tray.display_notify("Moodly",self.obj.status_msg[0],self.obj.status_msg[1])
		self.re_timer = QTimer()
		self.re_timer.timeout.connect(partial(self.hideStatus,1))
		self.re_timer.setSingleShot(True)
		self.showStatus(self.obj.config_status,1)
		self.re_timer.start(5000)

		self.tabWidget.updating = False

		if self.obj.intValChanged ==0:
			self.current_timer.stop()
			self.current_timer.deleteLater()
			self.updateTimer()
			self.obj.intValChanged = -1

		elif self.obj.intValChanged ==1:
			if self.notifier == True:
				self.timer1.stop()
				self.timer1.deleteLater()
			self.notifTimer()
			self.obj.intValChanged = -1

		elif self.obj.intValChanged ==2:
			self.current_timer.stop()
			self.current_timer.deleteLater()
			self.updateTimer()

			if self.notifier == True:
				self.timer1.stop()
				self.timer1.deleteLater()
			self.notifTimer()

			self.obj.intValChanged = -1


class configureWidget(QWidget):
	def __init__(self,parent_):
		super(configureWidget,self).__init__(parent_)
		self.parent_=parent_
		self.obj=parent_.obj
		self.initUI()

	def initUI(self):
		self.qle1 = QLineEdit(self)
		self.qle1.setObjectName("qle")
		self.qle1.setPlaceholderText("Enter Your Moodle Username")
		self.qle2 = QLineEdit(self)
		self.qle2.setEchoMode(QLineEdit.Password)
		self.qle2.setObjectName("qle")
		self.qle2.setPlaceholderText("Enter Your Moodle Password")

		lbltxt = ['Username', 'Password', 'Keep Notifying', 'Update Interval' ]
		lbl=[]
		self.status_label = QLabel(self)
		self.status_label.setObjectName('slbl')
		self.status_label.setText(self.obj.config_status)
		for i in range(0,len(lbltxt)):
			lbl.append(QLabel(self))
			lbl[i].setText(lbltxt[i])
			lbl[i].setObjectName("lbl")

		self.combo = QComboBox(self)
		self.combo.setObjectName("combo")

		self.combo2 = QComboBox(self)
		self.combo2.setObjectName("combo")

		for i1 in range(1,7):
			self.combo.addItem(str(i1)+" hrs")

		self.combo2.addItem("Turn Off")

		for i4 in range(1,9):
			self.combo2.addItem(str(i4*5)+" mins")

		btn=QPushButton("Configure")
		btn.setObjectName("btn")
		btn.clicked.connect(self.callRetrieve)

		grid = QGridLayout()

		for i2 in range(0,len(lbl)):
			grid.addWidget(lbl[i2],i2+1 , 0)

		grid.addWidget(self.qle1,1,1)

		grid.addWidget(self.qle2,2,1)

		grid.addWidget(self.combo2,3,1)

		grid.addWidget(self.combo,4,1)

		grid.addWidget(btn, 5,0)
		grid.addWidget(self.status_label,5,1)

		grid.setHorizontalSpacing(50)
		grid.setVerticalSpacing(0)
		grid.setContentsMargins(150, 40, 150, 0)

		self.setLayout(grid)


	def keyPressEvent(self,event):
		if event.key() == QtCore.Qt.Key_Return:

			self.callRetrieve()



	def callRetrieve(self):
		self.obj.saveUserData(str(self.qle1.text()),
						  str(self.qle2.text()),str(self.combo2.currentText()),str(self.combo.currentText()))

		self.parent_.verify()


class reConfigureWidget(QWidget):
	def __init__(self,parent_):
		super(reConfigureWidget,self).__init__(parent_)
		self.parent_=parent_
		self.obj=parent_.obj
		self.initUI()

	def initUI(self):
		self.qle1 = QLineEdit(self)
		self.qle1.setObjectName("qle")
		self.qle1.setText(self.obj.uname)
		self.qle1.setReadOnly(True)

		self.qle2 = QLineEdit(self)
		self.qle2.setEchoMode(QLineEdit.Password)
		self.qle2.setObjectName("qle")
		self.qle2.setText(self.obj.passwd)

		self.updating=False

		lbltxt = ['Username', 'Password', 'Keep Notifying', 'Update Interval' ]
		lbl=[]
		self.status_label = QLabel(self)
		self.status_label.setObjectName('slbl')

		self.obj.config_status =''

		self.status_label.setText('')
		for i in range(0,len(lbltxt)):
			lbl.append(QLabel(self))
			lbl[i].setText(lbltxt[i])
			lbl[i].setObjectName("lbl")

		self.combo = QComboBox(self)
		self.combo.setObjectName("combo")

		self.combo2 = QComboBox(self)
		self.combo2.setObjectName("combo")


		for i1 in range(1,7):
			self.combo.addItem(str(i1)+" hrs")

		index = self.combo.findText(self.obj.upIntval,QtCore.Qt.MatchExactly)

		self.combo.setCurrentIndex(index)

		self.combo2.addItem("Turn Off")

		for i4 in range(1,9):
			self.combo2.addItem(str(i4*5)+" mins")

		index1 = self.combo2.findText(self.obj.nIntval,QtCore.Qt.MatchExactly)


		self.combo2.setCurrentIndex(index1)

		btn1=QPushButton("Save")
		btn1.setObjectName("btn")
		btn1.clicked.connect(self.callValidate)

		btn2=QPushButton("Cancel")
		btn2.setObjectName("gbtn")
		btn2.clicked.connect(self.closeConfig)

		grid = QGridLayout()

		for i2 in range(0,len(lbl)):
			grid.addWidget(lbl[i2],i2+1 , 0)

		grid.addWidget(self.qle1,1,1)
		grid.addWidget(self.qle2,2,1)
		grid.addWidget(self.combo2,3,1)
		grid.addWidget(self.combo,4,1)
		grid.addWidget(btn1, 5,0)
		grid.addWidget(btn2, 5,1)
		grid.setHorizontalSpacing(70)
		grid.setVerticalSpacing(40)
		grid.setContentsMargins(160, 35, 150, 0)

		hbox1 = QHBoxLayout()
		hbox1.addLayout(grid)
		self.hbox2 = QHBoxLayout()
		self.hbox2.setContentsMargins(160,0,0,0)
		self.hbox2.setSpacing(0)
		self.hbox2.addWidget(self.status_label)

		vbox = QVBoxLayout()
		vbox.setContentsMargins(0,30,0,0)
		vbox.setSpacing(0)
		vbox.addLayout(hbox1)
		vbox.addLayout(self.hbox2)

		self.widget = QWidget()
		self.widget.setLayout(vbox)
		self.widget.setObjectName('CWidget')
		self.widget.setStyleSheet('#CWidget{background-color: rgb(255, 250, 175);}')

		self.scroll = QScrollArea(self)
		self.scroll.setWidget(self.widget)
		self.scroll.setWidgetResizable(True)
		self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)

		vbox1 = QVBoxLayout()
		vbox1.setContentsMargins(0,0,0,0)
		vbox1.setSpacing(0)
		vbox1.addWidget(self.scroll)
		self.setLayout(vbox1)


	def callValidate(self):
		if self.obj.updating == True:
			pygame.init()
			pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'sounds/message.wav'))
			pygame.mixer.music.play()
			reply = QMessageBox.question(self,'Moodly',"An update is in progress. Kindly wait. ", QMessageBox.Ok)

			if reply == QMessageBox.Ok:
				pass
		else:
			self.parent_.updating = True
			self.parent_.parent_.configWriter(str(self.qle1.text()),
							  str(self.qle2.text()),str(self.combo2.currentText()),str(self.combo.currentText()))



	def closeConfig(self):
		self.parent_.removeTab(self.parent_.indexOf(self))
		self.parent_.parent_.alreadyOpen = 0


class setupWidget(QWidget):

	def __init__(self,parent_):
		super(setupWidget,self).__init__(parent_)
		self.parent_=parent_
		self.initUI()

	def initUI(self):
		self.pbar = QProgressBar(self)
		self.pbar.setObjectName('pbar')
		self.pbar.setTextVisible(True)
		self.pbar.setFormat('Configuring...')

		self.timer = QBasicTimer()
		self.step = 0

		pixmap=QPixmap(':/Assets/moodly.gif')
		lbl=QLabel(self)
		lbl.setPixmap(pixmap)

		hbox1=QHBoxLayout()
		hbox1.addStretch(1)
		hbox1.addWidget(lbl)
		hbox1.addStretch(1)

		hbox2=QHBoxLayout()
		hbox2.addStretch(1)
		hbox2.addWidget(self.pbar)
		hbox2.addStretch(1)

		vbox=QVBoxLayout()
		vbox.addStretch(8)
		vbox.addLayout(hbox1)
		vbox.addStretch(1)
		vbox.addLayout(hbox2)
		vbox.addStretch(8)

		self.setLayout(vbox)
		self.callTimer()

	def timerEvent(self,e):
		if self.step>=100:
			self.step=0
		self.step=self.step+1
		self.pbar.setValue(self.step)

	def callTimer(self):
		 self.timer.start(100, self)


class tabWidget(QTabWidget):

	def __init__(self,parent_):
		super(tabWidget,self).__init__(parent_)
		self.parent_=parent_
		self.obj=parent_.obj
		self.initUI()

	def initUI(self):
		self.tab = []
		self.marker = 0
		self.updating = False

		self.tab1=courseTab(self)
		self.addTab(self.tab1,QIcon(':/Assets/course.png'),'My Courses')
		self.setTabToolTip(self.indexOf(self.tab1),'My Courses')

		self.tab2=notifyTab(self)
		self.addTab(self.tab2,QIcon(':/Assets/notif.png'),'Notifications')
		self.setTabToolTip(self.indexOf(self.tab2),'Notifications')

		self.currentChanged.connect(self.onChange)
		self.tab2.installEventFilter(self)

	def eventFilter(self,object,event):
		if event.type() == QEvent.MouseButtonPress:
			self.onActive()
			return True
		return False

	def onChange(self,i):
		if self.obj.notif[0].seen==0 and i==self.indexOf(self.tab2):
			self.nc_thread = notifySeenThread(self.obj)
			self.nc_thread.start()

	def onActive(self):
		if self.obj.notif[0].seen==0 and self.currentIndex() == self.indexOf(self.tab2):
			self.nc_thread = notifySeenThread(self.obj)
			self.nc_thread.start()


	def shortenTabName(self,cname):
		list1 =[]
		for i, ch in enumerate(cname):
				list1.append(ch)
				if len(list1)==12:
					if list1[i]== ' ':
						list1.pop(i)
					list1.append('..')
					break
		return ''.join(list1)


	def callItemTab(self,id_):
		if self.marker ==0:
			self.tab.append(itemTab(self,id_))
			cname = self.shortenTabName(self.obj.courses[id_].c_name)
			self.addTab(self.tab[self.marker],QIcon(':/Assets/course.png'),cname)
			self.setCurrentIndex(self.indexOf(self.tab[self.marker]))
			self.setTabToolTip(self.indexOf(self.tab[self.marker]),self.obj.courses[id_].c_name)
			self.marker+=1
		else:
			for tab in self.tab:
				if tab.id_ == id_:
					self.setCurrentIndex(self.indexOf(tab))
					return
			self.tab.append(itemTab(self,id_))
			cname = self.shortenTabName(self.obj.courses[id_].c_name)
			self.addTab(self.tab[self.marker],QIcon(':/Assets/course.png'),cname)
			self.setTabToolTip(self.indexOf(self.tab[self.marker]),self.obj.courses[id_].c_name)
			self.setCurrentIndex(self.indexOf(self.tab[self.marker]))
			self.marker+=1

	def closeItemTab(self,id_):
		for index, tab in enumerate(self.tab):
			if tab.id_ == id_:
				self.removeTab(self.indexOf(tab))
				self.tab.pop(index)
				self.marker = self.marker-1
				if self.marker==0:
					self.setCurrentIndex(self.indexOf(self.tab1))
				else:
					self.setCurrentIndex(self.indexOf(self.tab[self.marker-1]))
				break


class courseTab(QWidget):
	def __init__(self,parent_):
		super(courseTab,self).__init__(parent_)
		self.parent_=parent_
		self.obj=parent_.obj
		self.initUI()

	def initUI(self):
		self.btn = []
		self.lbl = []
		self.cFrames =[]
		self.marker=0
		self.d_=False

		if len(self.obj.courses) is 0:
			self.lbl.append(QLabel(self))
			self.lbl[self.marker].setText('Your credentials have been verified but we couldn\'t configure you up. Wait for auto-update')
			self.lbl[self.marker].setObjectName("slbl")
			self.cFrames.append(errorFrame(self.lbl[self.marker]))

		for i1 in range(self.marker,len(self.obj.courses)):
			self.lbl.append(QLabel(self))
			self.lbl[i1].setText(self.obj.courses[i1].c_name.upper())
			self.lbl[i1].setObjectName("lbl")
			self.btn.append(QPushButton('FILES'))
			self.btn[i1].setObjectName("btn")
			self.btn[i1].id=i1
			self.btn[i1].clicked.connect(partial(self.createItemTab,self.btn[i1].id))


		for i2 in range(self.marker,len(self.obj.courses)):
			self.cFrames.append(courseFrames(self.lbl[i2],self.btn[i2]))

		self.marker=len(self.obj.courses)

		self.widget = QWidget(self)

		self.vbox = QVBoxLayout()
		self.vbox.setContentsMargins(0,0,0,0)
		self.vbox.setSpacing(3)

		for index, frame in enumerate(self.cFrames):
			if index%2==0:
				frame.setObjectName('cFrameEven')
			else:
				frame.setObjectName('cFrameOdd')
			self.vbox.addWidget(frame)

		if len(self.cFrames)<4:
			self.dframe = QFrame()
			self.dframe.setObjectName('nFrameDummy')
			self.vbox.addWidget(self.dframe)
			self.d_=True

		self.widget.setLayout(self.vbox)

		self.scroll = QScrollArea(self)


		self.scroll.setWidget(self.widget)
		self.scroll.setWidgetResizable(True)
		self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

		vbox1 = QVBoxLayout()
		vbox1.setContentsMargins(0,0,0,0)
		vbox1.setSpacing(0)

		vbox1.addWidget(self.scroll)
		self.setLayout(vbox1)

	def createItemTab(self,id_):
		self.parent_.callItemTab(id_)

	def updater(self):
		if self.obj.dummy_courses is '':
			return
		else:
			if  self.d_==True:
				child = self.vbox.takeAt(len(self.cFrames))
				if child.widget() is not None:
					child.widget().deleteLater()
				elif child.layout() is not None:
					clearLayout(child.layout())
				self.dframe.deleteLater()

				self.d_=False

			if self.marker==0:
				self.cFrames[0].deleteLater()
				self.lbl[0].deleteLater()
				child = self.vbox.takeAt(0)
				if child.widget() is not None:
					child.widget().deleteLater()
				elif child.layout() is not None:
					clearLayout(child.layout())
				self.lbl.pop(0)
				self.cFrames.pop(0)

			for i1 in range(self.marker,len(self.obj.courses)):
				self.lbl.append(QLabel(self))
				self.lbl[i1].setText(self.obj.courses[i1].c_name.upper())
				self.lbl[i1].setObjectName("lbl")
				self.btn.append(QPushButton('FILES'))
				self.btn[i1].setObjectName("btn")
				self.btn[i1].id=i1
				self.btn[i1].clicked.connect(partial(self.createItemTab,self.btn[i1].id))


			for i2 in range(self.marker,len(self.obj.courses)):
				self.cFrames.append(courseFrames(self.lbl[i2],self.btn[i2]))

			for i3 in range (self.marker,len(self.cFrames)):
				if i3%2==0:
					self.cFrames[i3].setObjectName('cFrameEven')
				else:
					self.cFrames[i3].setObjectName('cFrameEven')

				self.vbox.addWidget(self.cFrames[i3])

			if len(self.cFrames)<4:
				self.dframe = QFrame()
				self.dframe.setObjectName('nFrameDummy')
				self.vbox.addWidget(self.dframe)
				self.d_=True

			self.marker=self.marker+len(self.obj.dummy_courses)


class notifyTab(QWidget):

	def __init__(self,parent_):
		super(notifyTab,self).__init__(parent_)
		self.parent_=parent_
		self.obj=parent_.obj
		self.initUI()

	def initUI(self):
		self.btn = []
		self.notif_lbl = []
		self.tag_lbl = []
		self.nFrames =[]
		self.d_ = False

		for i in range(0,len(self.obj.notif)):
			pixmap=QPixmap(self.obj.tagDict[self.obj.notif[i].tag])
			pixmap = pixmap.scaled(50, 50)
			self.tag_lbl.append(QLabel(self))
			self.tag_lbl[i].setPixmap(pixmap)

		for i1 in range(0,len(self.obj.notif)):
			self.notif_lbl.append(QLabel(self))
			self.notif_lbl[i1].setScaledContents(False)
			self.notif_lbl[i1].setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
			self.notif_lbl[i1].setText(self.obj.notif[i1].notif_text)
			self.notif_lbl[i1].setObjectName("nlbl")
			self.btn.append(QPushButton('Get Link'))
			self.btn[i1].setObjectName("btn")

		for i2 in range(0,len(self.obj.notif)):
			self.nFrames.append(notifyFrames(self.notif_lbl[i2],self.tag_lbl[i2],self.btn[i2]))
			tag = self.obj.notif[i2].tag
			if tag ==2 or tag==3 or tag==4:
				self.nFrames[i2].setObjectName('nFrameOdd')
			else:
				self.nFrames[i2].setObjectName('nFrameEven')

		self.widget = QWidget(self)
		self.vbox = QVBoxLayout()

		for index, frame in enumerate(self.nFrames):
			self.vbox.addWidget(frame)

		if len(self.nFrames)<4:
			self.dframe = QFrame()
			self.dframe.setObjectName('nFrameDummy')
			self.vbox.addWidget(self.dframe)
			self.d_ = True

		self.vbox.setContentsMargins(0,0,0,0)
		self.vbox.setSpacing(3)

		self.widget.setLayout(self.vbox)
		self.scroll = QScrollArea(self)
		self.scroll.setWidget(self.widget)
		self.scroll.setWidgetResizable(True)
		self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

		vbox1 = QVBoxLayout()
		vbox1.setContentsMargins(0,0,0,0)
		vbox1.setSpacing(0)

		vbox1.addWidget(self.scroll)
		self.setLayout(vbox1)


	def updater(self):
		marker=len(self.nFrames)
		marker1 = len(self.nFrames)

		for i in range(0,len(self.obj.notif)):
			pixmap=QPixmap(self.obj.tagDict[self.obj.notif[i].tag])
			pixmap = pixmap.scaled(50, 50)
			self.tag_lbl.append(QLabel(self))
			self.tag_lbl[marker].setPixmap(pixmap)
			marker=marker+1

		marker=marker1
		for i1 in range(0,len(self.obj.notif)):
			self.notif_lbl.append(QLabel(self))
			self.notif_lbl[marker].setScaledContents(False)
			self.notif_lbl[marker].setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
			self.notif_lbl[marker].setText(self.obj.notif[i1].notif_text)
			self.notif_lbl[marker].setObjectName("nlbl")
			self.btn.append(QPushButton('Get Link'))
			self.btn[marker].setObjectName("btn")
			marker+=1

		marker=marker1

		for i2 in range(0,len(self.obj.notif)):
			self.nFrames.append(notifyFrames(self.notif_lbl[marker],self.tag_lbl[marker],self.btn[marker]))
			marker+=1

		marker=marker1

		for i3 in range(len(self.nFrames)-1,marker-1,-1):
			self.vbox.insertWidget(0,self.nFrames[i3])
			tag = self.obj.notif[i3-marker].tag
			if tag ==2 or tag==3 or tag==4:
				self.nFrames[i3].setObjectName('nFrameOdd')
				self.nFrames[i3].setStyleSheet(' #nFrameOdd{background-color:#F5F5DC;min-height:110px;max-height:110px;min-width:805px;}')
			else:
				self.nFrames[i3].setObjectName('nFrameEven')
				self.nFrames[i3].setStyleSheet(' #nFrameEven{background-color: rgb(255, 250, 175);min-height:110px;max-height:110px;min-width:805px;}')

		if len(self.nFrames)>=4 and self.d_==True:
			child = self.vbox.takeAt(len(self.nFrames))
			if child.widget() is not None:
				child.widget().deleteLater()
			elif child.layout() is not None:
				clearLayout(child.layout())
			self.dframe.deleteLater()
			self.d_=False

class notifyFrames(QFrame):

	def __init__(self,lbl1,lbl2,btn):
		super().__init__()
		self.initUI(lbl1,lbl2,btn)


	def initUI(self,lbl1,lbl2,btn):
		grid = QGridLayout()
		grid.addWidget(lbl2,1,0)
		grid.addWidget(lbl1,1,0)
		grid.setContentsMargins(70,0,70,0)
		self.setLayout(grid)

class courseFrames(QFrame):

	def __init__(self,lbl,btn):
		super().__init__()
		self.initUI(lbl,btn)

	def initUI(self,lbl,btn):
		grid = QGridLayout()
		grid.addWidget(lbl,1,0)
		grid.addWidget(btn,1,1)
		grid.setContentsMargins(70,0,70,0)
		grid.setSpacing(0)
		self.setLayout(grid)


class itemTab(QWidget):

	def __init__(self,parent_,id_):
		super(itemTab,self).__init__(parent_)
		self.parent_=parent_
		self.obj = parent_.obj
		self.id_=id_
		self.initUI()

	def initUI(self):
		self.obtn = {}
		self.sbtn = {}
		self.lbl = []
		self.gbtn = []
		self.iFrames =[]
		self.d_ =False

		self.x = 0
		self.y=0

		self.backBtn = QPushButton(QIcon(':/Assets/close2.png'),'Close')
		self.backBtn.setObjectName('backBtn')
		self.backBtn.clicked.connect(partial(self.parent_.closeItemTab,self.id_))
		self.clbl = QLabel(self)
		self.clbl.setText(self.obj.courses[self.id_].c_name.upper())
		self.clbl.setObjectName('hlbl')

		for i1 in range(0,len(self.obj.courses[self.id_].items)):
			self.lbl.append(ExtendedQLabel(self,i1))
			cname = self.shortenTabName(self.obj.courses[self.id_].items[i1].i_name)
			self.lbl[i1].setText(cname)
			self.lbl[i1].setObjectName("lbl")

			self.sbtn[i1] = QPushButton('Save')
			self.sbtn[i1].setObjectName("sbtn")

			self.gbtn.append(QPushButton(QIcon(':/Assets/link.png'),''))
			self.gbtn[i1].setObjectName("linkBtn")
			self.gbtn[i1].id_ = i1
			self.gbtn[i1].clicked.connect(partial(self.copyLink,self.gbtn[i1].id_))
			self.sbtn[i1].clicked.connect(partial(self.saveItem,self.gbtn[i1].id_))

			if self.obj.courses[self.id_].items[i1].saved==1:
				self.obtn[i1] = QPushButton('Open')
				self.obtn[i1].setObjectName("obtn")
				self.obtn[i1].clicked.connect(partial(self.openItem,self.gbtn[i1].id_))

		self.iFrames.append(topFrame(self.backBtn,self.clbl))

		for i2 in range(0,len(self.obj.courses[self.id_].items)):
			if self.obj.courses[self.id_].items[i2].saved==1:
				self.iFrames.append(itemFrames(self.lbl[i2],self.gbtn[i2],self.sbtn[i2],self.obtn[i2]))
			elif self.obj.courses[self.id_].items[i2].saved==0:
				self.iFrames.append(itemFramesNew(self.lbl[i2],self.gbtn[i2],self.sbtn[i2]))
			else:
				self.iFrames.append(itemFramesForum(self.lbl[i2],self.gbtn[i2]))

		self.widget = QWidget(self)

		self.vbox = QVBoxLayout()
		self.vbox.setSpacing(3)

		for index, frame in enumerate(self.iFrames):
			if index%2==0:
				frame.setObjectName('nFrameEven')
			else:
				frame.setObjectName('nFrameEven')
			self.vbox.addWidget(frame)

		self.vbox.setContentsMargins(0,0,0,0)

		if len(self.iFrames)<4:
			self.dframe = QFrame()
			self.dframe.setObjectName('nFrameDummy')
			self.vbox.addWidget(self.dframe)
			self.d_=True

		self.widget.setLayout(self.vbox)
		self.scroll = QScrollArea(self)
		self.scroll.setWidget(self.widget)
		self.scroll.setWidgetResizable(True)
		self.scroll.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
		self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)

		vbox1 = QVBoxLayout()
		vbox1.setContentsMargins(0,0,0,0)
		vbox1.setSpacing(0)

		vbox1.addWidget(self.scroll)
		self.setLayout(vbox1)


	def shortenTabName(self,cname):
		list1 =[]
		for i, ch in enumerate(cname):
				list1.append(ch)
				if len(list1)==40:
					if list1[i]== ' ':
						list1.pop(i)
					list1.append('...')
					break
		return ''.join(list1)

	def updater(self):
		self.x=+1
		if self.obj.courses[self.id_].dummy_items is '':
			return
		else:
			if  self.d_==True:
				child = self.vbox.takeAt(len(self.iFrames))
				if child.widget() is not None:
					child.widget().deleteLater()
				elif child.layout() is not None:
					clearLayout(child.layout())
				self.dframe.deleteLater()
				self.d_=False

			marker = len(self.iFrames)-1

			for i1 in range(marker,len(self.obj.courses[self.id_].items)):
				self.lbl.append(ExtendedQLabel(self,i1))
				cname = self.shortenTabName(self.obj.courses[self.id_].items[i1].i_name)
				self.lbl[i1].setText(cname)
				self.lbl[i1].setObjectName("lbl")
				self.sbtn[i1] = QPushButton('Save')
				self.sbtn[i1].setObjectName("sbtn")
				self.gbtn.append(QPushButton(QIcon(':/Assets/link.png'),''))
				self.gbtn[i1].setObjectName("linkBtn")
				self.gbtn[i1].id_ = i1
				self.gbtn[i1].clicked.connect(partial(self.copyLink,self.gbtn[i1].id_))
				self.sbtn[i1].clicked.connect(partial(self.saveItem,self.gbtn[i1].id_))

				if self.obj.courses[self.id_].items[i1].saved==1:
					self.obtn[i1] = QPushButton('Open')
					self.obtn[i1].setObjectName("obtn")
					self.obtn[i1].clicked.connect(partial(self.openItem,self.gbtn[i1].id_))

			for i2 in range(marker,len(self.obj.courses[self.id_].items)):
				if self.obj.courses[self.id_].items[i2].saved==1:
					self.iFrames.append(itemFrames(self.lbl[i2],self.gbtn[i2],self.sbtn[i2],self.obtn[i2]))
				elif self.obj.courses[self.id_].items[i2].saved==0:
					self.iFrames.append(itemFramesNew(self.lbl[i2],self.gbtn[i2],self.sbtn[i2]))
				else:
					self.iFrames.append(itemFramesForum(self.lbl[i2],self.gbtn[i2]))

			for i3 in range (marker+1,len(self.iFrames)):
				if i3%2==0:
					self.iFrames[i3].setObjectName('nFrameEven')
				else:
					self.iFrames[i3].setObjectName('nFrameEven')

				self.vbox.addWidget(self.iFrames[i3])
				y=0

			if len(self.iFrames)<4:
				self.dframe = QFrame()
				self.dframe.setObjectName('nFrameDummy')
				self.vbox.addWidget(self.dframe)
				self.d_=True


	def saveItem(self,id_):
		fileName = QFileDialog.getOpenFileName(self, 'Select Your File')
		if fileName[0] is '':
			return
		else:
			self.obtn[id_] = QPushButton('Open')
			self.obtn[id_].setObjectName("obtn")
			self.obtn[id_].clicked.connect(partial(self.openItem,self.gbtn[id_].id_))
			self.obj.courses[self.id_].items[id_].olink = fileName[0]
			self.obj.courses[self.id_].items[id_].saved=1
			self.iFrames[id_+1].grid.addWidget(self.obtn[id_],1,3)
			self.parent_.parent_.itemsWriter(fileName[0],self.id_,id_)

	def openItem(self,id_):
		fileName = self.obj.courses[self.id_].items[id_].olink
		if sys.platform == "win32":
			os.startfile(fileName)
		else:
			opener ="open" if sys.platform == "darwin" else "xdg-open"
			subprocess.call([opener, fileName])

	def copyLink(self,id_):
		cb = QApplication.clipboard()
		cb.clear(mode=cb.Clipboard)
		cb.setText(self.obj.courses[self.id_].items[id_].glink, mode=cb.Clipboard)
		pygame.init()
		pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'sounds/message.wav'))
		pygame.mixer.music.play()
		reply = QMessageBox.question(self,'Moodly',"The link has been copied", QMessageBox.Ok)
		if reply == QMessageBox.Ok:
			pass

class ExtendedQLabel(QLabel):

	def __init__(self, parent_,id_):
		super(ExtendedQLabel,self).__init__(parent_)
		self.id_=id_
	def mousePressEvent(self, ev):
		pass

class itemFrames(QFrame):

	def __init__(self,lbl,btn1,btn2,btn3):
		super().__init__()
		self.initUI(lbl,btn1,btn2,btn3)

	def initUI(self,lbl,btn1,btn2,btn3):
		self.grid = QGridLayout()
		self.grid.addWidget(lbl,1,0)
		self.grid.addWidget(btn1,1,1)
		self.grid.addWidget(btn2,1,2)
		self.grid.addWidget(btn3,1,3)
		self.grid.setContentsMargins(50,0,40,0)
		self.grid.setSpacing(0)
		self.setLayout(self.grid)

class itemFramesForum(QFrame):

	def __init__(self,lbl,btn1):
		super().__init__()
		self.initUI(lbl,btn1)

	def initUI(self,lbl,btn1):
		self.grid = QGridLayout()
		self.grid.addWidget(lbl,1,0)
		self.grid.addWidget(btn1,1,1)
		self.grid.setContentsMargins(50,0,40,0)
		self.grid.setSpacing(0)
		self.setLayout(self.grid)

class itemFramesNew(QFrame):

	def __init__(self,lbl,btn1,btn2):
		super().__init__()
		self.initUI(lbl,btn1,btn2)

	def initUI(self,lbl,btn1,btn2):
		self.grid = QGridLayout()
		self.grid.addWidget(lbl,1,0)
		self.grid.addWidget(btn1,1,1)
		self.grid.addWidget(btn2,1,2)
		self.grid.setContentsMargins(50,0,40,0)
		self.grid.setSpacing(0)
		self.setLayout(self.grid)


class topFrame(QFrame):

	def __init__(self,btn,lbl):
		super().__init__()
		self.initUI(btn,lbl)

	def initUI(self,btn,lbl):
		grid = QGridLayout()
		grid.addWidget(btn,1,1)
		grid.addWidget(lbl,1,0,QtCore.Qt.AlignLeft)
		grid.setContentsMargins(50,0,50,0)
		grid.setSpacing(0)
		self.setLayout(grid)


class errorFrame(QFrame):

	def __init__(self,lbl):
		super().__init__()
		self.initUI(lbl)

	def initUI(self,lbl):
		grid = QGridLayout()
		grid.addWidget(lbl,1,0)
		grid.setContentsMargins(50,0,50,0)
		grid.setSpacing(0)
		self.setLayout(grid)


class SystemTrayIcon(QSystemTrayIcon):

	trigger = pyqtSignal()
	qtrigger = pyqtSignal()
	uptrigger = pyqtSignal()

	def __init__(self, icon,parent=None):
		QSystemTrayIcon.__init__(self,icon, parent)
		menu = QMenu(parent)

		showAction = menu.addAction("Show Moodly")
		showAction.triggered.connect(self.trigger.emit)

		exitAction = menu.addAction("Exit")
		exitAction.triggered.connect(self.qtrigger.emit)

		self.updateAction = menu.addAction("Update Now")
		self.updateAction.triggered.connect(self.uptrigger.emit)
		self.updateAction.setEnabled(False)

		self.activated.connect(self.activateIcon)
		self.setContextMenu(menu)


	def display_notify(self,msg1,msg2,rsn):
		self.n_timer = QTimer()
		self.n_timer.timeout.connect(partial(self.timed_notify,msg1,msg2,rsn))
		self.n_timer.setSingleShot(True)
		self.n_timer.start(300)

	def timed_notify(self,msg1,msg2,rsn):
		self.showMessage(msg1, msg2,rsn)
		pygame.init()
		pygame.mixer.music.load(os.path.join(os.path.dirname(__file__), 'sounds/notify.wav'))
		pygame.mixer.music.play()

	def activateIcon(self,reason):
		if reason == QSystemTrayIcon.DoubleClick:
			self.trigger.emit()


class WorkThread(QtCore.QThread):

	def __init__(self,obj):
		QtCore.QThread.__init__(self)
		self.obj=obj

	def run(self):
		cnt = self.obj.validate()
		if cnt==True:
				dbconn = Models()
				try:
					dbconn.createTables()
				except:
					pass

				self.obj.writeUserData(dbconn)
				self.obj.writeConfig(dbconn)
				self.obj.writeNotify(dbconn)
				self.obj.writeData(dbconn)
				dbconn.commit()

				scrap = self.obj.courseScrapper()
				if scrap == True:
					dbconn = Models()
					self.obj.writeCourses(dbconn)
					self.obj.removeNotify(dbconn)
					self.obj.writeNotify(dbconn)
					self.obj.alterData(dbconn,3)
					dbconn.commit()
					dbconn.closeConn()

					self.obj.courses.extend(self.obj.dummy_courses)

					for course in self.obj.courses:
						course.itemScrapper(self.obj)
						if course.flink is not '':
							course.forumScrapper(self.obj)

					t = self.obj.scheduled
					t = str(t.strftime("%d/%m/%y , %I:%M %p"))

					if self.obj.error is 0:
						self.obj.notif[0].notif_text = 'Last Update Successfully Completed at %s'%t
						self.obj.notif[0].tag = 1
						self.obj.status_msg[0] = "Last Update Successfully Completed. You have %s new notifications"
						self.obj.status_msg[1] = 1
						self.obj.d_n-=1

					elif self.obj.h is 1 and self.obj.error is not 0:
						self.obj.notif[0].notif_text = 'Last Update Partially Completed at %s'%t
						self.obj.notif[0].tag = 0
						self.obj.status_msg[0] = "Last Update Partially Completed. You have %s new notifications."
						self.obj.status_msg[1] = 2
						self.obj.d_n-=1
					else:
						self.obj.notif = []
						self.obj.notif.append(Notify('Last Update Failed at %s'%t,0,0,self.obj.scheduled,datetime.datetime.now()))
						self.obj.d_n=1

					self.obj.n+=self.obj.d_n

					dbconn = Models()
					self.obj.removeNotify(dbconn)
					self.obj.alterCourses(dbconn)
					self.obj.writeItems(dbconn)
					self.obj.writeNotify(dbconn)
					self.obj.alterData(dbconn,1)
					self.obj.writeForum(dbconn)
					dbconn.commit()
					dbconn.closeConn()

				else:
					pass

				if self.obj.d_n is 0:
					str_= "no"
				else:
					str_ = str(self.obj.d_n)

				self.obj.status_msg[0] = self.obj.status_msg[0] % str_


		else:
			pass


class updateThread(QtCore.QThread):

	def __init__(self,obj):
		QtCore.QThread.__init__(self)
		self.obj=obj

	def run(self):
		self.obj.emptyGlobalTemp()
		self.obj.scheduled = datetime.datetime.now()
		self.obj.d_n=0
		t = self.obj.scheduled
		t = str(t.strftime("%d/%m/%y , %I:%M %p"))
		self.obj.status_msg[0] = "Last Update Failed. You have %s new notifications"
		self.obj.status_msg[1] = 3
		self.obj.d_n+=1
		self.obj.notif.append(Notify('Last Update Failed at %s'%t,0,0,self.obj.scheduled,datetime.datetime.now()))
		dbconn = Models()
		self.obj.writeNotify(dbconn)
		self.obj.alterData(dbconn,2)
		dbconn.commit()
		dbconn.closeConn()
		cnt = self.obj.courseScrapper()
		self.obj.courses.extend(self.obj.dummy_courses)

		for course in self.obj.courses:
			course.itemScrapper(self.obj)
			if course.flink is not '':
				course.forumScrapper(self.obj)
		if self.obj.error is 0:
			self.obj.notif[0].notif_text = 'Last Update Successfully Completed at %s'%t
			self.obj.notif[0].tag = 1
			self.obj.status_msg[0] = "Last Update Successfully Completed. You have %s new notifications"
			self.obj.status_msg[1] = 1
			self.obj.d_n-=1
		elif self.obj.h==1 and self.obj.error is not 0:
			self.obj.notif[0].notif_text = 'Last Update Partially Completed at %s'%t
			self.obj.notif[0].tag = 0
			self.obj.status_msg[0] = "Last Update Partially Completed. You have %s new notifications"
			self.obj.status_msg[1] = 2
			self.obj.d_n-=1
		else:
			self.obj.notif = []
			self.obj.notif.append(Notify('Last Update Failed at %s'%t,0,0,self.obj.scheduled,datetime.datetime.now()))
			self.obj.d_n = 1

		if self.obj.d_n is 0:
			str_= "no"
		else:
			str_ = str(self.obj.d_n)

		self.obj.status_msg[0] = self.obj.status_msg[0] % str_
		self.obj.n+=self.obj.d_n

		dbconn = Models()
		self.obj.removeNotify(dbconn)
		self.obj.writeCourses(dbconn)
		self.obj.alterData(dbconn,1)
		self.obj.writeForum(dbconn)
		self.obj.writeItems(dbconn)
		self.obj.writeNotify(dbconn)
		dbconn.commit()
		dbconn.closeConn()

class itemsWriterThread(QtCore.QThread):

	def __init__(self,fileName,id1,id2,id3,obj):
		QtCore.QThread.__init__(self)
		self.id3 = id3
		self.fileName=fileName
		self.id1=id1
		self.id2=id2
		self.obj=obj

	def run(self):
		dbconn = Models()
		dbconn.updateItems((self.fileName,self.obj.courses[self.id1].c_id,self.obj.courses[self.id1].items[self.id2].i_name))
		dbconn.commit()
		dbconn.closeConn()

class notifySeenThread(QtCore.QThread):

	def __init__(self,obj):
		QtCore.QThread.__init__(self)
		self.obj=obj

	def run(self):
		self.obj.changeNotify()
		dbconn = Models()
		self.obj.alterNotify(dbconn)
		dbconn.commit()
		dbconn.closeConn()

class configWriterThread(QtCore.QThread):

	def __init__(self,obj,text1,text2,combo1,combo2):
		QtCore.QThread.__init__(self)
		self.obj=obj
		self.text1=text1
		self.text2=text2
		self.combo1=combo1
		self.combo2=combo2


	def run(self):
		if self.text2 != self.obj.passwd :
			cnt = self.obj.reValidate(self.text2)

			if cnt == True:
				if str(self.combo1) == str(self.obj.nIntval):
					self.obj.intValChanged = 0
				elif str(self.combo2) == str(self.obj.upIntval):
					self.obj.intValChanged = 1
				elif str(self.combo2) == str(self.obj.upIntval) and str(self.combo1) == str(self.obj.nIntval) :
					self.obj.intValChanged = 2


				self.obj.saveUserData(str(self.text1),
							  str(self.text2),str(self.combo1),str(self.combo2))

				dbconn = Models()
				self.obj.alterUserData(dbconn)
				dbconn.commit()
				dbconn.closeConn()

			else:
				pass

		elif self.text2 == self.obj.passwd and self.combo1 == self.obj.nIntval and self.combo2==self.obj.upIntval:
			self.obj.config_status = 'There are no changes to save'
			self.obj.status_msg[0] = "There are no changes to save"
			self.obj.status_msg[1] = 2

		else:
			if str(self.combo1) == str(self.obj.nIntval):
				self.obj.intValChanged = 0
			elif str(self.combo2) == str(self.obj.upIntval):
				self.obj.intValChanged = 1
			elif str(self.combo2) == str(self.obj.upIntval) and str(self.combo1) == str(self.obj.nIntval) :
				self.obj.intValChanged = 2

			self.obj.saveUserData(str(self.text1),
						  str(self.text2),str(self.combo1),str(self.combo2))

			dbconn = Models()
			self.obj.alterUserData(dbconn)
			dbconn.commit()
			dbconn.closeConn()
			self.obj.config_status = 'Your changes have been saved successfully'
			self.obj.status_msg[0] = "Your changes have been saved successfully "
			self.obj.status_msg[1] = 1
