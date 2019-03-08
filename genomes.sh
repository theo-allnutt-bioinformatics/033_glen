#!/bin/bash

#example analysis script for data 33.1

./clip.sh
./idba.sh
./prokka.sh

bbPCR.py linstedt_lobersli_primers.fasta "idba/*.fa" mlva.out mlva.tab 5000 0.9

pathtype.py "idba/*.fa" ~/db/virulencefinder/vir_ecoli virgenes/ 95 80 blastn

bbPCR.py bonanno_primers.fasta "idba/*.fa" bbpcr.out bbpcr.tab 50000 0.9

parsnp -c -p 30 -d idba/ -r sakai.fasta -z 60 -o parsnp

harvesttools -i parsnp/parsnp.ggr -V 33.1.vcf

cat prokka/*.faa > all.faa

usearch -cluster_fast all.faa -id 0.6 -centroids centroids.fasta -sort size -uc clusters.uc 

gene-matrix-from-uclust3.py clusters_sorted.uc genes.txt -cds- 1 1

cds_annotation.py centroids.fasta ~/d/db/ecoli_p/ecoli_p centroids.blast p 1e-10
