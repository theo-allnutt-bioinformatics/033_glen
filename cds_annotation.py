#!/usr/bin/python

import sys
import re
from Bio import SeqIO
import subprocess
from random import randrange

r2=str(randrange(10000))

#read unannotated protein fasta and add annotations from a blast  db
#usage: python ~/s/cds_annotation.py centroids.fasta nr cds.blast p 1e-5
#'p' can be 'p' for protein or 'n' for nucleotide
#'1e-5' is evalue threshold for blast hits
#blast > v2.2.30+ required

f = sys.argv[1] #centroids.fasta

db = sys.argv[2] # database

h = open(sys.argv[3],'w') #annotated list output

#h=sys.argv[4] #blast output file

type = sys.argv[4] #type

e = sys.argv[5]

#m = open(sys.argv[2]+".un.fa",'w') #unknowns file

print
print f


print 'blasting'
n=0
cent=open(f,'r')
#get list of cds from centroids
cds=[]
for i in SeqIO.parse(cent,'fasta'):
	cds.append(i.id)
	

if type == "p":
	p1= subprocess.Popen("blastp -query %s -db %s -out temp%s.blast -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle' -max_hsps 1 -max_target_seqs 1 -evalue %s -num_threads 24" %(f,db,r2,e), shell=True).wait() 

if type == "n":
	p1= subprocess.Popen("blastn -task blastn -query %s -db %s -out temp%s.blast -outfmt '6 qseqid sseqid pident length mismatch gapopen qstart qend sstart send evalue bitscore stitle' -max_hsps 1 -max_target_seqs 1 -evalue %s -num_threads 24" %(f,db,r2,e), shell=True).wait() 
	

j = open("temp%s.blast" %r2,'r')


data={}
#gets blast hits in same order as cds if cds not in hits then also report
cnt=0
for i in j:
	cnt=cnt+1
	
	k= i.split("\t")
	line = "\t".join(str(p) for p in k)
	if k[0] not in data.keys():
		data[k[0]]=line #has return on end
print "%s hits" %str(cnt)		
for i in cds:
	if i in data.keys():
		h.write(data[i])
	else:
		h.write(i+"\tno hits\n")
	
p2= subprocess.Popen("rm temp%s.blast" %r2, shell=True).wait() 

print "done"


