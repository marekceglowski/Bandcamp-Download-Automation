# --- Notice: This project is now outdated, it won't work with Bandcamp's current webpage format! --- #
# --- #
# --- #


## Bandcamp Free Album Download Automator

This script will download free albums from Bandcamp without user-interaction. Note: This script does NOT rip audio from Bandcamp pages, it just automates the clicking process of downloading albums.

### Requirements:

* Python 3.4+ ([download](https://www.python.org/downloads/))
* Splinter (*pip install splinter*) ([docs](https://splinter.readthedocs.org/en/latest/index.html))
* PhantomJS ([download](http://phantomjs.org/download.html)) (place executable in same folder)
* PhantomJS Webdriver (*pip install selenium*)
* wget (*pip install wget*)

### How to use:

* A list of free bandcamp album links seperated by newlines should go into [links.ini](links.ini).
* Run the script and watch the output in your command window (or just let it run). 
* You can change the format download format and disposable email used as variables at the top of the script.

Download formats: MP3 V0, MP3 320, FLAC, AAC, Ogg Vorbis, ALAC, WAV, AIFF

### Some uses:

* Downloading Bandcamp albums in terminal (ex. over SSH connection)
* Automatically downloading a queue of bandcamp albums without clicking much
* Scripts that require Bandcamp albums to be downloaded before extraction, sharing, etc.

Copyright © 2016 Marek Ceglowski | [MIT license](https://opensource.org/licenses/MIT)
