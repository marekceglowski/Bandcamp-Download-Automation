from splinter import Browser
import urllib.request
import codecs
import time
import json
import wget
import uuid
import hashlib

##########
# Bandcamp Bulk Album Downloader
# 
# This script will download free albums from BandCamp without user-interaction.
# Note: This script does NOT rip audio from BandCamp pages, it just automates the
# process of downloading albums for use on headless servers.
# 
##########


list_file = 'links.ini'  # File with list of BandCamp URLs separated by newlines.
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
	
content = []	# Open file with list of BandCamp albums to download
with open(list_file) as f:
    content = f.readlines()

browser = Browser('phantomjs')
for album in content:
	url = album.replace("\n","")
	print('URL: '+album)
	browser.visit(url)
	#time.sleep(3)
	artistName = browser.find_by_id('band-name-location')[0].value.split('\n')[0] 	# Get artist name from top-right
	print('Getting artist name.')													# Will be used in the email portion

	# Check download's type (either says 'Buy Now (name your price)' or 'Free Download')
	for b in browser.find_by_tag('button'):					# Go through page's buttons
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

	# If Buy Now (name your price)
	if (enterPrice == True):
		browser.find_by_id('userPrice').first.fill('0') # Fill $0 as price to pay
		
	# If email required
	if browser.is_text_present('Email a link to my free download'):
		print('Email required. Generating mail address.')
		response = urllib.request.urlopen('http://api.temp-mail.ru/request/domains/format/json')	# Get possible email domains
		html = str(response.read().decode("utf-8"))													# Decode bytes
		data = json.loads(html)																		# Decode JSON
		email_domain = data[0]																		# Grab first domain
		email_name = "a"+str(uuid.uuid4()).replace("-","")[0:7]+""+data[0]				# Generate temporary email
		email_md5 = hashlib.md5(email_name.encode('utf-8')).hexdigest()					# Generate MD5 hash for email service API
		print('Email Name: '+email_name+', Email MD5: '+email_md5+', Goto temp-mail.org for more info.')
		print('Giving generated email address to Bandcamp.')
		browser.find_by_id('fan_email_address').first.fill(email_name) 					# Fill email field
		browser.find_by_id('fan_email_postalcode').first.fill('111111') 				# Fill postal code field
		for button in browser.find_by_tag('button'):
			if (button.value == 'OK'):
				button.click() 		# Click OK
				break
		# Go to disposable mail API
		print('Waiting for email...')
		link = ''				# Variable for download link
		found = False			# Will stop while loop
		while found == False:
			try:
				time.sleep(5)
				response = urllib.request.urlopen('http://api.temp-mail.ru/request/mail/id/'+email_md5+'/format/json/')	# Request mailbox JSON
				html = str(response.read().decode("utf-8"))
				data = json.loads(html)
				# Email received if reach here
				for item in data:									# Check all emails
					if (artistName in item["mail_from"]):			# If artist name found in email from
						text = item['mail_text_only']					# Get mail text
						link_start = text.find('http:')					# Find position of start of download link
						link_end = find_nth(text,'&',4) 				# Find position of end of link
						link = text[link_start:link_end].replace('\\',"") 	# Parse link
						found = True
			except:	# Email not yet received will throw 404 error
				pass
		# Go to specific email through API
		time.sleep(5)
		print('Download page link found! Going to link.')
		browser.visit(link) # Visit link
	else:	# No email required (much simpler)
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
