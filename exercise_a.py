import numpy as np
import sys

f=open(sys.argv[ 1], "r")

# read first line
num_nodes=int(f.readline())
print ("Number of nodes: %d" % num_nodes)

# allocate memory for weights
node_weight=np.empty(num_nodes)

# read weights
node_weight=np.array(f.readline().split(), dtype=np.float64)
print ("Node weight: ", node_weight)

# allocate memory for adjacency list
adj_list=np.empty([ num_nodes, num_nodes])

# read edges
for idx in range(num_nodes):
	adj_list[ idx, :]=np.array(f.readline().split())

# record node degree
node_deg=np.zeros(num_nodes)
for row in range(num_nodes):
	for col in range(num_nodes):
		if adj_list[ row, col]==1:
			node_deg[ row]+=1
print ("Node degree: ", node_deg)
avg_weight=node_weight/(node_deg+1)
print ("Average weight: ", avg_weight)
print (np.argmax(avg_weight))

# algorithm starts here
MWIS=[ ]
weight_sum=0
while sum(avg_weight)!=0:
	# greedy select 
	selected_node=np.argmax(avg_weight)
	print ("Node %d selected" % selected_node)
	MWIS.append(selected_node)
	weight_sum+=node_weight[ selected_node]
	# update degree
	node_deg[ :]=node_deg-adj_list[ selected_node,:]
	# update weight
	node_weight[ selected_node]=0
	node_weight[ :]=np.multiply(node_weight, (np.ones(num_nodes)-adj_list[ selected_node, :]))
	# update avg weight
	avg_weight[ :]=node_weight/(node_deg+1)
	print ("New average weight: ", avg_weight)

print ("MWIS: ", sorted(MWIS), "Weight: ", weight_sum)
