from collections import defaultdict
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--tsv', '-t', dest='cls_tsv_file', type=str,
                   help='clusters tsv file')
parser.add_argument('--fasta', '-f', dest='cls_fasta_file', type=str,
                   help='clusters fasta file')
parser.add_argument('--dir', '-d', dest='fasta_dir', type=str, help="directory for the ouput files")

args = parser.parse_args()

clusters = defaultdict(list)

# fasta file parsing
sequences = {}
FASTA_F = open("%s" %args.cls_fasta_file , "r") 
lines = FASTA_F.readlines()
cluster = None
last_seq_name = None
for i in range(len(lines)):
    if lines[i].startswith(">"):
        seq_name = lines[i].rstrip().split(">")[1]
        if lines[i+1].startswith(">"):
            cluster = seq_name
        else:
            clusters[cluster].append(seq_name)
            last_seq_name = seq_name
    else:
        sequences[last_seq_name] = lines[i]
        

FASTA_F.close()
print "fasta sequences obtained"

SINGL_F = open("%s/singletons.fa" %args.fasta_dir, "w") 
for cluster, cl_sequences in clusters.iteritems():
    if len(cl_sequences) == 1:
        seq = cl_sequences[0]
        print >> SINGL_F, ">%s" %seq
        print >> SINGL_F, sequences[seq]
    else:
        OUT = open("%s/%s_cluster.fa" %(args.fasta_dir, seq), "w")
        for seq in cl_sequences:
            print >> OUT, ">%s" %seq
            print >> OUT, sequences[seq]
        OUT.close()
  
SINGL_F.close()
