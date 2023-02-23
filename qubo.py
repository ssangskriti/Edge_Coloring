import networkx as nx
import matplotlib.pyplot as plt
from pyomo.environ import *
# import gurobipy
import time

def qubo(G, colors, edge_list, solver):
    '''qubo solver'''
    
    # start = time.time()
    
    model = ConcreteModel()
    model.K = RangeSet(1, colors)
    model.E = Set(initialize= edge_list)

    # model.E.pprint()
    # model.K.pprint()

    model.x = Var(model.E | {(v2,v1) for v1, v2 in G.edges}, model.K, within=Binary)

    # model.x.pprint()


    # coloring constraint
    model.color_constr = ConstraintList()
    for a,b in edge_list:
        model.color_constr.add(sum(model.x[a,b,k] for k in model.K) == 1)
    
    # model.color_constr.pprint()
    
    model.edge_constr = ConstraintList()
    for a,b in edge_list:
        for c,d in edge_list:
            if (a,b)!=(c,d):
                if (a==c or a==d or b==c or b==d):
                    model.edge_constr.add(sum(model.x[a,b,k]+model.x[c,d,k] for k in RangeSet(1,colors)) <=1)

    # model.edge_constr.pprint()
    
    
#     def obj_expression(model):

#       for a,b in G.edges:
#         for c,d in G.edges:
#           for k in RangeSet(1,colors):
#             P = 20
#             if a!=c and a!=d and b!=c and b!= d:
#               model.obj.expr += model.x[a, b, k] * model.x[c, d, k]
#             else:
#               model.obj.expr+= P* model.x[a,b,k]*model.x[c,d,k]


    # obj_expression(model)
    
    # model.penal = Var(within=Binary)
    # model.penalties = ConstraintList()
    # model.penalties.add(expr = model.x <=P*model.penal)

    
    model.obj = Objective(expr = 0, sense=minimize)
    # model.pprint()
    P = 4
    def obj_expression(P):
        for a,b in G.edges:
            for c,d in G.edges:
                for k in RangeSet(1,colors): 
                    if a!=c and a!=d and b!=c and b!= d:
                        continue
                    else:
                        model.obj.expr+= P* model.x[a,b,k]*model.x[c,d,k]
                        # print(model.obj.expr)
    
    obj_expression(P)
    
    solver = SolverFactory(solver)
    
    opt = solver
    if opt == 'gurobi':
      solver.options['TimeLimit'] = 10
    elif opt=='bonmin':
      solver.options['bonmin.time_limit'] = 10
      # solver.options['bonmin.solution_limit'] = '1'
    elif opt=='ipopt':
      solver.options['max_cpu_time'] = 10
    
    
    result = solver.solve(model)
    
    # end = time.time()
    # total_time = end-start
    total_time = result.Solver.time
    
    print("------------------------", result, "------------------------")

    # model.pprint()
    
    
    qubo_coloring = {}
    # count = 1
    for u in model.E:
      # print("Edge: ", count)
      # count+=1
      for k in model.K:
          if model.x[u,k].value == 1:
              # print("Edge ", u, " is assigned color ", k)
              qubo_coloring[u] = k
       
    
    
    #correctness
    for a, b in qubo_coloring.keys():
      for c,d in qubo_coloring.keys():
        if (a,b)!=(c,d):
          if (a==c or a==d or b==c or b==d) and qubo_coloring[(a,b)] == qubo_coloring[(c,d)]:
            qubo_coloring.clear()
            break
      if len(qubo_coloring)==0:
        break
    
    return qubo_coloring, total_time