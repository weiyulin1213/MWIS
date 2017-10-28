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
old_MWIS=[ ]
MWIS=[ ]
pre_MWIS=[ ]
weight_sum=0
done=False
_round=0
jump_in_before=np.zeros(num_nodes)
# for computation purpose
adj_list=adj_list+np.eye(num_nodes)
while done==False:
	print ("Round: ", _round)
	print ("Current MWIS: ", MWIS)
	print ("Old MWIS: ", old_MWIS)
	print ("Pre MWIS: ", pre_MWIS)
	# greedy select 
	for node_id in range(num_nodes):
		# check whether I should jump out of MWIS
		try:
			dummy=MWIS.index(node_id)
			# I am in MWIS, check if I can still stay in MWIS
			dif=list(set(pre_MWIS) ^ set(MWIS))
			for node in dif:
				if adj_list[ node_id, node]==1 and avg_weight[ node_id]<avg_weight[ node]:
					MWIS.remove(node_id)
					weight_sum-=node_weight[ node_id]
					print ("Node %d removed due to conflict" % node_id)
		except ValueError:
			# I am not in MWIS, nothing to worry
			dummy=-1
		# if I am max in my neighborhood
		if np.argmax(np.multiply(avg_weight, adj_list[ node_id, :]))==node_id and jump_in_before[ node_id]==0:
			MWIS.append(node_id)
			weight_sum+=node_weight[ node_id]
			jump_in_before[ node_id]=1;
			print ("Node %d selected" % node_id)
		# after first round, if my neighborhood is not in MWIS, Maybe I can join MWIS
		if _round!=0:
			try:
				pre_MWIS.index(node_id)
			except ValueError:
				join=1
				for i in range(num_nodes):
					if adj_list[ node_id, i]==1:
						try:
							MWIS.index(i)
							join=0
						except ValueError:
							join=join
				if join==1:
					MWIS.append(node_id)
					weight_sum+=node_weight[ node_id]
					jump_in_before[ node_id]=1
					print ("Node %d selected" % node_id)


	# check stop condition 
	print ("After this round")
	print ("Current MWIS: ", MWIS)
	print ("Old MWIS: ", old_MWIS)
	print ("Pre MWIS: ", pre_MWIS)
	if len(set(pre_MWIS) ^ set(MWIS))==0:
		break
	pre_MWIS=old_MWIS[ :]
	old_MWIS=MWIS[ :]
	_round+=1

print ("MWIS: ", sorted(MWIS), "Weight: ", weight_sum)
