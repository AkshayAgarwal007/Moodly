
![Moodly Logo](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/moodly_logo.png "Moodly Logo")

## What is Moodly?

Moodly is a student intimation system for Moodle (NIIT University). It a desktop app which keeps you updated with notifications of files uploaded or any forum updates (of the courses you are registered in) on NU-Moodle. In addition to that it also helps you download and manage your Moodle course files. 

Moodly is written in Python. It uses PyQt5, a set of python bindings for the Qt5 Application framework for its GUI, Requests for sending HTTP requests and BeautifulSoup for HTML parsing.

This does not make use of any Moodle API because it was intended to be a Web Scrapping Project. 

##Using Moodly

If you have been able to successfully install Moodly, this should be very easy for you.

##Configuration

The first thing you need to do after installing Moodly is configure it up. You need to fill in your Moodle Username and Password. Update interval is the time interval in which you want Moodly to fetch data from the university Moodle servers. Keep Notifying is the time interval in which you would be notified by Moodly about any unread notifications if any. This feature is turned off by default. 
You can make changes to your configuration in the future. However, once your credentials (username and password) get verified you won’t be able to change your username. Instead you can reset the app by deleting the moodly.sqlite file but that would mean a loss of previous data.

![Moodly Configure](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/config_linux.png "Initial Configuration")

![Moodly Configure](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/config_tab_linux.png "Changing Configurations")

##Setup

This would follow the initial configuration and would take time depending upon the number of courses you are registered in and the number of files and forum news each course contain. You are required to wait patiently during the setup phase.
Courses
The course tab lists all the courses that you are registered in and clicking on the FILES button would open the corresponding course item tab.

![Setup](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/setup_linux.png "Setup")

##Course Files

The course item tab would list all the course files. Initially there would be just a save button inside each item frame. After you save that particular file by selecting it from your local system, an open button would also accompany the initial save button and from the next time you can use that to open that particular file.
You can make use of the white-colored link button to copy the Moodle URL of a file to your clipboard. This may assist you to download files from Moodle.
This might be little tedious but thankfully the next feature update Moodly will see is Automatic File Download.

![Course Tab](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/course_tab_linux.png "Course Tab")

![Item Tab](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/item_tab_linux.png "Item Tab")

##Notifications

The notification tab would contain all the update notifications.

![Notifications Tab](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/notify_tab_linux.png "Notifications Tab")

##Shortcuts 

Ctrl+Shift+C - Configure
Ctrl+U – Update Moodly
Ctrl+Q – Quit Moddly
Clicking the close button will minimize Moodly to the System Tray. You can either press Ctrl+Q or right click on the system tray icon and click on Exit to close the app and remove it from the tray. 
