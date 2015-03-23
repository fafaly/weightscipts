#!/bin/env python

import os
import csv
import sys
import datetime
import time

print '----------get actual trade-----------'

if(len(sys.argv)==1):
	now=datetime.datetime.now()
	cdate = now.strftime("%Y%m%d")
else:
	cdate = sys.argv[1]

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
#         read ipx data
#=================================
ipxname=cdate+'.ipx.csv'
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
fname=cdate+'.actTrd.csv'
print 'Begin to write data %s' % fname
fd=open(fname,'w+')
fd.write('#tk,shr,BOT,EOT,duration,avgpx\n')
destrdname=cdate+'.desTrade.csv'
reader = csv.reader(file(destrdname,'r'))
print 'Begin to read %s' % destrdname
next(reader)
for line in reader:
	tk = line[0]
	shr = int(line[1])
	absshr= abs(shr)
	totalpx=0
	totalshr=0
	for i in range(10,240,2):
		cvol=float(ipxdict[tk][i])*0.05
		cpx = float(ipxdict[tk][i+1])
		if absshr-cvol > 0:
			totalpx+=cvol*cpx
			totalshr+=cvol
			absshr-=cvol
			continue
		else:
			break
	if totalshr>0:
		avgpx=totalpx/totalshr
	else:
		avgpx=float(ipxdict[tk][11])
	durtime=60*(i-10)/2
	btimestr='0940'
	etimestr=CalEndTime(btimestr,durtime)
	fd.write(('%s,%d,%s,%s,%d,%f\n') % (tk,shr,btimestr,etimestr,durtime/60,avgpx))

fd.close()

print 'Write finish'
	


