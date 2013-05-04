#!/usr/bin/python

# XKCD JSON scraper and image processor
# Myles Harrison
# April 6, 2013

import os
import urllib2
import json
import csv
import datetime
from datetime import date
from PIL import Image
from PIL import ImageStat


# Fetch the comic JSON (metadata)
def fetch_comic(comic_id):
	# Create the url
	url = 'http://xkcd.com/' + str(comic_id) + '/info.0.json'
		
	# Open the URL and download the JSON
	response = urllib2.urlopen(url)
	
	# Read the response and return the dictionary created from the JSON
	xkcd_json = response.read()
	jdict = json.loads(xkcd_json)
	return jdict

# Process image
def process_comic(jdict):
	# Get the image url and comic number
	imgurl = str(jdict['img'])
	comicnum = jdict['num']

	# Download the image
	r = urllib2.urlopen(imgurl)
	imagedata = r.read()

	# Save the image to file
	filename = str(os.path.join('.','img','%4.4d' % comicnum + '_' + os.path.basename(imgurl)))
	f = open(filename, 'w')
	f.write(imagedata)
	f.close()
	return filename

# Do image calculations and write to csv
def image_calcs(jdict, imagefile):

	# Open the image file
	im = Image.open(imagefile)

	# IMAGE DATA
	jdict['format'] = im.format # image format (filetype)	
	jdict['width'] = im.size[0] # image width
	jdict['height'] = im.size[1] # image height
	jdict['size'] = im.size[0]*im.size[1] # image area
	jdict['aspect'] = im.size[0]/float(im.size[1]) # aspect ratio
	jdict['mode'] = im.mode # image mode ('L' or 'RGB', etc.)
	jdict['filesize'] = os.stat(imagefile).st_size/float(1024.0) # filesize in kilobytes

	# Luminosity
	jdict['lumen'] = ImageStat.Stat(im).rms[0]

	# Convert the image to grayscale and take histogram
	h = im.convert('L').histogram()

	# Calculate the image 'sparseness' - percentage of non-white and white pixels
	jdict['nwpx'] = float(sum(h[0:-1]))/sum(h)
	jdict['wpx'] = float(h[-1])/sum(h)

	# COMIC DATA
	# convert from unicode to string
	ascii_fields = ('transcript','alt','safe_title','title')
	for j in ascii_fields:
		jdict[j] = jdict[j].encode('ascii','ignore')
	jdict = dict([(str(k), str(v)) for k, v in jdict.items()]) 

	# Remove special characters from the comic transcipt
	ts = jdict['transcript']
	alt = jdict['alt']
	special_chars = ['[',']','{','}']
	for i in special_chars:
		ts = ts.replace(i,'')
		alt = alt.replace(i,'')

	# newline & apostrophe
	ts = ts.replace('\n',' ').replace('\'','')
	alt = alt.replace('\n',' ').replace('\'','')

	# Remove the alt text from the transcript if it exists
	alt_ind = ts.lower().find('alt:')
	if (alt_ind != -1):
		ts = ts[0:alt_ind]

	jdict['transcript'] = ts
	jdict['alt'] = alt

	return jdict

def batch_process(start, end):

	# Process the comics listed and create a list of dictionaries
	l = []
	for i in range(start, end+1):
		print 'Fetching ' + str(i)
		try:
			j = fetch_comic(i)
		except:
			continue
		print 'Processing ' + str(i)
		k = process_comic(j)
		print 'Calculating ' + str(i)
		d = image_calcs(j, k)
		l.append(d)
	
	# Open a file for writing
	f = open('xkcd_data.csv', 'w')

	# List of fields (in sane order)
	fieldnames = ['num','img','title','safe_title','day','month','year','news','link','transcript',
		'alt','format','mode','filesize','width','height','aspect','size','nwpx','wpx','lumen']
	
	# Write the list of dictionaries to a file
	print 'Writing to file...'
        dictwrite = csv.DictWriter(f, fieldnames, restval='', extrasaction='ignore')
	dictwrite.writer.writerow(fieldnames)
	dictwrite.writerows(l)

	# Close the file
	f.close()



	





















