#!/usr/bin/python

# Quick parser to fix garmin tcx files that have wildly fluctuating time stamps
# It requires 2 command line arguments - input file, and output file

from xml.dom.minidom import parse, parseString #for tcx parsing
import datetime # for date/time functions
import sys, getopt # for command line args
import os.path

def usage():
	print 'usage: tcxFixer.py -i <inputfile> -o <outputfile>' 

def main(argv):

	# Gets the command line options

	inputFile = ''
	outputFile = ''
	iFound = False
	oFound = False
	fixedFlag = False

	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError, err:
		usage()
		sys.exit(2)

	for opt, arg in opts:
		if opt == "-h":
			usage()
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputFile = arg
			iFound = True
		elif opt in ("-o", "--ofile"):
			outputFile = arg
			oFound = True
	if not iFound or not oFound:
		usage()
		sys.exit(2)

	# checks input file exists
	if not os.path.isfile(inputFile):
		print inputFile + " does not exist"
		sys.exit(2)

	try:
		xmldoc = parse(inputFile) # source
		nodes = xmldoc.getElementsByTagName('Time') # get all the time nodes
	except:
		print "Unable to parse " + inputFile
		sys.exit(2)

	i = 0 # counter for the for loop

	# Parse through the tcx file time nodes

	for node in nodes:

		# Get the time in the node

		OrigTime = node.firstChild.nodeValue

		# Check to make sure the delta from the previous time is 1 second

		if i > 0:
			# i.e. this is not the first node
			
			# get the value of the previous node
			prevTime = nodes[i-1].firstChild.nodeValue

			# Convert the times
			OrigTime = datetime.datetime.strptime(OrigTime, "%Y-%m-%dT%H:%M:%S.%fZ")
			prevTime = datetime.datetime.strptime(prevTime, "%Y-%m-%dT%H:%M:%S.%fZ")

			# Calculate the delta between the previous node and the current node
			nodeDelta = OrigTime - prevTime
			nodeDelta = nodeDelta.total_seconds() - 1

			if nodeDelta > 1:
				# i.e. there is more than 1 second between the previous node and this node
				# it needs fixing, so lets figure out the new time
				newTime = OrigTime - datetime.timedelta(seconds=nodeDelta)

				# now convert it back to a string

				textTime = datetime.datetime.strftime(newTime, "%Y-%m-%dT%H:%M:%S.%fZ")

				# dirty string fix to remove extra microseconds

				textTime = textTime.replace("000000", "000")

				print("Fixing: " + str(OrigTime) + " to " + textTime)

				# Write the fix to the dom

				node.firstChild.replaceWholeText(textTime)

				# Set flag as something was done
				fixedFlag = True

		i = i + 1 # used to get the index of the node we are parsing

	# write out the new tcx file
	
	if fixedFlag:
		try:
			f = open(outputFile, 'w')
			xmldoc.writexml( f )
			f.close()
			print 'Fixed tcx written to' + outputFile
		except IOError:
			print 'Unable to write Output File: ' + outputFile
			sys.exit(2)
	else:
		print 'Nothing needed to be done. Nothing written out.'
		sys.exit()

if __name__ == "__main__":
   main(sys.argv[1:])