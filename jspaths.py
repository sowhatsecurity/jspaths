# Script that takes a domain, looks it up on wayback and parsers all the JS files for relative and absolute paths...

import requests
import re
import optparse
import json
import sys

#Arguments...
parser = optparse.OptionParser()
parser.add_option("-d", "--domain", action="store", dest="mDomain", help="Domain to query against", metavar="<domain.com>")
parser.add_option("-p", "--path", action="store", dest="mPath", help="Custom Path (Bypass Wayback Check)", metavar="<https://something.com/js/path>")
parser.add_option("-c", "--content", action="store", dest="mContentType", help="Content Type for Wayback Query", metavar="<text/html>")

options, args = parser.parse_args()

mDomain = ""
mPath = ""
mContentType = "application/javascript"

if options.mDomain:
	mDomain = options.mDomain

if options.mPath:
	mPath = options.mPath

if options.mContentType:
	mContentType = options.mContentType

if not options.mDomain and not options.mPath:
	parser.error("Please specifiy -d or -p")


# Set global vars
output = {}

# Find Relative paths RegEx...
relRegex = ur"((\"|\')(\/[\w\d\?\/&=\#\.\!:_-]*?)(\2))"
# Find Absolute paths RegEx...
abRegex = ur"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"


def performCheck(data):
	url = data

	# Do work here....
	response = requests.get(url, timeout=600, verify=False)

	# Only proceed if the server returns the js file!
	if response.status_code == 200:
		data = {}
		data['rel'] = {}
		data['ab'] = {}
	
		# Relative paths
		relMatches = re.findall(relRegex, response.text)

		for item in relMatches:
			data['rel'][item[2]] = item[2]

			# Absolute paths
			abMatches = re.findall(abRegex, response.text)

			for item in abMatches:
				fullURL = item[0] + "://" + item[1] + item[2]
				data['ab'][fullURL] = fullURL

		# Record the output for this file path
		if all(data.values()):

			# If you want to process the data later, or store in a file, use the output var
			#	output[url] = data

			print "\n----------------------------------------------------------------------------------"
			print url + "\n----------------------------------------------------------------------------------"
				
			# Print out the data
			print "\n****REL****\n"
			for item in data['rel']:
				print item
			print "\n****AB****\n"
			for item in data['ab']:
				print item

		# Flush the output, this forces the buffer to display on the web page, rather than waiting till the end.
		sys.stdout.flush()


# Begin work here.
try:

	if(mDomain):
		wayBackURL = "http://web.archive.org/cdx/search/cdx"
		wayBackSearch = mDomain + "/*"
		wayBackOptions = {
			"output":"json",
			"fl":"original",
			"collapse":"urlkey",
			"filter":"!statuscode:404",
			"limit":"2000000"
		}

		wayBackQuery = (wayBackURL +
			"?url=" + wayBackSearch +
			"&output=" + wayBackOptions['output'] +
			"&fl=" + wayBackOptions['fl'] +
			"&collapse=" + wayBackOptions['collapse'] +
			"&filter=" + wayBackOptions['filter'] + "&filter=mimetype:" + mContentType +
			"&limit=" + wayBackOptions['limit'])

		print "\nRunning query: " + wayBackQuery + "\n"
		sys.stdout.flush()

		# Execute Wayback Query
		wayBackReturn = requests.get(wayBackQuery, timeout=600)	
		wayBackResults = json.loads(wayBackReturn.text)

		# Work through Wayback results
		if wayBackResults:

			print "\nQuery Complete. Parsing Reuslts..."
			sys.stdout.flush()

			wayBackResults.pop(0)

			for data in wayBackResults:
				performCheck(data[0])

		else:
			print "No Data Found for: " + mDomain + "\n"

	if(mPath):
		performCheck(mPath)
					
except Exception as exception:
	# import traceback
	# print(traceback.format_exc())	
	print exception

