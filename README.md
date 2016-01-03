
![Moodly Logo](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/moodly_logo.png "Moodly Logo")

## What is Moodly?

Moodly is a student intimation system for Moodle (NIIT University). It a desktop app which keeps you updated with notifications of files uploaded or any forum updates (of the courses you are registered in) on NU-Moodle. In addition to that it also helps you download and manage your Moodle course files. 

Moodly is written in Python. It uses PyQt5, a set of python bindings for the Qt5 Application framework for its GUI, Requests for sending HTTP requests and BeautifulSoup for HTML parsing.

This does not make use of any Moodle API because it was intended to be a Web Scrapping Project. 

##Using Moodly

If you have been able to successfully install Moodly, this should be very easy for you.

##Configuration

The first thing you need to do after installing Moodly is configure it up. You need to fill in your **Moodle Username** and **Password**. **Update interval** is the time interval in which you want Moodly to fetch data from the university Moodle servers. **Keep Notifying** is the time interval in which you would be notified by Moodly about any unread notifications if any. This feature is turned off by default. 

You can make changes to your configuration in the future. However, once your credentials (username and password) get verified you won’t be able to change your username. To do this you can reset the app by deleting the **moodly.sqlite** file.


![Moodly Configure](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/config_linux.png "Initial Configuration")

![Moodly Configure](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/config_tab_linux.png "Changing Configurations")

##Setup

This would follow the initial configuration and would take time depending upon the number of courses you are registered in and the number of files and forum news each course contain. You are required to wait patiently during the setup phase.


![Setup](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/setup_linux.png "Setup")

##Courses
The course tab lists all the courses that you are registered in and clicking on the **FILES** button would open the corresponding course item tab.


![Course Tab](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/course_tab_linux.png "Course Tab")

##Course Files

The course item tab would list all the course files. Initially there would be just a save button inside each item frame. After you save that particular file by selecting it from your local system, an open button would also accompany the initial save button and from the next time you can use that to open that particular file.

You can make use of the white-colored link button to copy the Moodle URL of a file to your clipboard. This may assist you to download files from Moodle.

This might be little tedious but thankfully the next feature update Moodly will see is Automatic File Download.


![Item Tab](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/item_tab_linux.png "Item Tab")

##Notifications

The notification tab would contain all the update notifications.


![Notifications Tab](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/notify_tab_linux.png "Notifications Tab")

##Shortcuts 

* **Ctrl+Shift+C** - Configure

* **Ctrl+U** – Update Moodly

* **Ctrl+Q** – Quit Moddly

Clicking the close button will minimize Moodly to the System Tray. You can either press Ctrl+Q or right click on the System Tray icon and click on Exit to close the app and remove it from the tray. 

##Upcoming Features

* Automatic File Download
* MOOCs recommendation System
* Gate pass request status and submission system
* Task Scheduler

##Developers

Though this application is specifically made for NU-Moodle, the code can be modified to work with any website that makes use of Moodle or has a similar structure. However, anyone who wants to build such an app would prefer to use Moodle APIs and different tools because of the recent trend to build a universal app, the code base for Moodly can serve as a learning resource for those learning to make GUI applications using Python, working on a web scrapping project using Python or just wants to explore Python more.

##Contributing 

* Found a bug? Report it on GitHub Issues and include a code sample.
* Fork the repository and work on a feature update. 
* Users can also contribute by reporting a bug by simply mailing me. 

___

Developed and maintained by Akshay Agarwal.
