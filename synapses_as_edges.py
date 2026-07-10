#This is a dual script to neurondata. Here, synapses represent NODES and neurons represent EDGES. Two synapses are connected if they are both attached to the same neuron. This makes a distance matrix encoding this synapse-adjacency information.

from neuprint import Client, fetch_synapse_connections

from neuprint import NeuronCriteria as NC, SynapseCriteria as SC

import pandas, networkx as nx

#defaultdict is useful when we are going to add more than one thing to a key (like a list of synapses to a neuron) and we don't want to have to check every time for the existence of a key
from collections import defaultdict

from itertools import combinations


c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFyaWFuYXB1Y2NpbmlAZ21haWwuY29tIiwibGV2ZWwiOiJub2F1dGgiLCJpbWFnZS11cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKSkFYZkJjZXd4V0ZDU29mV041c0hLWnNDU0M0Y3ZQdm1peC1NQjBsN1NQTzB6a2c9czk2LWM_c3o9NTA_c3o9NTAiLCJleHAiOjE5NjI5MzQzMzF9.dvWZShmYtkZJ8NDYjq4d5NXTWo588SHWtBeDZNIsiwA')
c.fetch_version()

neuron_criteria = NC(status='Traced', type='FB4Y', cropped=False, inputRois=['EB'], min_roi_inputs=100, min_pre=400)
eb_syn_criteria = SC(rois='EB', primary_only=True)
eb_conns = fetch_synapse_connections(neuron_criteria, None, eb_syn_criteria)
print(eb_conns)

refined_eb_conns = eb_conns[["bodyId_pre", "bodyId_post"]].drop_duplicates()
print(refined_eb_conns)

neurons_to_synapses = defaultdict(list)

for index, row in refined_eb_conns.iterrows():
    neurons_to_synapses[row["bodyId_pre"]].append(index)
    neurons_to_synapses[row["bodyId_post"]].append(index)

G = nx.Graph()

#What do the synapse vertices represent? They represent the fact that there IS is a synapse between two neurons

#What do the neuron edges represent? They represent the fact that two synapses are connected to the same neuron

G.add_nodes_from(refined_eb_conns.index)

for synapses in neurons_to_synapses.values():
    G.add_edges_from(combinations(synapses, 2))

#These three lines make a physical network we can see, but it takes too much processing power for the size of graphs we are dealing with. It is here if we need it
#net = Network()
#net.from_nx(G)  # graph is imported here
#net.show("graph.html", notebook=False)


#synapses may be way more connected than we thought
D = nx.floyd_warshall_numpy(G)
distance_matrix = pandas.DataFrame(D)
distance_matrix.to_csv("synapse_distance_matrix.csv")

degrees = [d for _, d in G.degree()]

print("Number of nodes:", G.number_of_nodes())
print("Average degree:", sum(degrees)/len(degrees))
print("Maximum degree:", max(degrees))

from collections import Counter

counts = Counter()

for source, lengths in nx.shortest_path_length(G):
    counts.update(lengths.values())

print(counts)