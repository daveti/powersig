#!/bin/bash

# PowerSig Data Collector
# Collect the %CPU,%MEM for certain process
# Apr 15, 2015
# root@davejingtian.org
# http://davejingtian.org

SAMPLING=1000			# Sampling number
OUTPUT=psig.dat			# Output filename
OUTPUT_CSV=psig.csv		# CSV output filename using both CPU and Mem
OUTPUT_CPU=psig_cpu.csv		# CSV output using CPU data only
PROCESS_NAME=virt-manager	# Should be unique!

# Top
top -b -n $SAMPLING | grep $PROCESS_NAME | awk '{print $9,$10}' > $OUTPUT

# CSV
tr -s ' ' < $OUTPUT | tr ' ' ',' > $OUTPUT_CSV

# CPU-only
TOGGLE=0
CPU0=0
CPU1=0
while read line
do
	CPU=`echo $line | cut -d',' -f1`
	if [ $TOGGLE -eq 0 ]
	then
		CPU0=`echo $CPU`
		TOGGLE=1
	else
		CPU1=`echo $CPU`
		echo $CPU0,$CPU1 >> $OUTPUT_CPU
		CPU0=`echo $CPU1`
	fi
done < $OUTPUT_CSV
