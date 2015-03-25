#!/bin/env python

import csv
import os
import sys
import datetime
import time
import globalfunc

print '----------get des hold-----------'

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
# get actual holding BOD
#=================================
reader = csv.reader(file(cdate+'.actHoldingBOD.csv','r'))
next(reader)
i=1
for line in reader:
	if i==1:
		cash=float(line[2])
	else:
		clsdict[line[0]]=float(line[2])

print 'cash:%s' % cash

#=================================
#    get the close price value
#=================================
clsdict={}
reader = csv.reader(file(ldate+'.dpx.csv','r'))
next(reader)
for line in reader:
	clsdict[line[0]]=float(line[6])

#=================================
#   write data to desire hold
#=================================
fname=cdate+'.desHolding.csv'
print 'write to %s' % fname
reader = csv.reader(file(cdate+'.weight.csv','rb'))
fd=open(fname,'w+')
fd.write('#tk,shares\n')
next(reader)#ignore the first line
for line in reader:
	tk=line[0]
	if clsdict.has_key(tk):
		shr=cash*float(line[1])/clsdict[tk]
	else:
		shr=0
	fd.write("%s,%d\n" % (tk,shr))

fd.close()

print 'write finish.'
