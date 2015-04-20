# -*- coding: utf-8 -*-

import scraperwiki
import urllib2
import urllib
import urlparse
from datetime import datetime
from bs4 import BeautifulSoup

# Set up variables
entity_id = "E0201_LBC_gov"
url = "http://www.luton.gov.uk/Business/Doing%20business%20with%20the%20council/Business_procurement/councilspend/Pages/default.aspx"

# Set up functions
def convert_mth_strings ( mth_string ):
	month_numbers = {'JAN': '01', 'FEB': '02', 'MAR':'03', 'APR':'04', 'MAY':'05', 'JUN':'06', 'JUL':'07', 'AUG':'08', 'SEP':'09','OCT':'10','NOV':'11','DEC':'12' }
	#loop through the months in our dictionary
	for k, v in month_numbers.items():
		#then replace the word with the number
		mth_string = mth_string.replace(k, v)
	return mth_string

# pull down the content from the webpage
html = urllib2.urlopen(url)
soup = BeautifulSoup(html)

# find all entries with the required class
block = soup.find('ul', {'class':'lutonarrowblack'})
pageLinks = block.findAll('a', href=True)

for pageLink in pageLinks:
	pageUrl = 'http://www.luton.gov.uk' + pageLink['href']
	pageUrl = pageUrl.replace(' ','%20')
	
	html2 = urllib2.urlopen(pageUrl)
	soup2 = BeautifulSoup(html2)
	
	fileLinks = soup2.findAll('a', href=True)
	
	for fileLink in fileLinks:
		url = fileLink['href']
		parsed_link = urlparse.urlsplit(url.encode('utf8'))
		parsed_link = parsed_link._replace(path=urllib.quote(parsed_link.path))
		encoded_link = parsed_link.geturl()
		if encoded_link.startswith('/Council_government_'):
			encoded_link = 'http://www.luton.gov.uk'+encoded_link
			
		if '.xls' in url:
			# create the right strings for the new filename
			title = fileLink.text
			csvYr = title.split(' ')[1]
			csvMth = title.split(' ')[0][:3]
			csvMth = csvMth.upper()
			csvMth = convert_mth_strings(csvMth);
			filename = entity_id + "_" + csvYr + "_" + csvMth + ".csv"
			todays_date = str(datetime.now())
			scraperwiki.sqlite.save(unique_keys=['l'], data={"l": encoded_link, "f": filename, "d": todays_date })
			print filename
