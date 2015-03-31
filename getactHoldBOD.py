#!/bin/env python
import csv
import os
import sys
import datetime
import time
import globalfunc

cacsdir='/z/data/WindDB/cacs/'
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
cacsname=cacsdir+ndate+'.cacs.csv'
print 'Get ratio of %s' % cacsname
if os.path.exists(cacsname):
	reader=csv.reader(file(cacsname,'r'))
	next(reader)
	for line in reader:
		if line[3]=='':
			vol1=0
			pvol1=1
		else:
			pvol1=float(line[2])
			vol1=float(line[3])
		if line[5]=='':
			vol2=0
			pvol2=1
		else:
			pvol2=float(line[4])
			vol2=float(line[5])
		if line[7]=='':
			vol3=0
			pvol3=1
		else:
			pvol3=float(line[6])
			vol3=float(line[7])
		clist=(vol1/pvol1,vol2/pvol2,vol3/pvol3)
		cacsdict[line[0][0:6]]=clist

fname=scacsdir+cdate+'.ratio.csv'
fd=open(fname,'w+')
fd.write('#tk,ratio\n')
for key in cacsdict:
	fd.write("%s,%d\n" % (key,1+cacsdict[key][1]+cacsdict[key][0]))

fd.close()

#=================================
#    get actual holding BOD
#=================================
print 'Begin read actual holding EOD and calcute the BOD'
actEOD = actholdingdir + cdate+'.actholdingEOD.csv'
reader=csv.reader(file(actEOD,'r'))
next(reader)
holdBODlist=[]
i=0
cash=0
for line in reader:
	tk=line[0]
	shr=int(line[1])
	cls=float(line[2])
	if tk=='CASH':
		cash = float(line[2])
	elif cacsdict.has_key(tk):
		print 'here is a cacs',line[0]
		cash+=shr*cacsdict[tk][2]
		nshr=shr*(1+cacsdict[tk][0]+cacsdict[tk][1])
		if nshr!=0:
			ncls=float(line[1])*float(line[2])/nshr
			ncls=round(ncls,2)
		holdBODlist.append([tk,nshr,ncls])
	else:
		holdBODlist.append([tk,shr,cls])
	i+=1

print 'Begin to write %s' % fname
fname = actholdingdir+ndate + '.actHoldingBOD.csv'
fd = open(fname,'w+')
fd.write('#tk,shr,cls\n')
fd.write('CASH,1,%s\n' % cash)
for i in range(0,len(holdBODlist)):
	fd.write("%s,%d,%s\n" % (holdBODlist[i][0],holdBODlist[i][1],holdBODlist[i][2]))
fd.close()
print 'write finish'
