#!/usr/bin/env python
import sys
from Bio import SeqIO
import subprocess
import re
import glob

#Theo Allnutt, 2017
#bbmaps pcr primers in pairs to find location(s) and orientation

digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))


primers = sys.argv[1]
#ref = sys.argv[2]
g=open(sys.argv[3],'a') # hits detail output
h=open(sys.argv[4],'w') #table output
maxlen = sys.argv[5]

id = sys.argv[6]

folder = sys.argv[2] 

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
print filelist

data={}
for ref in filelist:

	p1=subprocess.Popen("bbmap.sh in=%s ref=%s out=bb.sam ordered=t overwrite=t interleaved=t ambiguous=all pairedonly=t pairlen=%s minid=%s" %(primers,ref,maxlen,id),shell=True).wait()
		
	h1=open('bb.sam','r')

	data[ref]={}
	reads=[]
	for i in h1:
		if i[0]<>"@":
			k=i.rstrip("\n").split("\t")
			read=k[0].split(":")[0]
			if read not in reads:
				reads.append(read)
			scaf=k[2]
			locus=k[3]
			s=int(k[8])
			if s<0:
				orient="-"
			else:
				orient="+"
			size=str(abs(s))
			
			if read not in data[ref].keys():
				data[ref][read]=[]
				data[ref][read].extend([scaf,locus,size,orient])
	
	g.write(ref+"\n")
	g.write("assay\thit\tlocus\tsize\torientation\n")

	for i in reads:	
		g.write(i+"\t"+"\t".join(str(x) for x in data[ref][i])+"\n")
	g.write("\n")

#record pcr size table

h.write("Subject\t"+"\t".join(str(p) for p in reads)+"\n")
for i in filelist:
	output=""
	for j in reads:
	
		output=output+"\t"+data[i][j][2]

	h.write(i+output+"\n")

	
			
			
		
		