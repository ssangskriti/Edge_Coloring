import sys 
import os
from qubo import *
from greedy import *
import networkx as nx
import time


G = nx.Graph()
G.add_edges_from([(0,2),(0,4),(1,2),(1,7),(2,3),(3,5),(3,4),(4,5),(4,6),(6,7)])
# nx.draw(G)
# plt.show()



# edges to edgelist
e = len(G.edges)
edge_list=[]
for i in G.edges:
  edge_list.append(i)
# print(type(edge_list))

# nodes and edges
nodes = G.number_of_nodes()
# print("no of nodes", nodes)
edges = len(G.edges)
# print("no of edges ", edges)

# degrees
max_deg = 0
min_deg = edges
total_deg = 0

for n in range(0, nodes):
  if G.degree[n] > max_deg:
    max_deg  = G.degree[n]
  if G.degree[n] < min_deg:
    min_deg = G.degree[n]

    total_deg+=G.degree[n]

avg_deg = total_deg/nodes 

# print("maximum degree = ", max_deg)
# print("minimum degree = ", min_deg)
# print("average degree = ", avg_deg)

# for u in G.edges():
#   print(u)



print("solution: ")
print("no of edges ", edges)
print("no of nodes", nodes)
print("maximum degree = ", max_deg)
print("minimum degree = ", min_deg)
print("average degree = ", avg_deg)



colors = max_deg
start = time.time()
qubo_coloring = qubo(G, colors, edge_list, 'cplex')
qubo_time = time.time()
greedy_coloring = edge_coloring(edge_list, colors)
greedy_time = time.time()
print("no of colors: ", colors)
if greedy_coloring == 0:
    print("no greedy solution")
else:
    print("Greedy solution: ", greedy_coloring)
    print("greedy solver time: ", (greedy_time-qubo_time))
if len(qubo_coloring)==0:
  print("no qubo solution")
else:
  print(qubo_coloring)
  print("qubo solver time: ", (qubo_time-start))



if len(qubo_coloring) == 0:
    colors = max_deg+1
    start = time.time()
    qubo_coloring = qubo(G, colors, edge_list, 'cplex')
    qubo_time = time.time()
    greedy_coloring = edge_coloring(edge_list, colors)
    greedy_time = time.time()
    print("no of colors: ", colors)
    if greedy_coloring == 0:
        print("no greedy solution")
    else:
        print("Greedy solution: ", greedy_coloring)
        print("greedy solver time: ", (greedy_time-qubo_time))
    if len(qubo_coloring)==0:
      print("no qubo solution")
    else:
      print(qubo_coloring)
      print("qubo solver time: ", (qubo_time-start))