#!/bin/env python
import csv
import os
import sys
import datetime
import time
import globalfunc
#dpxdir='/z/data/WindTerminal/dpx/'

actholddir='/z/data/WindDB/production5/portfolio_liuyi/actHolding/'
acttrddir='/z/data/WindDB/production5/portfolio_liuyi/actTrade/'
spnldir='/z/data/WindDB/production5/portfolio_liuyi/pnl/'
universedir='/z/data/WindDB/setting/universe/'
#dpxdir=''
#actholddir=''
#acttrddir=''
#spnldir=''


print '----------get actual hold EOD-----------'

if(len(sys.argv)==1):
	now=datetime.datetime.now()
	cdate = now.strftime("%Y%m%d")
else:
	cdate = sys.argv[1]

print 'date time is %s' % cdate

#cdatetime=time.strptime(cdate,"%Y%m%d")
#ldatetime=time.mktime(cdatetime)-82800
#ldate=time.strftime("%Y%m%d",time.localtime(ldatetime))
ndate=globalfunc.getNextDate(cdate)

print 'next date time is %s' % ndate

#=================================
#    get next date's price
#=================================
clsdict={}
uniname=universedir+ndate+'_universe.csv'
reader = csv.reader(file(uniname,'r'))
next(reader)
for line in reader:
	clsdict[line[0]]=float(line[50])


#=================================
#    get actual hold BOD
#=================================
print "Begin get date's BOD actual hold"
acttradename=actholddir+cdate+'.actHoldingBOD.csv'
actholddict={}
reader=csv.reader(file(acttradename))
next(reader)
i=0
cash=0
lcash=0
lholdpnl=0
for line in reader:
	if i==0:
		cash=float(line[2])
		lcash=cash
		i+=1
	else:
		shr=int(line[1])
		cls=float(line[2])
		actholddict[line[0]]=shr
		lholdpnl+=shr*cls

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
nbuy=0
buyamt=0
nsell=0
sellamt=0
nstock=0
tradepnl=0
acttradename=acttrddir+cdate+'.actTrade.csv'
acttrddict={}
reader=csv.reader(file(acttradename,'r'))
next(reader)
for line in reader:
	tk=line[0]
	shr=int(line[5])
	avgpx=round(float(line[9]),2)
	nstock+=1
	expx=float(line[9])
	tradepnl+=(clsdict[tk]-expx)*shr
	if actholddict.has_key(line[0]):
		actholddict[line[0]]+=shr
	else:
		actholddict[line[0]]=shr
	happencash=-shr*avgpx
	if happencash<0:
		nbuy+=1
		buyamt+=shr*avgpx
	elif happencash>0:
		nsell+=1
		sellamt+=-shr*avgpx
	comtax+=abs(happencash)*2.5/10000
	if shr<0:
		stamptax+=happencash*0.001
	if line[0][0]=='6':
		transtax+=abs(happencash)*1.7/10000
		transtax=0#temperary use zero to test
	tcash+=happencash	
cash+=tcash-comtax-stamptax-transtax
print cash
#=================================
#	calculate today's actual hold
#=================================
fname=actholddir+cdate+'.actHoldingEOD.csv'
print 'Begin to write %s' % fname
fd=open(fname,'w+')
fd.write('#tk,shr,lastGoodCls\n')
#calculate hold pnl
stockvalue=0
for key in actholddict:
	if clsdict.has_key(key):
		stockvalue+=actholddict[key]*clsdict[key]
#cash+=holdpnl

fd.write('CASH,1,%.2f\n' % cash)
actholdlist=sorted(actholddict.iteritems(),key=lambda asd:asd[0],reverse=False)
for line in actholdlist:
	key = line[0]
	if key=='CASH':
		continue
	if clsdict.has_key(key):
		cls=clsdict[key]
	else:
		cls=0
		print 'clsdict has not key:%s' % key
	if line[1] != 0 :
		fd.write("%s,%s,%.2f\n" % (key,line[1],cls))

fd.close()
print 'write finish.'
	
pnl=tradepnl+lholdpnl
pnlname=spnldir+cdate+'.pnl.csv'
print 'Begin to write %s' % pnlname
fd=open(pnlname,'w+')
fd.write("#date,cash,nstock,stockValue,nbuy,buyAmt,nsell,sellAmt,comm,stampTax,transtax,trdPnl,holdPnl,pnl,value\n")
fd.write("%s,%f,%d,%d,%d,%f,%d,%f,%f,%f,%f,%f,%f,%f,%f\n" % (cdate,cash,nstock,stockvalue,nbuy,buyamt,nsell,sellamt,comtax,stamptax,transtax,tradepnl,lholdpnl,pnl,cash+stockvalue))

fd.close()
print 'write finish.'
