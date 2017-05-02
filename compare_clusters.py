from collections import defaultdict
import hashlib
from datetime import datetime

startTime = datetime.now()

eggnog_cls_F = open("/g/bork1/kastano/eggnog_clustering/NOG.members.tsv", "r")
mmseqs_cls_F = open("/g/bork1/kastano/eggnog_clustering/eggnog_clusters.c00.s7.clusters_per_line","r")


m_clusters = defaultdict(list)

# getting all mmseqs clusters in a dict

for line in mmseqs_cls_F:
    fields = line.rstrip().split("\t")
    cluster = fields[0]
    members = map(str.strip, fields[1].split(","))
    if len(members) > 1:
        m_clusters[cluster] = set(members)
mmseqs_cls_F.close()

# getting all eggnog clusters in a dict

e_clusters = {}
for line in eggnog_cls_F:
    fields = line.rstrip().split("\t")
    cluster = fields[1]
    members = map(str.strip, fields[5].split(","))
    e_clusters[cluster] = set(members)
eggnog_cls_F.close()

print "clusters obtained"

# converting to hashes
m_hashes = {}
e_hashes = {}
for c1 in m_clusters.keys():
    c1_string = ','.join(sorted(m_clusters[c1]))
    m_hashes[hashlib.md5(c1_string).hexdigest()] = c1
for c2 in e_clusters.keys():
    c2_string = ','.join(sorted(e_clusters[c2]))
    e_hashes[hashlib.md5(c2_string).hexdigest()] = c2
print "converting to hashes done"

h1_set = set(m_hashes.keys())
h2_set = set(e_hashes.keys())

common = h1_set & h2_set
print "common clusters", len(common)

for h in common:
    del m_clusters[m_hashes[h]]
    del e_clusters[e_hashes[h]]

print len(m_clusters), len(e_clusters)

t1 = datetime.now()

def compared_clusters(e_clusters, m_clusters):
    """
    e_clusters = {eclu_name: set(eclu_members), ...}
    m_clusters = {mclu_name: set(mclu_members), ...}
    """
    RESULTS_F = open("clusters_comparison.tsv","w")

    # precalculate where does it appear each individual
    # sequence name (what clusters)
    seq2ecluster = defaultdict(list)
    for clu_name, members in e_clusters.iteritems():
        for seq in members:
            seq2ecluster[seq].append(clu_name)

    seq2mcluster = defaultdict(list)
    for clu_name, members in m_clusters.iteritems():
        for seq in members:
            seq2mcluster[seq].append(clu_name)


    print "members mapping to clusters done"

    # For each MMseqs clusters, lets compare content only against the subset of
    # eggnog clusters that had at least one sequence in common (avoids brute
    # force double loop).

    # eggnog cluster contained or overlapping with mmseqs clusters 
    for m_clu, m_members in m_clusters.iteritems():
        related_eggnog_clusters = set()
        for member in m_members:
            member_e_clusters = seq2ecluster.get(member, [])
            related_eggnog_clusters.update(member_e_clusters)
            
        for e_clu in related_eggnog_clusters:
            print e_clu
            common = len(m_members & e_clusters[e_clu])
            m_missing = len(m_members - e_clusters[e_clu])
            e_missing = len(e_clusters[e_clu] - m_members)
            print >> RESULTS_F, "\t".join(map(str, (m_clu, len(related_eggnog_clusters), e_clu, common, m_missing, e_missing)))

compared_clusters(e_clusters, m_clusters)


print "comparison done in ", datetime.now() - t1

print "script running for", datetime.now() - startTime
