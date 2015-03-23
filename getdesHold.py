#!/bin/env python

import csv
import os
import sys
import datetime
import time

print '----------get des hold-----------'

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
#       get the cash value
#=================================
reader = csv.reader(file(ldate+'.actHold.csv','rb'))
next(reader)
for line in reader:
	cash=float(line[1])
	break

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
fname=cdate+'.desHold.csv'
print 'write to %s' % fname
reader = csv.reader(file(cdate+'.000300_wt.csv','rb'))
fd=open(fname,'w+')
fd.write('#tk,shares\n')
next(reader)#ignore the first line
for line in reader:
	tk=line[1][0:6]
	if clsdict.has_key(tk):
		shr=cash*float(line[4])/clsdict[tk]
	else:
		shr=0
	fd.write("%s,%d\n" % (tk,shr))

fd.close()

print 'write finish.'
