#!/bin/env python
import os
import csv
import sys
import datetime
import time
import math
import globalfunc

destrddir='/z/data/WindDB/production5/portfolio_liuyi/desTrade/'
actholddir='/z/data/WindDB/production5/portfolio_liuyi/actHolding/'
desholddir='/z/data/WindDB/production5/portfolio_liuyi/desHolding/'
universedir='/cygdrive/z/data/WindDB/setting/universe/'
#destrddir=''
#actholddir=''
#desholddir=''
#universedir=''

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
univername=universedir+cdate+'_universe.csv'
print 'get vol from %s' % univername
reader=csv.reader(file(univername,'r'))
next(reader)
for line in reader:
	index=13
	if int(line[13])>0:
		index=13
	elif int(line[14])>0:
		index=14
	elif int(line[15])>0:
		index=15
	else:
		voldict[line[0]]=0
	voldict[line[0]]=int(line[index])

fname=destrddir+cdate+'.desTrade.csv'
print 'Begin write data to %s' % fname

#=================================
#           write data
#=================================
fd=open(fname,'w+')
fd.write('#tk,desShr,desStartTime,desEndTime,desDuration,vol5\n')
btimestr='0940'
btime=time.mktime(time.strptime(btimestr,"%H%M"))
#put desholddict in order
desholdlist=sorted(desholddict.iteritems(),key=lambda asd:asd[0],reverse=False)
lactholdlist=sorted(lactholddict.iteritems(),key=lambda asd:asd[0],reverse=False)
i=0
j=0
desholdlen=len(desholdlist)
lactholdlen=len(lactholdlist)
while i<desholdlen or j < lactholdlen:
	key=''
	if i>=desholdlen:
		destrd=-lactholdlist[j][1]
		key=lactholdlist[j][0]
		j+=1
	elif j>= lactholdlen:
		key=desholdlist[i][0]
		destrd=desholdlist[i][1]
		i+=1
	else:
		deskey=desholdlist[i][0]
		desshr=desholdlist[i][1]
		lactshr=lactholdlist[j][1]
		lactkey=lactholdlist[j][0]
		if deskey == lactkey:
			key=deskey
			destrd=desshr-lactshr
			i+=1
			j+=1
		elif deskey >lactkey:
			key=lactkey
			destrd=-lactshr
			j+=1
		elif deskey < lactkey:
			key=deskey
			destrd=desshr
			i+=1
	if destrd>0:
		destrd-=destrd%100
	avgvol=voldict[key]*0.05/240
	durtime=0
	if avgvol==0:
		durtime=0
	if durtime < 10 and durtime != 0:
		durtime = 10
	if(durtime<0):
		destrd=0
		etimestr=btimestr
		durtime=0
	elif durtime>=110:
		etime=btime+durtime*60+90
		etimestr=time.strftime("%H%M",time.localtime(etime))
	else:
		etime=btime+durtime*60
		etimestr=time.strftime("%H%M",time.localtime(etime))
	if destrd != 0 and abs(destrd)>300:
		fd.write("%s,%d,%s,%s,%d,%d\n" % (key,destrd,btimestr,etimestr,durtime,voldict[key]))

fd.close()

print 'Write finish.'

