#!/bin/env python

import os
import sys

fdatedir='/z/data/WindDB/setting/'
fdatedir=''
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


