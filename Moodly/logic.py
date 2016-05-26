from .models import *
from requests import session
from bs4 import BeautifulSoup
from random import randint
import re
from requests.exceptions import ConnectionError
import datetime
import sys
import os


class Configure():

    def __init__(self):

        self.configured=0
        self.dwnld=0
        self.config_status=''
        self.notif=[]
        self.intValChanged =-1
        self.courses = []
        self.error = 0
        self.dir_url=''
        self.status_msg=[]
        self.scheduled = 0
        self.seen=-4
        self.updating=False
        self.n = 0
        self.d_n=0
        self.h=0
        self.c_names = []
        self.c_id = []
        self.dummy_courses=[]
        self.tagDict = {0:':/Assets/error.png',1:':/Assets/gtick.png',2:':/Assets/file.png',3:':/Assets/forum.png',4:':/Assets/hw.png'}
        self.initialise()

    def initialise(self):
        self.status_msg = ['','']

    def getConfig(self):

        ptr = Models()
        try:
            row =ptr.fetchConfig()
            self.configured = row[1]

            if self.configured == 2:
                self.getUserData(ptr)
                self.getData(ptr)
                self.getNotify(ptr)
                self.getCourses(ptr)
                self.getForum(ptr)

                if len(self.courses) is not 0:
                    self.getItems(ptr)

                self.generateCheckers()

        except:
            self.configured=0

        finally:
            ptr.closeConn()

    def getUserData(self,ptr):
        row = ptr.fetchUserData()
        self.uname=row[1]
        self.passwd=row[2]
        self.nIntval=row[3]
        self.upIntval=row[4]
        self.dwnld=row[5]
        self.dir_url=row[6]

    def writeConfig(self,ptr):
        ptr.insertConfig((0,self.configured))

    def writeUserData(self,ptr):
        ptr.insertUserData((0,self.uname,self.passwd,self.nIntval,self.upIntval,self.dwnld,self.dir_url))

    def alterConfig(self,ptr):
        ptr.updateConfig((self.configured,self.statux_text,0))

    def alterUserData(self,ptr):
        ptr.updateUserData((self.passwd,self.nIntval,self.upIntval,self.dwnld,self.dir_url,0))

    def saveConfig(self,configured):
        self.configured=configured

    def saveUserData(self,uname,passwd,nIntval,upIntval,dwnld,path_):
        self.uname=uname
        self.passwd=passwd
        self.nIntval=nIntval
        self.upIntval=upIntval
        self.dwnld=dwnld
        self.dir_url = path_

    def writeCourses(self,ptr):
        t=()
        for courses in self.dummy_courses:

            t=((courses.c_name,courses.c_id,courses.flink),)+t
        ptr.insertCourses(t)

    def alterCourses(self,ptr):
        for course in self.courses:
            ptr.updateCourses((course.flink,course.c_id))

    def removeCourses(self,c_id,ptr):
        ptr.deleteCourses((c_id))

    def getCourses(self,ptr):
        courses=ptr.fetchCourses()
        for course in courses:
            self.courses.append(Course(course[1],course[2],course[3]))

    def writeNotify(self,ptr):
        t=()
        for j in range(0,len(self.notif)):
                t=((self.notif[j].notif_text,self.notif[j].tag,self.notif[j].seen,self.notif[j].scheduled,self.notif[j].date),)+t
        ptr.insertNotify(t)

    def emptyGlobalTemp(self):
        self.notif=[]
        self.error=0
        self.h=0
        self.d_n=0

    def getNotify(self,ptr):
        notifications = ptr.fetchNotify(self.lastScr)
        for notif in notifications:
            self.notif.append(Notify(notif[0],notif[1],notif[2],notif[3],notif[4]))

    def removeNotify(self,ptr):
        ptr.deleteNotify((self.scheduled))

    def writeItems(self,ptr):
        t=()
        for course in self.courses:
            for items in course.dummy_items:
                t=((items.i_name,items.glink,items.olink,items.saved,items.date,course.c_id,items.dwnld,items.type),)+t
        ptr.insertItems(t)

    def getItems(self,ptr):
        for course in self.courses:
            items = ptr.fetchItems(course.c_id)
            for item in items:
                course.items.append(Items(item[1],item[2],item[3],item[4],item[5],item[7],item[8]))

    def writeForum(self,ptr):
        t=()
        for course in self.courses:
            for text in course.dummy_forum:
                t=((text,course.c_id),)+t
        ptr.insertForum(t)

    def getForum(self,ptr):
        for course in self.courses:
            forum = ptr.fetchForum(course.c_id)
            for text in forum:
                course.forum.append(text[0])

    def writeData(self,ptr):
        ptr.insertData((0,self.scheduled,1))

    def alterData(self,ptr,con):
        if con==0:
            ptr.updateDataScr((self.scheduled,0))
        elif con==1:
            ptr.updateDataNotif((self.n,0))
        elif con==2:
            ptr.updateDataScr((self.scheduled,0))
            ptr.updateDataNotif((self.n+1,0))
        else:
            ptr.updateDataNotif((1,0))

    def getData(self,ptr):
        data = ptr.fetchData()
        self.n =data[2]
        self.lastScr = data[1]

    def generateCheckers(self):
        if len(self.courses) is not 0:
          for course in self.courses:
            self.c_names.append(course.c_name)
            self.c_id.append(course.c_id)
            if len(course.items) is not 0:
                for item in course.items:
                    course.glink.append(item.glink)

    def alterNotify(self,ptr):
        ptr.updateNotify()
        self.alterData(ptr,1)

    def changeNotify(self):
        for notif in self.notif:
          if notif.seen==0:
            notif.seen=1
        self.n=0

    def reValidate(self,passwd):
        payload = {
        'action' : 'login',
        'username' : self.uname,
        'password' : passwd
          }

        try:
           with session() as c:
              c.post('https://moodle.niituniversity.in/moodle/login/index.php/', data=payload,timeout=20)
              response=c.get('https://moodle.niituniversity.in/moodle/my/index.php?mynumber=100',timeout=20)

        except:
            self.config_status = "Connection can't be established with the server."
            self.status_msg[0] = "Unable to Configure. Connection can't be established with the server. "
            self.status_msg[1] = 3
            return False

        soup=BeautifulSoup(response.text,"lxml")

        if "My home" not in soup.head.title.text:
             self.config_status="Either your username or password is incorrect"
             self.status_msg[0] = "Unable to Configure. Either your username or password is incorrect. "
             self.status_msg[1] = 3
             return False

        self.config_status="Your changes have been successfully changed successfully"
        self.status_msg[0] = "Your password has been successfully changed "
        self.status_msg[1] = 1

        return True


    def validate(self):
        payload = {
        'action' : 'login',
        'username' : self.uname,
        'password' : self.passwd
          }

        self.scheduled = datetime.datetime.now()

        try:
           with session() as c:
              c.post('https://moodle.niituniversity.in/moodle/login/index.php/', data=payload,timeout=20)
              response=c.get('https://moodle.niituniversity.in/moodle/my/index.php?mynumber=100',timeout=20)

        except:
            self.config_status = "Connection can't be established with the server."
            self.status_msg[0] = "Unable to Configure. Connection can't be established with the server. "
            self.status_msg[1] = 3
            self.saveConfig(0)
            return False

        soup=BeautifulSoup(response.text,"lxml")

        if "My home" not in soup.head.title.text:
             self.config_status="Either your username or password is incorrect"
             self.status_msg[0] = "Unable to Configure. Either your username or password is incorrect"
             self.status_msg[1] = 3
             self.saveConfig(0)
             return False

        self.saveConfig(2)
        t = self.scheduled
        t = str(t.strftime("%d/%m/%y , %I:%M %p"))
        self.notif.append(Notify('Last Update Failed at %s'%t,0,0,self.scheduled,datetime.datetime.now()))
        self.status_msg[0] = "Last Update Failed. You have %s unread notifications"
        self.status_msg[1] = 3
        self.d_n+=1

        return True

    def courseScrapper(self):
        list_ci=[]
        list_cl=[]

        self.dummy_courses = []

        payload = {
        'action' : 'login',
        'username' : self.uname,
        'password' : self.passwd
          }

        try:
           with session() as c:
              c.post('https://moodle.niituniversity.in/moodle/login/index.php/', data=payload,timeout=20)
              response=c.get('https://moodle.niituniversity.in/moodle/my/index.php?mynumber=100',timeout=20)

        except  :
            self.error=1
            return False

        soup=BeautifulSoup(response.text,"lxml")

        self.h=1
        for i in soup.find_all("h2",attrs={'class':'title'}):
            for j in i.find_all('a'):
                if j.text not in self.c_names:
                    list_cl.append(j.text)
        for tag in soup.find_all(class_='box coursebox'):
            if re.findall(r'\d+', tag.get('id'))[0] not in self.c_id:
                list_ci.append(re.findall(r'\d+', tag.get('id'))[0])

        for k in range(0,len(list_ci)):
                self.dummy_courses.append(Course(list_cl[k],list_ci[k],''))

        if len(list_ci) is not 0:
            self.notif.append(Notify('%s courses has been added'%len(list_ci),2,0,self.scheduled,datetime.datetime.now()))
            self.d_n+=1

        self.c_names.extend(list_cl)
        self.c_id.extend(list_ci)

        return True



