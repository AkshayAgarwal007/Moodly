from setuptools import setup

setup(

    name="Moodly",

    version="1.0",

    author="Akshay Agarwal",

    author_email="agarwal.akshay.akshay8@gmail.com",

    packages=["Moodly"],

    include_package_data=False ,

    url="http://github.com/AkshayAgarwal007/Moodly",

    entry_points = {
              'gui_scripts': [
                  'moodly = Moodly.controller:main',
              ],
          },

    # license="LICENSE.txt",

    description="Student Intimation System for Moodle(NIIT University)",

    # long_description=open("README.txt").read(),

    # Dependent packages (distributions)

)

