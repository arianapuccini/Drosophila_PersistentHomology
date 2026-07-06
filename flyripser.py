from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import shortest_path

from ripser import ripser
from persim import plot_diagrams

try:
    import networkx as nx
    HAS_NETWORKX = True
except Exception:
    HAS_NETWORKX = False

#read the weight matrix
D = pd.read_csv("weight_matrix.csv", index_col=0)

#convert to a NumPy array
D = D.to_numpy()

result = ripser(D, distance_matrix=True, maxdim=3)

diagrams = result["dgms"]

print("H0")
print(diagrams[0])

print("H1")
print(diagrams[1])

print("H2")
print(diagrams[2])

print("H3")
print(diagrams[3])