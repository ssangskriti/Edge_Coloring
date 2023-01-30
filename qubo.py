import networkx as nx
import matplotlib.pyplot as plt
from pyomo.environ import *

import xpress



def qubo(G, colors, edge_list, solver):
    '''qubo solver'''
    model = ConcreteModel()
    model.K = RangeSet(1, colors)
    model.E = Set(initialize= edge_list)

    # model.E.pprint()
    # model.K.pprint()

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
    
    if solver == 'cplex':
        solver = SolverFactory('cplex_direct')
    elif solver == 'xpress':
        solver = SolverFactory('xpress')
    elif solver == 'couenne':
        solver = SolverFactory('couenne')
    elif solver == 'bonmin':
        solver = SolverFactory('bonmin')
        
    solver.options['timelimit'] = 10
    result = solver.solve(model)
    print(result)

    # model.pprint()
    # time = result.
    
    qubo_coloring = {}
    count = 1
    for u in model.E:
      # print("Edge: ", count)
      count+=1
      for k in model.K:
          if model.x[u,k].value == 1:
              # print("Edge ", u, " is assigned color ", k)
              qubo_coloring[u] = k
        
    # correctness
    # for a, b in qubo_coloring.keys():
    #   for c,d in qubo_coloring.keys():
    #     if (a,b)!=(c,d):
    #       if (a==c or a==d or b==c or b==d) and qubo_coloring[(a,b)] == qubo_coloring[(c,d)]:
    #         qubo_coloring.clear()
    #         break
    #   if len(qubo_coloring)==0:
    #     break
    
    return qubo_coloring