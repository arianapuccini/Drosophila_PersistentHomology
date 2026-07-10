#BEFORE USING THIS, USE true_distance TO MAKE A POINT CLOUD OR synapses_as_edges/ neurondata TO MAKE A DISTANCE MATRIX!

#This calculates the persistent homology of a graph with a distance matrix, or of points from a point cloud. In practice the distance matrix should be used when dealing with points that are a certain number of edges (or connections) away from eachother. The point cloud should be used when dealing with points that are a certain distance away from eachother in a Euclidean space.

from matplotlib import colors
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from ripser import ripser

try:
    import networkx as nx
    HAS_NETWORKX = True
except Exception:
    HAS_NETWORKX = False

#read the distance matrix / point cloud data
D = D = pd.read_csv("eb_synapse_coords.csv", header=None).to_numpy()

print(D.shape)

#If the distance matrix is a point cloud, set distance_matrix to False. Make sure maxdim is greater than or equal to the maximum homology dimension you specify on line 89.
result = ripser(D, distance_matrix=False, maxdim=3)

diagrams = result["dgms"]

#colors for each homology dimension barcode
colors = {0: "blue", 1: "red", 2: "green"}

def plot_barcode(result, dims, sort_by, title, inf_extension = 0.25):
    """Plot a barcode for selected homology dimensions.

    Infinite deaths are displayed slightly beyond the largest finite death.
    """
    dgms = result["dgms"]
    if dims is None:
        dims = list(range(len(dgms)))

    finite_deaths = []
    for dgm in dgms:
        if len(dgm):
            finite_deaths.extend(dgm[np.isfinite(dgm[:, 1]), 1].tolist())
    max_finite = max(finite_deaths) if finite_deaths else 1.0
    inf_value = max_finite + inf_extension * max(1.0, max_finite)

    fig, ax = plt.subplots(figsize=(9, max(3, 0.25 * sum(len(dgms[d]) for d in dims))))
    y = 0
    yticks = []
    yticklabels = []

    for dim in dims:
        intervals = np.array(dgms[dim], dtype=float)
        if len(intervals) == 0:
            continue

        if sort_by == "birth":
            order = np.lexsort((intervals[:, 1], intervals[:, 0]))
        elif sort_by == "persistence":
            deaths_for_sort = intervals[:, 1].copy()
            deaths_for_sort[~np.isfinite(deaths_for_sort)] = inf_value
            pers = deaths_for_sort - intervals[:, 0]
            order = np.argsort(-pers)
        else:
            order = np.arange(len(intervals))

        for idx in order:
            birth, death = intervals[idx]
            death_display = inf_value if not np.isfinite(death) else death
            ax.hlines(y, birth, death_display, linewidth=1, color=colors.get(dim, "black"))
            if not np.isfinite(death):
                ax.plot(death_display, y, marker=">", markersize=6)
            yticks.append(y)
            yticklabels.append(f"H{dim}")
            y += 1

    ax.set_xlabel("r value")
    ax.set_ylabel("dimension")
    if len(yticks) <= 60:
        ax.set_yticks(yticks)
        ax.set_yticklabels(yticklabels)
    else:
        ax.set_yticks([])
    if title is None:
        title = f"Barcode for $M_{{{result['n']}}}$"
    ax.set_title(title)
    ax.grid(axis="x", alpha=0.25)
    plt.tight_layout()
    plt.show()

#Change the title to best fit your data/graph
plot_barcode(result, dims=[0, 1, 2, 3], sort_by="birth", title="Barcodes for Fly Brain Epsiloid Body", inf_extension=0.25)

print("H0")
print(diagrams[0])

print("H1")
print(diagrams[1])

print("H2")
print(diagrams[2])