#!/usr/bin/python
#
# AjaxHandler.py
# Based on the AjaxHandler.php written by Nexocentric
#

import time
import datetime
import sys
import os.path
import random

import json
import cgi

# for cgi debugging
import cgitb
cgitb.enable()


# Modify this to be your web server's document path
# webDocumentPath = "/var/www/public/"            
webDocumentPath = "/Library/WebServer/Documents/" # Mac OS Apache server

# Get POST headers
form = cgi.FieldStorage()

# Function Definitions
# Check POST header for value or use default
def checkPost(cgivarname, default=None):
    try:
        temp = form[cgivarname].value
    except KeyError:
        temp = default
    return temp

# Convert CSV to dictionary
def stringToDictionary(string):
    if string:
        keypairs = string.split(",")
        dictionary = {}
        for item in keypairs:
            key, value = item.split(":")
            dictionary[key] = value
        return dictionary
    else:
        return {}

# String to Tuple
def stringToTuple(string):
    if string:
        return string.split(",")
    else:
        return None

# Dictionary to String
def compressDictionaryToString(dictionary):
    if dictionary:
        myList = []
        for key, value in dictionary.items():
            myList.append("" + str(key) + ":" + str(value))
        return ",".join(myList)
    else:
        return ""

# Execution starts here

timeout = int(checkPost("timeout", 300)) # 5 minutes timeout if not specified
monitorList = stringToTuple(checkPost("monitorList"))
previousUpdateStatusList = stringToDictionary(checkPost("previousUpdateStatusList"))

# Create JSON response
# a variable named "updateStatus" is expected by our JS
updateStatus = "updateStatus"
response = {
        updateStatus: False,
        }

#if random.randint(1, 4) == 1:
#    response["updateStatus"] = True
#    response["newValue"] = "hello!"

# Loop until timeout is reached
starttime = time.time()
respondbreak = False
while ((time.time() - starttime) < timeout) and not respondbreak:
    if monitorList is not None:
        for file in monitorList:
            lastMtime = str(os.path.getmtime(os.path.join(webDocumentPath, file)))
            if not file in previousUpdateStatusList:
                previousUpdateStatusList[file] = lastMtime
                respondbreak = True
            elif previousUpdateStatusList[file] != lastMtime:
                previousUpdateStatusList[file] = lastMtime
                response[updateStatus] = True
                respondbreak = True
    time.sleep(1)

response["previousUpdateStatusList"] = compressDictionaryToString(previousUpdateStatusList)
result = json.dumps(response)
time_format = "%a, %d %b %Y %H:%M:%S %Z"
print "Content-Type: application/json"
print "Expires: Tue, 01 Jan 2000 00:00:00 GMT"
print "Last-Modified: %s" % (
        datetime.datetime.now().strftime(time_format)
        )
print "Cache-Control: no-store, no-cache, must-revalidate, max-age=0"
print "Cache-Control: post-check=0, pre-check=0"
print "Pragma: no-cache"
print 
print result
print
