#!/bin/bash
mmseqs=/g/bork1/kastano/mmseqs2/bin/mmseqs
clusters_file_name=eggnog_clusters.c00.s7.cm0
export PATH=/g/bork1/huerta/miniconda/bin:$PATH


# 1. Clustering
$mmseqs createdb eggnog4.proteins.core_periphery.fa eggnog_seqs.db
mkdir tmpdir
$mmseqs cluster eggnog_seqs.db $clusters_file_name.db tmpdir/ --threads 20 -c 0.0 --cascaded -s 7 --cluster-mode 2

# 2. Export to fasta or/and tsv
$mmseqs createseqfiledb eggnog_seqs.db $clusters_file_name.db clu_seq 
$mmseqs result2flat eggnog_seqs.db eggnog_seqs.db clu_seq clu_seq.fa
$mmseqs createtsv eggnog_seqs.db eggnog_seqs.db $clusters_file_name.db $clusters_file_name.tsv 

# 3. Compute stats
stats_f=${clusters_file_name}.stats
echo "nb of clusters:" > $stats_f
cat $clusters_file_name.tsv |datamash countunique 1 >> $stats_f
cat $clusters_file_name.tsv |datamash -g1 countunique 2 > $clusters_file_name.sizes 
echo "nb of singletons" >> $stats_f
cat $clusters_file_name.sizes | awk '{if ($2==1) {print $1 " " $2}}' | wc -l >> $stats_f 

echo "clusters average size" >> $stats_f
cat $clusters_file_name.sizes | awk '{if ($2>1) sum += $2 n++;} END {if (n>0) print sum/n;}' >> $stats_f 

cat $clusters_file_name.sizes | awk '{if ($2>2) sum++} END {print sum}'


# Compare mmseqs with eggnog clusters

clusters_per_line_f=${clusters_file_name}.clusters_per_line
#cat ${clusters_file_name}.tsv | datamash -g 1 collapse 2 > $clusters_per_line_f
comparison_f=${clusters_file_name}.comparison
python compare_clusters.py -i $clusters_per_line_f -o $comparison_f
echo "nb of mmseqs clusters in eggnog clusters" >> $stats_f
cat $comparison_f | awk '{if ($5==0) n++;} END {print n}' >> $stats_f
echo "nb of eggnog clusters in mmseqs clusters" >> $stats_f
cat $comparison_f | awk '{if ($6==0) n++;} END {print n}' >> $stats_f
echo "number of the rest of the overlapping clusters" >> $stats_f
cat $comparison_f | awk '{if ($5!=0 && $6!=0) n++;} END {print n}' >> $stats_f
echo "average nb of shared members in these overlapping clusters" >> $stats_f
cat $comparison_f | awk '{if ($5!=0 && $6!=0) sum+=$4 n++;} END {print sum/n}' >> $stats_f
