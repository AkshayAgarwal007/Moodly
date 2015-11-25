import sqlite3
import os

class Models():

  def __init__(self):
     sqlite_file=os.path.join(os.getcwd(), "./moodly.sqlite")
     self.conn=sqlite3.connect(sqlite_file,timeout=120)


  def createTables(self):
      c = self.conn.cursor()
      c.execute('''CREATE TABLE CONFIGURE (ID INTEGER PRIMARY KEY AUTOINCREMENT,CONF INTEGER)''')
      c.execute('''CREATE TABLE USERDATA (ID INTEGER PRIMARY KEY AUTOINCREMENT,USERNAME TEXT, PASSWORD TEXT, NINTVAL TEXT,UPINTVAL TEXT)''')
      c.execute('''CREATE TABLE COURSES (NID INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT, ID TEXT, FLINK TEXT)''')
      c.execute('''CREATE TABLE ITEMS (NID INTEGER PRIMARY KEY AUTOINCREMENT,NAME TEXT, GLINK TEXT,OLINK TEXT, SAVED INT, DATE TIMESTAMP,ID TEXT )''')
      c.execute('''CREATE TABLE NOTIFY (NID INTEGER PRIMARY KEY AUTOINCREMENT,NOTIF TEXT ,TAG INT,SEEN INT,SCHEDULE TIMESTAMP,DATE TIMESTAMP)''')
      c.execute('''CREATE TABLE FORUM (FORUM TEXT,ID TEXT)''')
      c.execute('''CREATE TABLE DATA(ID INT, LASTSCR TIMESTAMP,NOTIF INT)''')


  def insertConfig(self,conf):
      c = self.conn.cursor()
      c.execute("INSERT INTO CONFIGURE VALUES(?,?)",(conf))


  def updateConfig(self,conf):
      c = self.conn.cursor()
      c.execute("UPDATE CONFIGURE SET CONF=? WHERE ID=?",(conf))


  def fetchConfig(self):
      c = self.conn.cursor()
      c.execute("SELECT * FROM CONFIGURE")
      rows =c.fetchall()
      for row in rows:
        return row


  def insertUserData(self,udata):
      c = self.conn.cursor()
      c.execute("INSERT INTO USERDATA VALUES(?,?,?,?,?)",(udata))


  def updateUserData(self,udata):
      c = self.conn.cursor()
      c.execute("UPDATE USERDATA SET PASSWORD=?, NINTVAL=?, UPINTVAL=? WHERE ID=?",(udata))


  def fetchUserData(self):
      c = self.conn.cursor()
      c.execute("SELECT * FROM USERDATA")
      rows =c.fetchall()
      for row in rows:
        return row


  def insertCourses(self,courses):
      c = self.conn.cursor()
      c.executemany("INSERT INTO COURSES(NAME,ID,FLINK) VALUES(?,?,?)",(courses))


  def updateCourses(self,courses):
      c = self.conn.cursor()
      c.execute("UPDATE COURSES SET FLINK=? WHERE ID=?",(courses))


  def deleteCourses(self,courses):
      c = self.conn.cursor()
      c.execute("DELTE FROM COURSES WHERE ID=?",(courses))


  def fetchCourses(self):
      c = self.conn.cursor()
      c.execute("SELECT * FROM COURSES ORDER BY NID DESC")
      rows =c.fetchall()
      return rows


  def insertItems(self,items):
      c = self.conn.cursor()
      c.executemany("INSERT INTO ITEMS(NAME,GLINK,OLINK,SAVED,DATE,ID) VALUES(?,?,?,?,?,?)",(items))


  def updateItems(self,items):
      c = self.conn.cursor()
      c.execute("UPDATE ITEMS SET SAVED =1,OLINK=? WHERE ID=? AND NAME=?",(items))


  def fetchItems(self,items):
      c = self.conn.cursor()
      c.execute("SELECT * FROM ITEMS WHERE ID=? ORDER BY NID DESC",(items,))
      rows =c.fetchall()
      return rows


  def insertNotify(self,notif):
      c = self.conn.cursor()
      c.executemany("INSERT INTO NOTIFY(NOTIF,TAG,SEEN,SCHEDULE,DATE) VALUES(?,?,?,?,?)",(notif))


  def updateNotify(self):
      c = self.conn.cursor()
      c.execute("UPDATE NOTIFY SET SEEN=1 WHERE SEEN=0")

  def deleteNotify(self,notif):
      c = self.conn.cursor()
      c.execute("DELETE FROM NOTIFY WHERE SCHEDULE=?",(notif,))

  def fetchNotify(self,notif):
      c = self.conn.cursor()
      c.execute("SELECT NOTIF,TAG,SEEN,SCHEDULE,DATE FROM NOTIFY WHERE SEEN=0 ORDER BY SCHEDULE DESC,NID DESC")
      rows = c.fetchall()
      if rows == []:
          c.execute("SELECT NOTIF,TAG,SEEN,SCHEDULE,DATE FROM NOTIFY WHERE SCHEDULE=? ORDER BY NID DESC",(notif,))
          rows =c.fetchall()
      return rows

  def insertForum(self,forum):
      c = self.conn.cursor()
      c.executemany("INSERT INTO FORUM VALUES(?,?)",(forum))

  def fetchForum(self,forum):
      c = self.conn.cursor()
      c.execute("SELECT * FROM FORUM WHERE ID =?",(forum,))
      rows = c.fetchall()
      return rows

  def insertData(self,data):
     c = self.conn.cursor()
     c.execute("INSERT INTO DATA VALUES(?,?,?)",(data))

  def updateDataScr(self,data):
     c = self.conn.cursor()
     c.execute("UPDATE DATA SET LASTSCR=? WHERE ID=?",(data))

  def updateDataNotif(self,data):
     c = self.conn.cursor()
     c.execute("UPDATE DATA SET NOTIF=? WHERE ID=?",(data))

  def fetchData(self):
     c = self.conn.cursor()
     c.execute("SELECT * FROM DATA")
     rows = c.fetchall()
     return rows[0]

  def closeConn(self):
      self.conn.close()

  def commit(self):
      self.conn.commit()
