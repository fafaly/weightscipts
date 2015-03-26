#!/bin/env python

import os
import csv
import sys
import datetime
import time
import globalfunc

ipxdir='/z/data/WindTerminal/ipx/old/'
acttrddir='/z/data/WindDB/production5/portfolio/actTrade/'
destrddir='/z/data/WindDB/production5/portfolio/desTrade/'
dpxdir='/z/data/WindDB/dpx/'
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
reader = csv.reader(file(dpxdir+ldate+'.dpx.csv','r'))
next(reader)
for line in reader:
	clsdict[line[0]]=float(line[6])


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
fd.write('#tk,shr,BOT,EOT,duration,actual,avgpx\n')
destrdname=destrddir+cdate+'.desTrade.csv'
reader = csv.reader(file(destrdname,'r'))
print 'Begin to read %s' % destrdname
print 'Begin to write data %s' % fname
next(reader)
for line in reader:
	tk = line[0]
	shr = int(line[1])
	absshr= abs(shr)
	totalpx=0
	totalshr=0
	clspx=clsdict[tk]
	for i in range(12,240,2):
		cvol=float(ipxdict[tk][i])*0.05
		cpx = float(ipxdict[tk][i+1])
		#limit up or down
		if cpx>=clspx*1.1 or cpx <= clspx*0.9:
			break
		dif=absshr-cvol
		if dif > 0:
			totalpx+=cvol*cpx
			totalshr+=cvol
			absshr-=cvol
			continue
		elif dif<0:
			totalshr+=absshr
			totalpx+=absshr*cpx
			break
		else:
			break
	if totalshr>0:
		avgpx=totalpx/totalshr
	else:
		avgpx=float(ipxdict[tk][13])
	durtime=(i-10)/2
	btimestr='0940'
	etimestr=CalEndTime(btimestr,durtime*60)
	fd.write(('%s,%d,%s,%s,%d,%d,%f\n') % (tk,shr,btimestr,etimestr,durtime,totalshr,avgpx))

fd.close()

print 'Write finish'
	


