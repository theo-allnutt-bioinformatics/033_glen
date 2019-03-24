#!/bin/bash
set -e

#mkdir -p idba
#idba.py "int/*.fasta" idba/ 50 250 50 4

#n50folder.py "idba/*.fa" fasta > assembly.stats

#bbPCR.py linstedt_lobersli_primers.fasta "idba/*.fa" mlva.out mlva.tab 5000 0.9
#bbPCR.py bonanno_primers.fasta "idba/*.fa" bbpcr.out bbpcr.tab 50000 0.9

#mkdir -p virgenes
#pathtype.py "idba/*.fa" ~/db/virulencefinder/vir_ecoli virgenes/ 90 60 blastn
#mkdir -p stx
#pathtype.py "idba/*.fa" ~/db/stx/stx stx 90 60 blastn
#mkdir -p vir_bbmap
#bbmap_virgenes.py "int/*.fasta" ~/db/virulencefinder/vir_ecoli.fasta vir_bbmap/ 50

#mkdir -p parsnp
#parsnp -c -p 30 -d idba/ -r sakai.fasta -z 60 -o parsnp

#harvesttools -i parsnp/parsnp.ggr -V 33.1.vcf

prokka.py "idba/*.fa" prokka/

cat prokka/*.faa > all.faa

usearch -cluster_fast all.faa -id 0.6 -centroids centroids.fasta -consout cons.fasta -sort size -uc clusters.uc && sort -nk2 clusters.uc > clusters_sorted.uc

gene-matrix-from-uclust3.py clusters_sorted.uc genes.txt -cds- 1 1

cds_annotation.py centroids.fasta ~/d/db/ecoli_p/ecoli_p centroids.blast p 1e-10


