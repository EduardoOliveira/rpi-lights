#!/usr/bin/python

import bluetooth
import time
from main import light

while True:
    print "Checking " + time.strftime("%a, %d %b %Y %H:%M:%S", time.gmtime())

    result = bluetooth.lookup_name('7C:F9:0E:A4:85:0A', timeout=5)
    if (result != None):
	light({"r":0,"g":255,"b":0})
	print "Welcome Home!"
	
    time.sleep(10)


