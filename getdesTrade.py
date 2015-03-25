#!/bin/env python
import os
import csv
import sys
import datetime
import time
import math
import globalfunc

destrddir=''
actholddir=''
desholddir=''
universedir=''

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

#cdatetime=time.strptime(cdate,"%Y%m%d")
#ldatetime=time.mktime(cdatetime)-82800
#ldate=time.strftime("%Y%m%d",time.localtime(ldatetime))
ldate=globalfunc.getLastDate(cdate)

print 'last date time is %s' % ldate

#=================================
#        get desire hold
#=================================
desholdname=desholddir+cdate+'.desHolding.csv'
print 'get desire hold %s' % desholdname
reader=csv.reader(file(desholdname,'r'))
next(reader)
for line in reader:
	desholddict[line[0]]=int(line[1])

#=================================
#     get BOD actual hold
#=================================
lactholdname=actholddir+cdate+'.actHoldingBOD.csv'
print 'get actual holding BOD %s' % lactholdname

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
	index=12
	if int(line[12])>0:
		index=12
	elif int(line[13])>0:
		index=13
	elif int(line[14])>0:
		index=14
	else:
		voldict[line[0]]=0
	voldict[line[0]]=int(line[index])

fname=universedir+cdate+'.desTrade.csv'
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
	if avgvol==0:
		durtime=0
	else:
		durtime=math.ceil((destrd/avgvol)*2)
	if(durtime<0):
		destrd=0
		etimestr=btimestr
		durtime=0
	else:
		etime=btime+durtime*60
		etimestr=time.strftime("%H%M",time.localtime(etime))
	fd.write("%s,%d,%s,%s,%d\n" % (key,destrd,btimestr,etimestr,durtime))

fd.close()

print 'Write finsh.'

