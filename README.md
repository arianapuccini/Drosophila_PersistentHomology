Introduction:
This repository analyzes neuron data from the Neuprint dataset.

Possible methods:
* Point cloud to track where synapses are located in Euclidean space OR where the mid-point of neurons are
  - Increasing Euclidean dist
* Graph where neurons are vertices and are connected if they share a synapse, where the paths are unweighted
* Graph where synapses are vertices and are connected if they share a nueron, unweighted
  - Shortest path metric
  - Increasing by weight where weight is #synapses or #neurons
* Neurons as vertices with weighted edges, where edge weights' are inversly proportional to the number of synapse connections between neurons
  - Increasing shortest path distances defined by weight (MaxSyn - ConnSyn + 1)
  - Randomize initial weights, simulate training by randomly/linearly increasing/decreasing weights back to original value

  
