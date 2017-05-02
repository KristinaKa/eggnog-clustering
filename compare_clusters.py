def compared_clusters(e_clusters, m_clusters):
    """
    e_clusters = {eclu_name: set(eclu_members), ...}
    m_clusters = {mclu_name: set(mclu_members), ...}
    """

    # precalculate where does it appear each individual
    # sequence name (what clusters)
    seq2ecluster = defaultdict(list)
    for clu_name, seq in e_clusters:
        seq2ecluster[seq].append(clu_name)

    seq2mcluster = defaultdict(list)
    for clu_name, seq in m_clusters:
        seq2mcluster[seq].append(clu_name)


    # For each MMseqs clusters, lets compare content only against the subset of
    # eggnog clusters that had at least one sequence in common (avoids brute
    # force double loop).

    # eggnog cluster contained or overlapping with mmseqs clusters 
    for m_clu, m_members in m_clusters.iteritems():
        related_eggnog_clusters = set()
        for member in m_members:
            e_clusters = seq2ecluster.get(member, [])
            related_eggnog_clusters.update(e_clusters)

        for e_clu in related_eggnog_clusters:
            common = len(m_set & e_clusters[e_clu])
            m_missing = len(m_set - e_clusters[e_clu]))
            e_missing = len(m_set - e_clusters[e_clu]))
            print m_clue, len(related_eggnog_clusters), e_clu, common, m_missing, e_missing
