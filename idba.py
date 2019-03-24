#!/usr/bin/env python

import sys
import re
import glob
import subprocess

#Theo Allnutt, 2019

def tokenize(filename):
	digits = re.compile(r'(\d+)')
	return tuple(int(token) if match else token
		for token, match in((fragment, digits.search(fragment))
			for fragment in digits.split(filename)))

folder = sys.argv[1] 

filelist=glob.glob(folder)
filelist.sort(key=tokenize)

outfolder =sys.argv[2]

mink=sys.argv[3]
maxk=sys.argv[4]
kstep=sys.argv[5]
threads=sys.argv[6]

p0=subprocess.Popen("mkdir -p %s" %outfolder,shell=True).wait()

names=[]
print filelist
for f in filelist:
	print f
	name=f.split("/")[-1].split(".")[0]
	names.append(name)
	p1=subprocess.Popen("idba_ud -r %s -o %s/%s --num_threads %s  --mink %s --maxk %s --step %s" %(f,outfolder,name,threads,mink,maxk,kstep),shell=True).wait()
	
for i in names:
	try:
		subprocess.Popen("mv %s/%s/scaffold.fa %s/%s.fa" %(outfolder,i,outfolder,i),shell=True).wait()
		subprocess.Popen("rm -r %s/%s/" %(outfolder,i),shell=True).wait()
	except:
		print i,'no scaffold'









	