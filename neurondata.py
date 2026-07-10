#This makes a weight matrix for neurons in the Epsilloid Body of the fly brain, using the neuprint API. The ROI (region of interest) of the brain can be altered. The weights associated with each neuron-neuron connection are the number of synapses between a pair of neurons. This only looks at neuron pairs with at least 100 synapses between them to make data analysis more practical, but this number can be altered.

from neuprint import NeuronCriteria, fetch_neurons, fetch_adjacencies, Client

from pyvis.network import Network

import numpy, pandas, networkx as nx

c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFyaWFuYXB1Y2NpbmlAZ21haWwuY29tIiwibGV2ZWwiOiJub2F1dGgiLCJpbWFnZS11cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKSkFYZkJjZXd4V0ZDU29mV041c0hLWnNDU0M0Y3ZQdm1peC1NQjBsN1NQTzB6a2c9czk2LWM_c3o9NTA_c3o9NTAiLCJleHAiOjE5NjI5MzQzMzF9.dvWZShmYtkZJ8NDYjq4d5NXTWo588SHWtBeDZNIsiwA')
c.fetch_version()

#specify the part of the brain to analyze
criteria = NeuronCriteria(rois=['EB'])

#get neurons
neuron_df, roi_counts_df = fetch_neurons(criteria)

#get connectivity
adjacencies_df, conn_df = fetch_adjacencies(criteria)


#MAKE THE ADJACENCIES CSV. Change the weight qualifications as desired (the number of synapses between a pair of neurons for the edge between them to exist)
filtered = conn_df[
    (conn_df["roi"] == "EB") &
    (conn_df["weight"] >= 100)
]

filtered["a"] = filtered[["bodyId_pre", "bodyId_post"]].min(axis=1)
filtered["b"] = filtered[["bodyId_pre", "bodyId_post"]].max(axis=1)

#group and sum weights
result = (
    filtered.groupby(["a", "b", "roi"], as_index=False)["weight"]
      .sum()
      .rename(columns={"a": "bodyId_1", "b": "bodyId_2"})
      .sort_values("weight", ascending=False)
)

vertices = sorted(set(result["bodyId_1"]).union(result["bodyId_2"]))

#this is a dictionary. It makes a mapping of each vertex to its index in the weight matrix
index = {v: i for i, v in enumerate(vertices)}
n = len(vertices)
D = numpy.full((n, n), numpy.inf)
numpy.fill_diagonal(D, 0)

#This makes a weight matrix. The number being subtracted in w is the maximum number of synapses between any pair of neurons in the dataset, plus one. This allows the edges to be inversely weighted so that edges with more neurons get added first when we start with r=0 for our vietoris-ripps complex.
for _, row in result.iterrows():
    i = index[row["bodyId_1"]]
    j = index[row["bodyId_2"]]
    w = 1023 - row["weight"]

    D[i, j] = w
    D[j, i] = w

weight_df = pandas.DataFrame(D, columns = vertices)

weight_df.to_csv("weight_matrix.csv", index = False, header = False)


result.to_csv("EB_adjacencies.csv", index=False)


G = nx.Graph()

for _, row in filtered.iterrows():
    G.add_edge(
        row["bodyId_pre"],
        row["bodyId_post"],
        weight=row["weight"] / 30 #the weights would be too big otherwise
    )

net = Network()
net.from_nx(G)  # graph is imported here
net.show("graph.html", notebook=False)