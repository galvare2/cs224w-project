
from __future__ import print_function
import snap
from scipy import io
import random
import numpy as np
import math
import matplotlib.pyplot as plt
from sets import Set

FILENAMES = [("cat", "CIJall"), ("macaque71", "CIJ"), ("Coactivation_matrix", "Coactivation_matrix")]

def load_data():
    for filename, keyname in FILENAMES:
        make_edge_list(filename, keyname)

def make_edge_list(filename, keyname):
    mat_file = io.loadmat(filename + ".mat")
    print(mat_file.keys())
    #CIJctx = np.asarray(cat_mat["CIJctx"])
    matrix = np.asarray(mat_file[keyname])
    (num_nodes, _) = matrix.shape
    f = open(filename + ".txt", "w")
    for i in range(num_nodes):
        if np.count_nonzero(matrix[i,:]) == 0:
            matrix = np.delete(matrix, i, 0)
            matrix = np.delete(matrix, i, 1)
    for i in range(num_nodes):
        for j in range(i, num_nodes):
            if(matrix[i,j] > 0):
                print(str(i) + " " + str(j) + " " + str(matrix[i,j]), file=f)


if __name__=="__main__":
    load_data()