# Script that takes a domain, looks it up on wayback and parsers all the JS files for relative and absolute paths...

import requests
import re
import optparse
import json
import sys

#Arguments...
parser = optparse.OptionParser()
parser.add_option("-d", "--domain", action="store", dest="mDomain", help="Domain to query against", metavar="<domain.com>")
options, args = parser.parse_args()

if not options.mDomain:
	parser.error('Top level domain not specified')
else:
	mDomain = options.mDomain

# Set global vars
output = {}

# Find Relative paths RegEx...
relRegex = ur"((\"|\')(\/[\w\d\?\/&=\#\.\!:_-]*?)(\2))"
# Find Absolute paths RegEx...
abRegex = ur"(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?"

# Begin work here.
try:
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
		"&filter=" + wayBackOptions['filter'] + "&filter=mimetype:application/javascript" +
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

			url = data[0]

			# Do work here....
			response = requests.get(data[0], timeout=600)

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

	else:
		print "No Data Found for: " + mDomain + "\n"
					
except Exception as exception:
	# import traceback
	# print(traceback.format_exc())	
	print exception

