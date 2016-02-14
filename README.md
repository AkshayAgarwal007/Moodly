
![Moodly Logo](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/moodly_logo.png "Moodly Logo")

## What is Moodly?

Moodly is a student intimation system for [Moodle](https://moodle.org/) (NIIT University). It is a desktop app which keeps you updated with notifications of files uploaded or any forum updates (of the courses you are registered in) on [NU-Moodle](https://moodle.niituniversity.in/moodle/). In addition to that it also helps you download and manage your Moodle course files. 

Moodly is written in Python. It uses PyQt5, a set of Python bindings for the Qt5 Application framework for its GUI, Requests for sending HTTP requests and BeautifulSoup for HTML parsing.

This does not make use of any Moodle API because it was intended to be a Web Scrapping Project. 

##Installation

###Windows

1. Download the [.7z file] (https://www.dropbox.com/s/px4mi7usczio9lp/Moodly.7z?dl=0) and extract it.
  
2. Copy the extracted Moodly.exe to your preferable location. And that's it.

**To launch the application on startup**

1. Create a shortcut for Moodly.exe

2. From the start menu open the run command box and type `shell:startup` and click on Ok.

3. Copy the shortcut to this location (i.e the startup directory). And you are done. Now reboot and Moodly should launch on startup. 

###Linux

1. Download the [tar file](https://www.dropbox.com/s/iv082uae4e4zr41/Moodly-1.0-Alpha-Linux.tar.gz?dl=0) and extract it.

2. Copy the extracted Moodly executable to your preferable location. And Thats it!

**To lauch the application on startup**

1. Open the terminal.

2. Type `$PATH` and check whether `/usr/bin` is set on your Linux path or not, it should definitely be there.

3. Create a symlink to Moodly there by simply typing

   ```
   cd /usr/bin (or /usr/local/bin or ~/.local/bin)

   sudo ln -s  /path/to/Moodly (for e.g sudo ln -s $HOME/Moodly)
   ```

4. Copy the extracted Moodly.desktop to `~/.config/autostart/ or (/etc/xdg/autostart)`
   ```
   cp /path/to/Moodly.desktop ~/.config/autostart/
   ```

5. And you are done. Now reboot and Moodly should launch on startup. 

**Note:**

There are several ways you can make the application launch on startup and there are varied answers you'll find for this on the web. Not all will work You should find the one that suits you the best. The one for windows should definitely work but the answer varies for different linux distros.

You can do many things like add the Moodly executable in a directory and add its path to `~/.profile` or `~/.bash_profile` and create a bash script to launch the executable and store it in `/etc/init.d` and then create a symlink for it in `rc.d` or use the `rc.local` way or use `crontabs` or take the `gui route` and add it to `Startup Applications Preferences`. At the end of the day you are a linux user and you probably know how to solve your issues if you are facing one.

These are a few links that should help you understand things better:

* [Set path permanently on linux](http://stackoverflow.com/questions/14637979/how-to-permanently-set-path-on-linux)

* [Difference between bashrc and bash-profile](http://stackoverflow.com/questions/415403/whats-the-difference-between-bashrc-bash-profile-and-environment)

* [Launch program on startup-linux](http://stackoverflow.com/questions/7221757/run-automatically-program-on-startup-under-linux-ubuntu)

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


![Notifications Tab](https://github.com/AkshayAgarwal007/Moodly/blob/master/img/notify_tab.png "Notifications Tab")

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

Though this application is specifically made for NU-Moodle, the code can be modified to work with any website that makes use of Moodle or has a similar structure. However, anyone who wants to build such an app would prefer to use Moodle APIs and different tools because of the recent trend to build a universal app and packaging issues associated with Python Applications, the code base for Moodly can serve as a learning resource for those learning to make GUI applications using Python, working on a web scrapping project using Python or just wants to explore Python more.

Since this app targets a higly specific group of people there might not be many developers visiting this repo. Though there are many aspects of this application like (Web Scrapping, Making GUI apps using Python, Packaging a Python app,multithreading. writing non-blocking code, working with libraries like sqlite3, requests and BeautifulSoup) which is of importance to any Python developer and I would like to explain those things to you (You must be interested if you are reading this). But instead of doing that here I would prefer to write a blog on this topic and I would add the link to the same here as soon as I do so.

##Contributing 

* Found a bug? Report it on GitHub [Issues](https://github.com/AkshayAgarwal007/Moodly/issues) and include a code sample.
* [Fork](https://github.com/AkshayAgarwal007/Moodly/issues#fork-destination-box) the repository and work on a feature update. 
* Users can also contribute by reporting a bug by simply [mailing me](mailto:agarwal.akshay.akshay8@gmail.com). 

___

Developed and maintained by [Akshay Agarwal](mailto:agarwal.akshay.akshay8@gmail.com). Any suggestions are welcomed.
