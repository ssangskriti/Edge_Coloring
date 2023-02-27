import sys 
import os
# from qubo import *
from gurobi_qubo import *
from greedy import *
import networkx as nx
import time
from graphs.networkx_graphs import *
import csv


for key, graph in graph_list.items():
    # G.add_edges_from(graph)
    # print(G.edges)
    # nx.draw(G)
    # plt.show()
    
    G = graph
    
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



    print("solution to ",key," ", G)
    print("no of edges ", edges)
    print("no of nodes", nodes)
    print("maximum degree = ", max_deg)
    print("minimum degree = ", min_deg)
    print("average degree = ", avg_deg)



    # ---------------------greedy coloring---------------------------


    start = time.time()
    greedy_coloring, num_colors = edge_coloring(edge_list, e)
    greedy_time = time.time()

    # print("Greedy solution: ---------- ", greedy_coloring)
    print("number of colors for greedy solution: ", num_colors)
    print("greedy solver time: ", (greedy_time-start))


#     with open('results.txt', 'a') as f:
#         f.write('\n')
#         f.write("solution to "+str(key)+" "+ str(G))
#         f.write('\n')
#         f.write("no of edges "+str( edges))
#         f.write('\n')
#         f.write("no of nodes"+str( nodes))
#         f.write('\n')
#         f.write("maximum degree = "+str( max_deg))
#         f.write('\n')
#         f.write("minimum degree = "+str( min_deg))
#         f.write('\n')
#         f.write("average degree = "+str( avg_deg))
#         f.write('\n')

#         f.write("Greedy solution: ---------- "+str( greedy_coloring))
#         f.write('\n')
#         f.write("number of colors for greedy solution: "+str(num_colors))
#         f.write('\n')
#         f.write("greedy solver time: "+str( (greedy_time-start)))
#         f.write('\n')
    
    
    # -------------------------solver---------------------------------

    solvers = ["gurobi"]

    for solver in solvers:
        # ----------------------------delta coloring----------------------

        colors = max_deg

        
        qubo_coloring, qubo_time = qubo(colors, edge_list)
        


        print("no of colors for qubo: ", colors)
        if len(qubo_coloring)==0:
          print("-----no qubo solution for delta coloring------")
        else:
          # print("qubo solution: ---------", qubo_coloring)
          print(solver, " solver time: ", qubo_time)

        #  -----------------------delta+1 coloring------------------------

        if len(qubo_coloring) == 0:

            colors = max_deg+1
            
            qubo_coloring, qubo_time = qubo(colors, edge_list)


            print("no of colors for qubo: ", colors)
            if len(qubo_coloring)==0:
              print("-----no qubo solution for delta+1 coloring------")
            else:
              # print("qubo solution: ---------", qubo_coloring)
              print(solver, " solver time: ", qubo_time)
                
#         with open('results.txt', 'a') as f:

#             f.write("no of colors for qubo: "+str(colors))
#             f.write('\n')
#             f.write("qubo solution: ---------"+str(qubo_coloring))
#             f.write('\n')
#             f.write(str(solver)+ " solver time: "+str((qubo_time)))
#             f.write('\n')
                
            