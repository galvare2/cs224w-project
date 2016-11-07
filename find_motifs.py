
import sys
import snap
from scipy import io
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from sets import Set
from itertools import permutations

POSSIBLE_MOTIFS_3 = [
    [(0,1), (0,2), (1,2)], #Cycle/Clique
    [(0,1), (1,2)] #Line
    ]

POSSIBLE_MOTIFS_4 = [
    [(0,1), (1,2), (2,3)], #Line
    [(0,1), (0,2), (0,3)], #Center
    [(0,1), (0,3), (1,2), (2,3)], #Cycle
    [(0,1), (0,2), (0,3), (1,3)], #Boxed Center
    [(0,1), (0,2), (0,3), (1,2)], #Crossed Center
    [(0,1), (0,2), (0,3), (1,2), (2,3)], #One Missing
    [(0,1), (0,2), (0,3), (1,2), (1,3), (2,3)] #Clique
]

POSSIBLE_MOTIFS_5 = [
    [(0,1), (1,2), (2,3), (3,4)], #Line
    [(0,1), (0,2), (0,3), (0,4)], #Center
    [(0,1), (0,2), (0,3), (3,4)], #Partial Center
    [(0,1), (0,4), (1,2), (2,3), (3,4)], #Cycle
    [(0,1), (0,2), (1,2), (2,3), (3,4)], #Broken Cycle 1
    [(0,1), (0,3), (1,2), (2,3), (3,4)], #Broken Cycle 2
    [(0,1), (0,4), (1,2), (1,4), (3,4)], #Broken Cycle 3
    [(0,1), (0,4), (1,2), (1,4), (2,3), (3,4)], #6-Cycle
    [(0,1), (1,2), (1,4), (2,3), (2,4), (3,4)], #6-Nocycle-1
    [(0,1), (1,2), (1,3), (2,3), (2,4), (3,4)], #6-Nocycle-2
    [(0,1), (1,2), (1,3), (1,4), (2,3), (3,4)], #6-Nocycle-3
    [(0,1), (0,2), (1,2), (2,3), (2,4), (3,4)], #6-Nocycle-4
    [(0,1), (0,4), (1,2), (1,4), (2,3), (2,4), (3,4)], #7-Cycle-1
    [(0,1), (0,2), (0,4), (1,2), (1,4), (2,3), (3,4)], #7-Cycle-2
    [(0,1), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)], #7-Nocycle-1
    [(0,1), (0,2), (1,2), (1,3), (2,3), (2,4), (3,4)], #7-Nocycle-2
    [(0,1), (0,2), (0,3), (0,4), (1,2), (1,4), (2,3), (3,4)], #8-1
    [(0,1), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)], #8-2
    [(0,1), (0,2), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)], #8-3
    [(0,1), (0,3), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)], #8-4
    [(0,2), (0,3), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)], #8-5
    [(0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)], #All But One
    [(0,1), (0,2), (0,3), (0,4), (1,2), (1,3), (1,4), (2,3), (2,4), (3,4)] #Clique
]

NUM_SAMPLES_3 = 100000
NUM_SAMPLES_4 = 100000
NUM_SAMPLES_5 = 100000

def find_motifs(filename):
    graph = snap.LoadEdgeList(snap.PUNGraph, filename, 0, 1)
    #motifs_3 = check_motifs_3(graph)
    #print motifs_3   
    #motifs_3_sampled = sample_motifs(graph, 3, POSSIBLE_MOTIFS_3, NUM_SAMPLES_3)  
    #print motifs_3_sampled
    #motifs_4_sampled = sample_motifs(graph, 4, POSSIBLE_MOTIFS_4, NUM_SAMPLES_4) 
    #print motifs_4_sampled
    motifs_5_sampled = sample_motifs(graph, 5, POSSIBLE_MOTIFS_5, NUM_SAMPLES_5)
    print motifs_5_sampled

def sample_motifs(graph, n, motifs_list, num_samples):
    motif_results = [0]*len(motifs_list)
    for i in range(num_samples):
        if i % 10000 == 0:
            print "Iter:",i
        sample = get_one_sample(graph, n)
        motifs_found = check_motifs_nodes(graph, sample, motifs_list)
        for i in range(len(motifs_found)):
            motif_results[i] += motifs_found[i]
    return np.asarray(motif_results, dtype=float) / num_samples

def get_one_sample(graph, n):
    graph_nodes = graph.GetNodes()
    samples = np.random.choice(range(graph_nodes), n, replace=False)
    return samples.tolist()


def check_motifs_3(graph):
    num_nodes = graph.GetNodes()
    motif_results = [0]*len(POSSIBLE_MOTIFS_3)
    combinations_examined = 0
    for i in range(num_nodes-2):
        for j in range(i+1, num_nodes-1):
            for k in range(j+1, num_nodes):
                nodes = [i, j, k]
                motifs = check_motifs_nodes(graph, nodes, POSSIBLE_MOTIFS_3)
                for i in range(len(motifs)):
                    motif_results[i] += motifs[i]
                combinations_examined += 1
    return np.asarray(motif_results, dtype=float) / combinations_examined
    

def check_motifs_nodes(graph, nodes, motifs_list):
    motifs_met = [0]*len(motifs_list)
    # Try all possible labelings
    for labeling in permutations(range(len(nodes))):
        connection_list = get_connection_list(graph, nodes, labeling)
        for i,motif in enumerate(motifs_list):
            if motifs_met[i] == 1:
                continue
            elif connection_list == motif:
                motifs_met[i] = 1
    #print motifs_met
    return motifs_met

def get_connection_list(graph, nodes, labeling):
    result = []
    for i in range(len(nodes) - 1):
        for j in range(i, len(nodes)):
            if graph.IsEdge(nodes[i], nodes[j]):
                result.append((labeling[i],labeling[j]))
    return result




if __name__=="__main__":
    if len(sys.argv) != 2:
        print "Usage: find_motifs.py filename"
    else:
        find_motifs(sys.argv[1])