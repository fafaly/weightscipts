#!/bin/sh

if [ -n $1 ]
then
	date=$1
else
	echo please input the date
	exit
fi

./getdesHold.py $date
./getdesTrade.py $date
./getactTrade.py $date
./getactHoldEOD.py $date
./getactHoldBOD.py $date
