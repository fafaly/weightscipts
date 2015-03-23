#!/bin/env python
import os
import csv
import sys
import datetime
import time

desholddict={}
lactholddict={}
voldict={}

print '----------get des trade-----------'

if(len(sys.argv)==1):
	now=datetime.datetime.now()
	cdate = now.strftime("%Y%m%d")
else:
	cdate = sys.argv[1]

print 'date time is %s' % cdate

cdatetime=time.strptime(cdate,"%Y%m%d")
ldatetime=time.mktime(cdatetime)-82800
ldate=time.strftime("%Y%m%d",time.localtime(ldatetime))

print 'last date time is %s' % ldate

#=================================
#        get desire hold
#=================================
desholdname=cdate+'.desHold.csv'
print 'get desire hold %s' % desholdname
reader=csv.reader(file(desholdname,'r'))
next(reader)
for line in reader:
	desholddict[line[0]]=int(line[1])

#=================================
#     get last date actual hold
#=================================
lactholdname=ldate+'.actHold.csv'
print 'get last date actual hold %s' % lactholdname

reader=csv.reader(file(lactholdname,'r'))
next(reader)
next(reader)
if reader:
	for line in reader:
		lactholddict[line[0]]=int(line[1])

#=================================
#            get vol
#=================================
univername=ldate+'_universe.csv'
print 'get vol from %s' % univername
reader=csv.reader(file(univername,'r'))
next(reader)
for line in reader:
	voldict[line[0]]=int(line[12])

fname=cdate+'.desTrade.csv'
print 'Begin write data to %s' % fname

#=================================
#           write data
#=================================
fd=open(fname,'w+')
fd.write('#tk,shr,BOT,EOT,duration\n')
btimestr='0940'
btime=time.mktime(time.strptime(btimestr,"%H%M"))
for key in desholddict:
	if lactholddict.has_key(key):
		destrd=desholddict[key] - lactholddict[key]
	else:
		destrd=desholddict[key]
	avgvol=voldict[key]*0.05/240
	durtime=(destrd/avgvol)*60
	if(durtime<0):
		destrd=0
		etimestr=btimestr
		durtime=0
	elif durtime==0:
		durtime+=60
	else:
		etime=btime+durtime
		etimestr=time.strftime("%H%M",time.localtime(etime))
	fd.write("%s,%d,%s,%s,%d\n" % (key,destrd,btimestr,etimestr,durtime/60))

fd.close()

print 'Write finsh.'