class Course():

    def __init__(self,c_name,c_id,flink):
        self.c_name = c_name
        self.c_id = c_id
        self.flink = flink
        self.forum = []
        self.added = False
        self.failed = False
        self.dummy_forum=[]
        self.items = []
        self.glink=[]
        self.dummy_items = []
        self.it_count=0

    def forumScrapper(self,obj):
     if self.failed == False:
        self.dummy_forum=[]
        items=[]

        payload = {
            'action': 'login',
            'username': obj.uname,
            'password': obj.passwd
        }

        try:
           with session() as c:
              c.post('https://moodle.niituniversity.in/moodle/login/index.php/', data=payload,timeout=20)
              response = c.get(self.flink,timeout=20)

        except:
            obj.notif.append(Notify('Forum Update Failed for %s'%self.c_name,0,0,obj.scheduled,datetime.datetime.now()))
            obj.error=1
            obj.d_n+=1
            return

        item=0
        obj.h=1
        soup=BeautifulSoup(response.text,"lxml")
        for i in soup.findAll('td',attrs={'class':'topic starter'}):
            for r in i.find_all("a"):
                if i.text not in self.forum:
                    self.dummy_forum=[i.text]+self.dummy_forum
                    items.append(Items(i.text,r['href'],'',0,datetime.datetime.now(),0,1))
                    item+=1


        if item is not 0 and self.added == False:
            obj.notif.append(Notify('%s Successfully updated'%self.c_name,1,0,obj.scheduled,datetime.datetime.now()))
            obj.notif.append(Notify('%s items has been added'%str(item),2,0,obj.scheduled,datetime.datetime.now()))
            obj.d_n+=1

        if self.added==True and item is not 0:
            obj.notif[-1].notif_text = '%s items has been added'%str(item+self.it_count)


        for text in self.dummy_forum:
            obj.notif.append(Notify('%s'%text,3,0,obj.scheduled,datetime.datetime.now()))
            obj.d_n+=1

        self.dummy_items.extend(items)
        self.forum.extend(self.dummy_forum)
        self.items.extend(items)

    def createDirs(self,obj,c_name):
        path_= os.path.join(obj.dir_url, c_name)
        if not os.path.exists(path_):
            os.makedirs(path_)

    def itemScrapper(self,obj):
        self.added = False
        self.failed = False
        self.dummy_items = []
        self.it_count=0

        payload = {
        'action' : 'login',
        'username' : obj.uname,
        'password' : obj.passwd
          }

        try:
           with session() as c:
              c.post('https://moodle.niituniversity.in/moodle/login/index.php/', data=payload,timeout=20)
              response = c.get('https://moodle.niituniversity.in/moodle/course/view.php?id=%s'%self.c_id,timeout=20)

        except :
            obj.notif.append(Notify('Update Failed for %s'%self.c_name,0,0,obj.scheduled,datetime.datetime.now()))
            obj.error=1
            obj.d_n=obj.d_n+1
            self.failed = True

            return

        obj.h=1
        soup=BeautifulSoup(response.text,"lxml")
        item=0
        pos=0
        assign = 0
        noscrap = []
        for k in soup.find_all("div",attrs={'class':'activityinstance'}):
            for r in k.find_all("a"):
              if r['href'] not in self.glink:
                self.dummy_items.append(Items('',r['href'],'',0,datetime.datetime.now(),0,0))
                self.glink.append(r['href'])


                if "forum/view.php" in r['href'] and self.flink is '':
                    self.flink = r['href']
                    self.dummy_items[item].saved=2

                item=item+1
              else:
                  noscrap.append(pos)
              pos=pos+1

        pos=0
        num=0
        a = ["assignment","exam","quiz"]

        for i in soup.find_all("div",attrs={'class':'activityinstance'}):
            for j in i.find_all("span",attrs={'class':'instancename'}):
              if pos not in noscrap:
                if any(x in j.text.lower() for x in a):
                    obj.notif.append(Notify('%s'%j.text,4,0,obj.scheduled,datetime.datetime.now()))
                    obj.d_n+=1
                self.dummy_items[num].addText(j.text)
                num=num+1
              pos=pos+1

        if item is not 0:
            obj.notif.append(Notify('%s Successfully updated'%self.c_name,1,0,obj.scheduled,datetime.datetime.now()))
            self.added = True
            obj.notif.append(Notify('%s items has been added'%str(item),2,0,obj.scheduled,datetime.datetime.now()))
            obj.d_n+=1
        self.items.extend(self.dummy_items)
        self.it_count=item


