#!/usr/bin/env python
import sys
import re
import glob
import subprocess


digits = re.compile(r'(\d+)')
def tokenize(filename):
    return tuple(int(token) if match else token
                 for token, match in
                 ((fragment, digits.search(fragment))
                  for fragment in digits.split(filename)))



folder = sys.argv[1] 

filelist=glob.glob(folder)

filelist.sort(key=tokenize)
print filelist

ref=sys.argv[2]

outfolder=sys.argv[3]

cov_t=float(sys.argv[4])

p0=subprocess.Popen("mkdir -p ./%s" %outfolder,shell=True).wait()
outlist=[]
outnames=[]
for i in filelist:
		
	name = i.split("/")[-1].split(".")[0]

	p1= subprocess.Popen("bbmap.sh ref=%s ambig=all nzo=t mappedonly=t covstats=%s/%s.count in=%s overwrite=t" %(ref,outfolder,name,i), shell=True).wait()
	
	outlist.append(outfolder+"/"+name+".count")
	outnames.append(name)
	
data={}
genes={}
for x in outlist:

	h=open(x,'r')
	name=x.split("/")[-1].split(".count")[0]
	data[name]={}
	
	for y in h:
		if y[0]<>"#":
			gene=y.split("\t")[0].split("_")[0] #gene root name
			gene_full=y.split("\t")[0]
			cov=float(y.split("\t")[4])
				
			if gene in data[name].keys(): #record highest coverage hit
				if cov > data[name][gene] and cov>=cov_t:
					data[name][gene]=cov
					genes[gene]=gene_full
					
				
			if gene not in data[name].keys() and cov>=cov_t:
				data[name][gene]=cov
				genes[gene]=gene_full
				

g=open(outfolder+"/summary.txt",'w')

g.write("\t"+"\t".join(str(p) for p in outnames)+"\n")

genelist=genes.keys()
genelist.sort()

for j in genelist:

	g.write(genes[j])
	
	for k in outnames:
		if j in data[k].keys():
			g.write("\t"+str(data[k][j]))
		else:
			g.write("\t"+"0")
	
			
	g.write("\n")
	
	
	
	
	
	
	