#!/bin/env python

import os
import sys

universedir='/cygdrive/z/data/WindDB/setting/'
universedir=''
if len(sys.argv)<2:
	print 'usage:./runrang.py [start date] [end date]'
	exit()

fd= open(universedir+'tradingDates.csv','r')
start=0
for line in fd:
	fdate=line[0:8]
	if start==1:
		os.system('./run.sh ' + fdate)
	if fdate==sys.argv[1]:
		start=1
		os.system('./run.sh ' + fdate)
	elif fdate==sys.argv[2]:
		os.system('./run.sh ' + fdate)
		break