class Items(object):

    def __init__(self,i_name,glink,olink,saved,date,dwnld,type_):
        self.i_name=i_name
        self.glink=glink
        self.olink=olink
        self.saved=saved
        self.date = date
        self.dwnld = dwnld
        self.type = type_

    def addText(self,i_name):
        i_name = re.sub('File', '', i_name)
        self.i_name=i_name

    def downloadForumItem(self,obj,c_name):
        payload = {
        'action' : 'login',
        'username' : obj.uname,
        'password' : obj.passwd
          }

        try:
            with session() as c:
               c.post('https://moodle.niituniversity.in/moodle/login/index.php/', data=payload,timeout=20)
               r=c.get(self.glink,timeout=20,stream=True)

        except:
                return False

        soup=BeautifulSoup(r.text,"lxml")
        
        try:
            c_name = c_name.lstrip().rstrip()
            fileName = self.generateFileName(0)
            path_ = os.path.join(obj.dir_url, c_name)
            path_ = os.path.join(path_, fileName)
        
            with open(path_, 'w') as f:
                for i in soup.find_all(class_='posting fullpost'):
                    for j in i.find_all('p'):
                        f.write(str(j))
                        
            
        except:
            c_name = c_name.lstrip().rstrip()
            fileName = self.generateFileName(1)
            path_ = os.path.join(obj.dir_url, c_name)
            path_ = os.path.join(path_, fileName)
        
            with open(path_, 'w') as f:
                for i in soup.find_all(class_='posting fullpost'):
                    for j in i.find_all('p'):
                        f.write(str(j))
    

        self.dwnld=1
        self.saved=1
        self.olink = path_
        return True
        
    def generateFileName(self,val):
        ext='.html'
        fileName = self.i_name.lstrip().rstrip()
        if val==0:
            tmp = fileName.split(',', 1)[0]
        else:
            tmp = fileName.split(' ', 1)[0] + str(randint(0,9))
        
        
        fileName=tmp+ext
        return fileName


    def downloadItem(self,obj,c_name):
        payload = {
        'action' : 'login',
        'username' : obj.uname,
        'password' : obj.passwd
          }

        try:
            with session() as c:
               c.post('https://moodle.niituniversity.in/moodle/login/index.php/', data=payload,timeout=20)
               r=c.get(self.glink,timeout=20,stream=True)

        except:
             return False

        if r.headers['Content-Type'] == 'application/pdf':
            ext= '.pdf'
        elif r.headers['Content-Type'] =='application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            ext= '.docx'
        elif r.headers['Content-Type'] =='application/vnd.openxmlformats-officedocument.presentationml.presentation':
            ext = '.pptx'
        else:
            return False

        fileName = self.i_name.lstrip().rstrip() + ext
        c_name = c_name.lstrip().rstrip()
        path_ = os.path.join(obj.dir_url, c_name)
        path_ = os.path.join(path_, fileName)
        
        
        with open(path_, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)
        self.dwnld=1
        self.saved=1
        self.olink = path_
        return True

class Notify():

    def __init__(self,n_text,tag,seen,scheduled,date):
        self.notif_text = n_text
        self.tag =  tag
        self.seen = seen
        self.scheduled=scheduled
        self.date=date
