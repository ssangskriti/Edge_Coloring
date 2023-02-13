import networkx as nx


# graph_list=[[(0,2),(0,4),(1,2),(1,7),(2,3),(3,5),(3,4),(4,5),(4,6),(6,7)],
#             [(0,1),(0,4),(1,2),(1,4),(2,3),(3,4)]]


# G = nx.Graph()
# # G.add_edges_from([(0,2),(0,4),(1,2),(1,7),(2,3),(3,5),(3,4),(4,5),(4,6),(6,7)])
# # G.add_edges_from([(0,1),(0,4),(1,2),(1,4),(2,3),(3,4)])

# for graph in graph_list:
#     G.add_edges_from(graph)
#     print(G.edges)



graphs= [nx.dorogovtsev_goltsev_mendes_graph(2)]

graph_list={}
count = 1

for g in graphs:
    graph_list[count] = g
    count+=1