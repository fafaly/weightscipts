#!/bin/env python

import os
import csv
import sys
import datetime
import time
import globalfunc
import math

ipxdir='/z/data/WindTerminal/ipx/old/'
acttrddir='/z/data/WindDB/production5/portfolio_liuyi/actTrade/'
destrddir='/z/data/WindDB/production5/portfolio_liuyi/desTrade/'
universedir='/cygdrive/z/data/WindDB/setting/universe/'
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
#   dtime:duration time(minuite)
#=================================
def CalEndTime(btimestr,durtime):
	if durtime>110:
		durtime+=90
	durtime=durtime*60
	btime=time.mktime(time.strptime(btimestr,"%H%M"))
	etimestr=btimestr
	if(durtime<0):
		etimestr=btimestr
		durtime=0
	elif durtime==0:
		durtime+=60
	else:
		etime=btime+durtime
		etimestr=time.strftime("%H%M",time.localtime(etime))
	return etimestr

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
for line in reader:
	tk = line[0]
	shr = int(line[1])
	absshr= abs(shr)
	totalpx=0
	totalshr=0
	clspx=clsdict[tk]
	durtime=0
	allcomplete=1
	for i in range(12,240,2):
		cvol=float(ipxdict[tk][i])*0.05
		cvol=math.floor(cvol)
		cpx = float(ipxdict[tk][i-1])
		cpx=round(cpx,2)
		#limit up or down
		if cpx>=clspx*1.1 or cpx <= clspx*0.9:
			allcomplete=0
			break
		dif=absshr-cvol
		if dif >= 0:
			totalpx+=round(cvol*cpx,2)
			totalshr+=cvol
			absshr-=cvol
			continue
		elif dif<0:
			totalshr+=absshr
			totalpx+=round(absshr*cpx,2)
			break
		else:
			break
	if allcomplete==1:
		totalshr=abs(shr)
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
	etimestr=CalEndTime(btimestr,durtime)
	fd.write(('%s,%s,%s,%s,%s,%d,%s,%s,%d,%f,%f\n') % (tk,line[1],line[2],line[3],line[4],actshr,btimestr,etimestr,durtime,avgpx,clspx))

fd.close()

print 'Write finish'



