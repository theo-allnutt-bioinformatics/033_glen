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

p0=subprocess.Popen("mkdir -p %s" %outfolder,shell=True).wait()

names=[]
print filelist
for f in filelist:
	print f
	name=f.split("/")[-1].split(".")[0]
	names.append(name)
	p1=subprocess.Popen("prokka --fast --force --outdir %s/ --prefix %s  --locustag  %s-cds- --cpus 0 --metagenome --mincontiglen 60 %s" %(outfolder,name,name,f),shell=True).wait()
	










	