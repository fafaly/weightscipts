#!/bin/env python
import csv
import os
import sys
import datetime
import time

print '----------get actual hold-----------'

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
#    get last date's actual hold
#=================================
print "Begin get last date's actual hold"
lactholdname=ldate+'.actHold.csv'
actholddict={}
reader=csv.reader(file(lactholdname))
next(reader)
i=0
cash=0
for line in reader:
	if i==1:
		cash=float(line[1])
		i+=1
		continue
	actholddict[line[0]]=int(line[1])
	i+=1

#=================================
# get today's actual trade and avpx
#   calculate the tax fare
#   calculate cash
#=================================
print 'Begin calculate tax fare and cash'
comtax=0
stamptax=0
transtax=0
tcash=0
lactholdname=cdate+'.actTrd.csv'
acttrddict={}
actclsdict={}
reader=csv.reader(file(lactholdname,'r'))
next(reader)
for line in reader:
	shr=int(line[1])
	avgpx=float(line[5])
	if actholddict.has_key(line[0]):
		actholddict[line[0]]+=shr
	else:
		actholddict[line[0]]=shr
	happencash=shr*avgpx
	comtax+=abs(happencash)*2.5/10000
	if shr<0:
		stamptax+=-shr*0.001
	if line[0][0]=='6':
		transtax+=abs(happencash)*6/10000
	tcash+=happencash	
cash+=tcash-comtax-stamptax-transtax

#=================================
#    get today's close price value
#=================================
clsdict={}
reader = csv.reader(file(cdate+'.dpx.csv','r'))
next(reader)
for line in reader:
	clsdict[line[0]]=float(line[6])


#=================================
#	calculate today's actual hold
#=================================
fname=cdate+'.actHold.csv'
print 'Begin to write %s' % fname
fd=open(fname,'w+')
fd.write('#tk,shr\n')
fd.write('CASH,%f\n' % cash)
holdpnl=0
for key in actholddict:
	fd.write("%s,%s\n" % (key,actholddict[key]))
	if clsdict.has_key(key):
		holdpnl+=actholddict[key]*clsdict[key]
	else:
		print 'clsdict has not key:%s' % key

fd.close()
print 'write finish.'
	
pnlname=cdate+'.pnl.csv'
print 'Begin to write %s' % pnlname
fd=open(pnlname,'w+')
fd.write("#holdpnl,tradepnl,comtax,stamptax,transtax,leftcash\n")
fd.write("%f,%f,%f,%f,%f,%f\n" % (holdpnl,tcash,comtax,stamptax,transtax,cash))

fd.close()
print 'write finish.'
