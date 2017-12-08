#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import parsedatetime
from datetime import *


def parsenumberlist(string):
    """
    Take strings like '0, 1, 15-20' and return 
    sorted lists with all inbetween items like
    this: [0, 1, 15, 16, 17, 18, 19, 20]
    Unfitting input is ignored
    Everything longer than an int will become a long
    """
    # Find ranges like 0-15 or 30-10
    ranges = re.findall("\d+\s*\-\s*\d+", str(string))
    # Remove already found ranges from string
    string = re.sub("\d+\s*\-\s*\d+", "", str(string))
    # In the rest search for normal numbers
    singlenumbers = re.findall("(\d+)", str(string))
    # Convert all to int
    singlenumbers = [int(x) for x in singlenumbers]
    # Iterate through the ranges and append the numbers to rangenumbers
    rangenumbers = []
    for r in ranges:
        values = [int(x) for x in r.replace(" ", "").split("-")]
        for value in range(min(values),max(values)+1):
            rangenumbers.append(value)
    # Join single numbers and ranges and sort them
    allnumbers = rangenumbers + singlenumbers
    allnumbers.sort()
    return allnumbers




def parsetime(string):
    """
    Parse humanreadable text and return a datetime
	Return now if unreadable input
    """
    cal = parsedatetime.Calendar()
    time_struct, parse_status = cal.parse(string)
    return datetime(*time_struct[:6])


def parsefilters(string):
	# Return a dict of filters (logical AND)
	string = str(string)
	# Set a default dict for filters:
	filters = {"all":False, "status":[], "tags":[], 
		"groups":[], "description":[], "tasknumbers":[]}
	
	# Find "all" or "*" return filters (no need to search further)
	allmatches = re.findall("all|\*", str(string).lower())
	if len(allmatches) > 0:
		filters["all"] = True
		return filters

	# Find statuses (new, due, etc) and add to filters
	statusmatches = re.findall("\s*(current|new|due|overdue|neglected|done|deleted|marked)", str(string).lower())
	filters["status"] = statusmatches
	# Remove matches from string
	for match in statusmatches: string = string.replace(match, "")

	# Find Tags (#blah, #Tag) and add to filters
	tagmatches = re.findall("#\w+", str(string))
	filters["tags"] = tagmatches
	# Remove matches from string
	for match in tagmatches: string = string.replace(match, "")

	# Find group (@Group) and add to filters, avoid catching emailadresses
	groupmatches = re.findall("\s@\w+", str(string))
	filters["groups"] = [groupmatch.lstrip() for groupmatch in groupmatches]
	# Remove matches from string
	for match in groupmatches: string = string.replace(match, "")

	# Find numberlist and add to filters
	tasknumbermatches = parsenumberlist(string)
	filters["tasknumbers"] = tasknumbermatches
	# Remove Ranges from string
	string = re.sub("\d+\s*\-\s*\d+", "", string)
	# Remove matched numbers from string
	for match in groupmatches: string = string.replace(str(match), "")

	# Find Description in remaining string (Fuzzy matching)
	descriptionmatches = re.findall("^\.+|\s+.+", string.lower())
	descriptionmatches = [x.replace(",", "") for x in descriptionmatches]
	filters["description"] = [x.lstrip() for x in descriptionmatches]
	return filters




if __name__ == "__main__":
	testparsenumberlist = False
	testparsetime = False
	testparsefilters = True
	# Run some tests on parsenumberlist
	if testparsenumberlist:
		print("="*30+" [parsenumberlist] "+"="*30+"\n\n")
		inputvariables = ["0", 0, "lol", "0-8", "100, 999, 1, 2", "0  ,   5 - 7,60    -58"]
		for testnumber, inputvariable in enumerate(inputvariables):
			print("\t[parsenumberlist][Test Nr.: "+str(testnumber).zfill(3)+"] Output for input: \""+str(inputvariable)+"\" (type: "+str(type(inputvariable))+")")
			for i, item in enumerate(parsenumberlist(inputvariable)):
				print("\t\t["+str(i)+"] "+str(item)+" (type: "+str(type(item))+")")
			print("\n")

	# Run some tests on parsetime
	if testparsetime:
		print("="*30+" [parsetime] "+"="*30+"\n\n")
		inputvariables = ["tomorrow", "tomorrow 12:00", "next month", "dsafasg"]
		for testnumber, inputvariable in enumerate(inputvariables):
			print("\t[parsetime][Test Nr.: "+str(testnumber).zfill(3)+"] Output for input: \""+str(inputvariable)+"\" (type: "+str(type(inputvariable))+")")
			item = parsetime(inputvariable)
			print("\t\t"+str(item)+" (type: "+str(type(item))+")")
		print("\n")

	# Run some tests on parsefilters
	if testparsefilters:
		print("="*30+" [parsefilters] "+"="*30+"\n\n")
		inputvariables = ["0 @Testgroup david@huss.at", "0-4, #hashtag", "all", "overdue", "new, 1-5 overdue, due #friends #bullshit Kuchen backen, afd wählen"]
		for testnumber, inputvariable in enumerate(inputvariables):
			print("\t[parsefilters][Test Nr.: "+str(testnumber).zfill(3)+"] Output for input: \""+str(inputvariable)+"\" (type: "+str(type(inputvariable))+")")
			item = parsefilters(inputvariable)
			print("\t\t"+str(item)+" (type: "+str(type(item))+")")
		print("\n")