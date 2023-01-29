import networkx as nx
import matplotlib.pyplot as plt
from pyomo.environ import *

G = nx.Graph()
G.add_edges_from([(0,2),(0,4),(1,2),(1,7),(2,3),(3,5),(3,4),(4,5),(4,6),(6,7)])
# G.add_edges_from([(0,1),(0,4),(1,2),(1,4),(2,3),(3,4)])
nx.draw(G)
plt.show()
print(type(G.edges))
print(list(G[0].keys()))

e = len(G.edges)
edge_list=[]
for i in G.edges:
  edge_list.append(i)
print(type(edge_list))

nodes = G.number_of_nodes()
print("no of nodes", nodes)
edges = len(G.edges)
print("no of edges ", edges)
max_deg = 0

for n in range(0, nodes):
  if G.degree[n] > max_deg:
    max_deg  = G.degree[n]

print("maximum degree = ", max_deg)

colors = max_deg

model = ConcreteModel()
model.K = RangeSet(1, colors)
model.E = Set(initialize= edge_list)

model.E.pprint()
model.K.pprint()

model.x = Var(model.E | {(v2,v1) for v1, v2 in G.edges}, model.K, within=Binary)

# model.x.pprint()

model.obj = Objective(expr = 0, sense=minimize)
# model.pprint()


# coloring constraint
model.color_constr = ConstraintList()
for a,b in G.edges:
    model.color_constr.add(sum(model.x[a,b,k] for k in model.K) == 1)
    

def obj_expression(model):

  for a,b in G.edges:
    for c,d in G.edges:
      for k in RangeSet(1,colors):
        P = 20
        if a!=c and a!=d and b!=c and b!= d:
          model.obj.expr += model.x[a, b, k] * model.x[c, d, k]
        else:
          model.obj.expr+= P* model.x[a,b,k]*model.x[c,d,k]
  
  
obj_expression(model)

solver = SolverFactory('cplex_direct')
# solver = SolverFactory('xpress')
# solver = SolverFactory('couenne', executable="/content/couenne")
# solver = SolverFactory('bonmin', executable='/content/bonmin')
result = solver.solve(model)
print(result)

model.pprint()

count = 1
for u in model.E:
  print("Edge: ", count)
  count+=1
  for k in model.K:
      if model.x[u,k].value == 1:
          print("Edge ", u, " is assigned color ", k)