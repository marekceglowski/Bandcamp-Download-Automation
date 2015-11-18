from splinter import Browser
from bs4 import BeautifulSoup
import urllib.request
import codecs
import time
import json
import wget

##########
# Bandcamp Bulk Album Downloader
# 
# This script will download free albums from Bandcamp without user-interaction.
# Note: This script does NOT rip audio from Bandcamp pages, it just automates the
# process of downloading albums.
# 
##########

list_file = 'dl.txt'  # File with list of Bandcamp URLs separated by newlines.
mail_name = 'heyo231' # Name used for disposable mail service, pick something unique.
dl_format = 'FLAC'	  # Audio format to download in.
					  # List of options (case sensitive):
						# MP3 V0
						# MP3 320
						# FLAC
						# AAC
						# Ogg Vorbis
						# ALAC
						# WAV
						# AIFF

# Function for finding the nth occurrence of a substring
def find_nth(haystack, needle, n):
	start = haystack.find(needle)
	while start >= 0 and n > 1:
		start = haystack.find(needle, start+len(needle))
		n -= 1
	return start

content = []	# Open file with list of Bandcamp albums to download
with open(list_file) as f:
    content = f.readlines()

browser = Browser('phantomjs')
for album in content:
	url = album.replace("\n","")
	print('URL: '+album)
	browser.visit(url)
	artistName = browser.find_by_id('band-name-location')[0].value.split('\n')[0] 	# Get artist name from top-right
	print('Getting artist name.')													# Will be used in the email portion

	# Check download's type (either says 'Buy Now (name your price)' or 'Free Download')
	if browser.is_text_present('Buy Now'):
	    enterPrice = True
	    print('Button is of type \'Buy Now\'')
	else:
	    enterPrice = False
	    print('Button is of type \'Free Download\'')

	# Click the Buy Now or Free Download button
	for b in browser.find_by_tag('button'):
		if b.value == 'Buy Now':
			enterPrice = True
			print('Button is of type \'Buy Now\'')
			b.click()
			break
		elif b.value == 'Free Download':
			enterPrice = False
			print('Button is of type \'Free Download\'')
			b.click()
			break

	# If Buy Now
	if (enterPrice == True):
		browser.find_by_id('userPrice').first.fill('0') # Fill $0 as price to pay
		
	# If email required
	if browser.is_text_present('Email a link to my free download'):
		print('Email required. Inputting email info.')
		browser.find_by_id('fan_email_address').first.fill(mail_name+'@mailinator.com') # Fill email field
		browser.find_by_id('fan_email_postalcode').first.fill('111111') 				# Fill postal code field
		for button in browser.find_by_tag('button'):
			if (button.value == 'OK'):
				button.click() 		# Click OK
				break
		# Go to disposable mail API
		print('Waiting for email.')
		emailRecieved = False 
		message_id = ''
		while (emailRecieved == False):
			time.sleep(5)
			response = urllib.request.urlopen('https://api.mailinator.com/api/inbox?to='+mail_name)	# Request mailbox JSON
			html = str(response.read())
			soup = BeautifulSoup(html,'lxml')
			text = soup.get_text()[soup.get_text().find('{'):soup.get_text().rfind('}')+1].replace('\\\\','\\')	# Adjust text slightly to fit JSON object
			data = json.loads(text)
			messages = list(reversed(data["messages"]))	# Create list of messages
			# Email recieved
			if (messages[0]["from"] in artistName):
				message_id = messages[0]["id"] 	# Grab email ID
				emailRecieved = True			# Stop loop
				print('Email Recieved! Visiting DL link.')
				break							# Just in case
			time.sleep(5)
		# Go to specific email through API
		time.sleep(5)
		response = urllib.request.urlopen('https://api.mailinator.com/api/email?msgid='+message_id)
		html = str(response.read())
		soup = BeautifulSoup(html,'lxml')
		text = soup.get_text()
		link_start = text.find('http:')	# Find position of start of link
		link_end = find_nth(text,'&',4) # Find position of end of link
		link = text[link_start:link_end].replace('\\',"") 	# Parse link
		browser.visit(link) # Visit link
	else:	# No email required
		if (enterPrice == True):
			print('Email NOT required. Going to download page.')
			for button in browser.find_by_tag('button'):
				if (button.value == 'Download Now'):
					button.click() 		# Click OK
					break

	# --Download page reached--
	format = browser.find_by_id('downloadFormatMenu0').first # Open download format chooser
	format.click()

	# Switch to your desired download format
	for a in browser.find_by_tag('a'):
		if dl_format+' -' in a.value:
			a.click()
			print('Switching to '+dl_format+' format.')
			break

	# Print format being used
	format = browser.find_by_id('downloadFormatMenu0').first
	print('Format: '+format.value)

	# Wait while the download is being prepared...
	print('Preparing download.')
	while browser.is_text_present('preparing'):
		time.sleep(5)

	# Grab final download link
	downloadLink = browser.find_link_by_text('Download').first
	print('Got download link! Starting download...')
	url = downloadLink['href']
	file_name = wget.download(url)	# Download the link using wget

# Repeat for other albums in the list
