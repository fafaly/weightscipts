#!/bin/env python
import csv
import os
import sys
import datetime
import time
import globalfunc

cacsdir='/z/data/WindTerminal/cacs/old/'
actholdingdir='/z/data/WindDB/production5/portfolio_liuyi/actHolding/'
scacsdir='/z/data/WindDB/production5/portfolio_liuyi/cacs/'
#cacsdir=''
#actholdingdir=''
#scacsdir=''

print '----------get actual hold BOD-----------'

if(len(sys.argv)==1):
	now=datetime.datetime.now()
	cdate = now.strftime("%Y%m%d")
else:
	cdate = sys.argv[1]

print 'date time is %s' % cdate

#cdatetime=time.strptime(cdate,"%Y%m%d")
#ndatetime=time.mktime(cdatetime)+86400
#ndate=time.strftime("%Y%m%d",time.localtime(ndatetime))
ndate=globalfunc.getNextDate(cdate)


print 'next date time is %s' % ndate

#=================================
#    get cacs ratio
#=================================
cacsdict={}
cacsname=cacsdir+cdate+'.cacs.csv'
print 'Get ratio of %s' % cacsname
reader=csv.reader(file(cacsname,'r'))
next(reader)
for line in reader:
	if line[3]=='':
		vol1=0
	else:
		vol1=float(line[3])
	if line[5]=='':
		vol2=0
	else:
		vol2=float(line[5]	)
	if line[7]=='':
		vol3=0
	else:
		vol3=float(line[7])
	cacsdict[line[0][0:6]]=vol1/10+vol2/10+vol3/10

fname=scacsdir+cdate+'.ratio.csv'
fd=open(fname,'w+')
fd.write('#tk,ratio\n')
for key in cacsdict:
	fd.write("%s,%d\n" % (key,cacsdict[key]))

fd.close()

#=================================
#    get actual holding BOD
#=================================
print 'Begin read actual holding EOD and calcute the BOD'
fname = actholdingdir+ndate + '.actHoldingBOD.csv'
print 'Begin to write %s' % fname
fd = open(fname,'w+')
actEOD = actholdingdir + cdate+'.actholdingEOD.csv'
reader=csv.reader(file(actEOD,'r'))
for line in reader:
	if cacsdict.has_key(line[0]) and line[1]!='0':
		tk=line[0]
		shr=int(line[1])*(1+cacsdict[line[0]])
		cls=float(line[1])*float(line[2])/shr
		fd.write("%s,%d,%s\n" % (tk,shr,cls))
	else:
		fd.write("%s,%s,%s\n" % (line[0],line[1],line[2]))

fd.close()
print 'write finish'
