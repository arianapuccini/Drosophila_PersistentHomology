'''
This code can be used by adding bodyIds of neurons of interest to the lists a and b. 
The code will then fetch the synapse connections between the two sets of neurons, 
fetch the skeletons for the neurons, and plot them in the x-y plane.
'''


from neuprint import Client, fetch_synapse_connections
from neuprint import NeuronCriteria as NC, SynapseCriteria as SC
import matplotlib.pyplot as plt

c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', 
           token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFyaWFuYXB1Y2NpbmlAZ21haWwuY29tIiwibGV2ZWwiOiJub2F1dGgiLCJpbWFnZS11cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKSkFYZkJjZXd4V0ZDU29mV041c0hLWnNDU0M0Y3ZQdm1peC1NQjBsN1NQTzB6a2c9czk2LWM_c3o9NTA_c3o9NTAiLCJleHAiOjE5NjI5MzQzMzF9.dvWZShmYtkZJ8NDYjq4d5NXTWo588SHWtBeDZNIsiwA')
c.fetch_version()

# bodyIds for interested neurons
a = [1008378448,978733459]
b = [1008378448,973566036]

# Fetch synapse connections between the two sets of neurons
syns2fetch = fetch_synapse_connections(a, b)

# To check details:
# display(syns2fetch)

# Fetch skeletons for the neurons
sPre1 = c.fetch_skeleton(a[0])
sPost1 = c.fetch_skeleton(b[0])

# Plot
fig, ax = plt.subplots(1, figsize=(8,8))
ax.scatter(sPre1['x'][0], sPre1['y'][0], color='black')
ax.plot(sPre1['x'], sPre1['y'], color='#33FFF9', alpha=0.3) # light blue
ax.scatter(sPost1['x'][0], sPost1['y'][0], color='black')
ax.plot(sPost1['x'], sPost1['y'], color='blue', alpha=0.3)
ax.scatter(syns2fetch['x_post'], syns2fetch['y_post'], color='r')
ax.axis('off')
plt.title('x-y plane')
plt.show()