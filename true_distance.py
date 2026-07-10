#This makes the point cloud matrix (x,y,z columns) for synapses in the epsilloid body of the fly brain, specifically those that intake information from at least 100 neurons and deliver information to at least 400 neurons. This also creates an interactive graph so you can visualize the points in 3D. The ROI (region of interest) of the fly brain can be modified.

from neuprint import Client, fetch_synapses, NeuronCriteria as NC, SynapseCriteria as SC

from neuprint import fetch_synapses, NeuronCriteria as NC, SynapseCriteria as SC

import plotly.express as px

c = Client('neuprint.janelia.org', dataset='hemibrain:v1.2.1', token='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFyaWFuYXB1Y2NpbmlAZ21haWwuY29tIiwibGV2ZWwiOiJub2F1dGgiLCJpbWFnZS11cmwiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BQ2c4b2NKSkFYZkJjZXd4V0ZDU29mV041c0hLWnNDU0M0Y3ZQdm1peC1NQjBsN1NQTzB6a2c9czk2LWM_c3o9NTA_c3o9NTAiLCJleHAiOjE5NjI5MzQzMzF9.dvWZShmYtkZJ8NDYjq4d5NXTWo588SHWtBeDZNIsiwA')
c.fetch_version()

neuron_criteria = NC(status='Traced', type='FB4Y', cropped=False, inputRois=['EB'], min_roi_inputs=100, min_pre=400)
eb_syn_criteria = SC(rois='EB', type = 'pre', primary_only=True)
eb_tbars = fetch_synapses(neuron_criteria, eb_syn_criteria)

eb_synapse_coords = eb_tbars[['x', 'y', 'z']]

eb_synapse_coords.to_csv("eb_synapse_coords.csv", index=False)

fig = px.scatter_3d(
    eb_synapse_coords,
    x="x",
    y="y",
    z="z",
    opacity=0.7
)

fig.update_traces(
    marker=dict(
        size=3
    )
)

fig.update_layout(
    scene=dict(
        aspectmode="data",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        zaxis=dict(visible=False),
        bgcolor='rgba(0,0,0,0)'
    ),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)'
)

fig.show()
