import os

if os.name=='posix':
    from xdg.BaseDirectory import *

def getResourcePath():
    if os.name =='nt':
        dir_path = os.path.join(os.environ['APPDATA'], 'Moodly')
        print (dir_path)
    elif os.name=='posix':
        dir_path = os.path.join(xdg_data_home, 'Moodly')
    file_path = os.path.join(dir_path, 'moodly.sqlite')
    return file_path

def makeDataDirs():
     if os.name=='nt':
         dir_path = os.path.join(os.environ['APPDATA'], 'Moodly')
     elif os.name=='posix':
         dir_path = os.path.join(xdg_data_home, 'Moodly')
     if not os.path.exists(dir_path):
          os.makedirs(dir_path)
