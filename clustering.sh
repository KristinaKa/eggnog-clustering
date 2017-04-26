#!/bin/bash
mmseqs=/home/kristina/mmseqs2/bin/mmseqs
clusters_file_name=eggnog_clusters.c00.s7
export PATH=/g/bork1/huerta/miniconda/bin:$PATH

# 1. Clustering
$mmseqs createdb eggnog4.proteins.core_periphery.fa eggnog_seqs.db
mkdir tmpdir
$mmseqs cluster eggnog_seqs.db $clusters_file_name.db tmpdir/ --threads 20 -c 0.0 --cascaded -s 7 --cluster-mode 2

# 2. Export to fasta and/or tsv
$mmseqs createseqfiledb eggnog_seqs.db $clusters_file_name.db clu_seq 
$mmseqs result2flat eggnog_seqs.db $clusters_file_name.db clu_seq clu_seq.fa
$mmseqs createtsv eggnog_seqs.db eggnog_seqs.db $clusters_file_name.db $clusters_file_name.tsv 

# 3. Compute stats
#nb of clusters
nb_clusters=`cat $clusters_file_name.tsv |datamash countunique 1`
#nb of members per cluster
cat $clusters_file_name.tsv |datamash -g1 countunique 2 > $clusters_file_name.sizes 
#nb of signletons
nb_singletons=`cat $clusters_file_name.sizes | awk '{if ($2==1) {print $1 " " $2}}' | wc -l `

echo "nb of clusters:" $nb_clusters "\nnb of singletons:" $nb_singletons > $clusters_file_name.stats

# 4. Generate fasta files of clusters
mkdir ${clusters_file_name}_fasta
python separate_clusters.py -f clu_seq.fa -d ${clusters_file_name}_fasta
