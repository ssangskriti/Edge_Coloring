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

# ----------------------graph-stats------------------------------

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



# ---------------------greedy coloring---------------------------


start = time.time()
greedy_coloring, num_colors = edge_coloring(edge_list, e)
greedy_time = time.time()

print("Greedy solution: ---------- ", greedy_coloring)
print("number of colors for greedy solution: ", num_colors)
print("greedy solver time: ", (greedy_time-start))


# -------------------------solver---------------------------------

solvers = ["gurobi","bonmin","cplex_direct","xpress"]

for solver in solvers:
    # ----------------------------delta coloring----------------------

    colors = max_deg

    start = time.time()
    qubo_coloring = qubo(G, colors, edge_list, solver)
    qubo_time = time.time()


    print("no of colors for qubo: ", colors)
    if len(qubo_coloring)==0:
      print("-----no qubo solution for delta coloring------")
    else:
      print("qubo solution: ---------", qubo_coloring)
      print(solver, " solver time: ", (qubo_time-start))

    #  -----------------------delta+1 coloring------------------------

    if len(qubo_coloring) == 0:

        colors = max_deg+1
        start = time.time()
        qubo_coloring = qubo(G, colors, edge_list, solver)
        qubo_time = time.time()


        print("no of colors for qubo: ", colors)
        if len(qubo_coloring)==0:
          print("-----no qubo solution for delta+1 coloring------")
        else:
          print("qubo solution: ---------", qubo_coloring)
          print(solver, " solver time: ", (qubo_time-start))