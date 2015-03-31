#!/bin/env python

import os
import sys
import time
import datetime

fdatedir='/z/data/WindDB/setting/'
#fdatedir=''
fname='tradingDates.csv'

def getNextDate(cdate):
	reader=open(fdatedir+fname,'r')
	nextone=0
	ndate=''
	for line in reader:
		if nextone==1:
			ndate=line[0:8]
			break
		if line[0:8]==cdate:
			nextone=1
	return ndate

def getLastDate(cdate):
	reader=open(fdatedir+fname,'r')
	nextone=0
	ldate=reader.readline()
	next(reader)
	for line in reader:
		if line[0:8]==cdate:
			return ldate
		else:
			ldate=line[0:8]
	return -1

#=================================
#   dtime:duration time(minuite)
#=================================
def CalEndTime(btimestr,durtime):
	if durtime>110:
		durtime+=90
	durtime=durtime*60
	btime=time.mktime(time.strptime(btimestr,"%H%M"))
	etimestr=btimestr
	if(durtime<0):
		etimestr=btimestr
		durtime=0
	elif durtime==0:
		durtime+=60
	else:
		etime=btime+durtime
		etimestr=time.strftime("%H%M",time.localtime(etime))
	return etimestr


