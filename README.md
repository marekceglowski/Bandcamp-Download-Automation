Bandcamp Bulk Album Downloader

This script will download free albums from BandCamp without user-interaction. Note: This script does NOT rip audio from BandCamp pages, it just automates the clicking process of downloading albums.

Requirements:
Python 3 
BeautifulSoup (pip install beautifulsoup4) (http://www.crummy.com/software/BeautifulSoup/bs4/doc/)
Splinter (pip install splinter) (https://splinter.readthedocs.org/en/latest/index.html)
PhantomJS (http://phantomjs.org/download.html)
PhantomJS Webdriver (pip install selenium)
wget (pip install wget)

Usage:
A list of free bandcamp album links seperated by newlines should go into an input file (default is dl.txt). Run the script and watch the output in your command window. You can change format to download in and disposable email used as variables at the top of the script.