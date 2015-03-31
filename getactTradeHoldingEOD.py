#!/bin/env python

import os
import csv
import sys
import datetime
import time
import globalfunc
import math

ipxdir='/z/data/WindTerminal/ipx/'
acttrddir='/z/data/WindDB/production5/portfolio_liuyi/actTrade/'
destrddir='/z/data/WindDB/production5/portfolio_liuyi/desTrade/'
universedir='/cygdrive/z/data/WindDB/setting/universe/'
actholddir='/z/data/WindDB/production5/portfolio_liuyi/actHolding/'
spnldir='/z/data/WindDB/production5/portfolio_liuyi/pnl/'
#ipxdir=''
#acttrddir=''
#destrddir=''
#dpxdir=''
print '----------get actual trade-----------'

if(len(sys.argv)==1):
	now=datetime.datetime.now()
	cdate = now.strftime("%Y%m%d")
else:
	cdate = sys.argv[1]

ldate=globalfunc.getLastDate(cdate)

#=================================
#    get the close price value
#=================================
clsdict={}
reader = csv.reader(file(universedir+cdate+'_universe.csv','r'))
next(reader)
for line in reader:
	clsdict[line[0]]=float(line[50])


#=================================
#         read ipx data
#=================================
ipxname=ipxdir+cdate+'.ipx.csv'
print 'begin to read %s' % ipxname
reader = csv.reader(file(ipxname,'r'))
next(reader)
ipxdict={}
for line in reader:
	ipxdict[line[0][0:6]]=line

#=================================
# read today's desire trade file
# and write the data
#=================================
fname=acttrddir+cdate+'.actTrade.csv'
fd=open(fname,'w+')
fd.write('#tk,desShr,desStartTime,desEndTime,desDur,actShr,actStartTime,actEndTime,actDuration,expx,cls_1\n')
destrdname=destrddir+cdate+'.desTrade.csv'
reader = csv.reader(file(destrdname,'r'))
print 'Begin to read %s' % destrdname
print 'Begin to write data %s' % fname
next(reader)
actshr=0
stockamtdict={}
for line in reader:
	tk = line[0]
	shr = int(line[1])
	absshr= abs(shr)
	totalpx=0
	totalshr=0
	clspx=clsdict[tk]
	durtime=0
	for i in range(12,242,2):
		cvol=float(ipxdict[tk][i])*0.05
		cvol=math.floor(cvol)
		if cvol==0:
			continue
		cpx = float(ipxdict[tk][i-1])
		#limit up or down
		if cpx>=clspx*1.1 and shr>0:
		#	print tk,clspx,'limit-up'
			continue
		elif cpx<=clspx*0.9 and shr<0:
		#	print tk,clspx,' limit-down'
			continue
		dif=absshr-cvol
		if dif > 0:
			totalpx+=cvol*cpx
			totalshr+=cvol
			absshr-=cvol
			continue
		elif dif<=0:
			totalshr=abs(shr)
			totalpx+=absshr*cpx
			break
		else:
			break
	if shr>0:
		stockamtdict[tk]=-totalpx
	else:
		stockamtdict[tk]=totalpx
	durtime=i-10
	if totalshr>0:
		avgpx=totalpx/totalshr
	else:
		avgpx=float(ipxdict[tk][13])
	if avgpx==0:
		durtime=0
	if shr>0:
		actshr=totalshr
	else:
		actshr=-totalshr
	btimestr='0940'
	etimestr=globalfunc.CalEndTime(btimestr,durtime)
	fd.write(('%s,%s,%s,%s,%s,%d,%s,%s,%d,%f,%.2f\n') % (tk,line[1],line[2],line[3],line[4],actshr,btimestr,etimestr,durtime,avgpx,clspx))

fd.close()

print 'Write finish'

print '----------get actual hold EOD-----------'

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
	happencash=stockamtdict[tk]
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
fd.write('#tk,shr,cls\n')
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
