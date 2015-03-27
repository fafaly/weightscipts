#!/bin/env python

import csv
import os
import sys
import datetime
import time
import globalfunc


actholddir='/z/data/WindDB/production5/portfolio_liuyi/actHolding/'
desholddir='/z/data/WindDB/production5/portfolio_liuyi/desHolding/'
weightdir='/z/data/WindDB/production5/portfolio_liuyi/weight/'
universedir='/z/data/WindDB/setting/universe/'
#actholddir=''
#desholddir=''
#weightdir=''
#dpxdir=''

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
reader = csv.reader(file(actholddir+cdate+'.actHoldingBOD.csv','r'))
next(reader)
i=1
clsdict={}
for line in reader:
	if i==1:
		cash=float(line[2])
		i=i+1
	else:
		clsdict[line[0]]=float(line[2])

print 'cash:%s' % cash

#=================================
#    get the close price value
#=================================
clsdict={}
reader = csv.reader(file(universedir+cdate+'_universe.csv','r'))
next(reader)
for line in reader:
	clsdict[line[0]]=float(line[50])

#=================================
#   write data to desire hold
#=================================
fname=desholddir+cdate+'.desHolding.csv'
print 'write to %s' % fname
reader = csv.reader(file(weightdir+cdate+'.weight.csv','rb'))
fd=open(fname,'w+')
fd.write('#tk,shr,lastGoodCls\n')
next(reader)#ignore the first line
for line in reader:
	tk=line[0]
	if clsdict.has_key(tk):
		shr=cash*float(line[1])/clsdict[tk]
		shr-=shr%100
	else:
		shr=0
	fd.write("%s,%d,%f\n" % (tk,shr,clsdict[tk]))

fd.close()

print 'write finish.'
