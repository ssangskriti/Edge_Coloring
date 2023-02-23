import networkx as nx
import matplotlib.pyplot as plt
# import pyomo.environ
from gurobipy import *
import time

def qubo(G,colors, edge_list):
    '''qubo solver'''
    
    start = time.time()
    
    model = Model()
    
    color =[]
    for k in range(1, colors+1):
        color.append(k)
    
    
    
    x = {}
    for a,b in edge_list:
        for k in color:
            x[a,b,k] = model.addVar(vtype=GRB.BINARY, name="x={0},{1}-{2}".format(a, b, k))
    
    model.update()
    
    # print(model.display())
    
    
    for a,b in edge_list:
        model.addConstr(quicksum(x[a,b,k] for k in color) == 1)
        
    for a,b in edge_list:
        for c,d in edge_list:
            if (a,b)!=(c,d):
                if (a==c or a==d or b==c or b==d):
                    for k in color:
                        model.addConstr((x[a,b,k]+x[c,d,k]) <=1)
            
            
            
    model.update()
    
    # print(model.display())
    
    model.setObjective(quicksum(x[a, b, k] for a, b in edge_list for k in color), GRB.MINIMIZE)
    
    
    
    # for a,b in edge_list:
    #     for c,d in edge_list:
    #         # model.setObjective(quicksum( (x[a, b, k] * x[c, d, k]) for k in color), GRB.MINIMIZE)
    #         if (a,b)!=(c,d):
    #             P = 20
    #             if a!=c and a!=d and b!=c and b!= d:
    #                 model.setObjective(quicksum( (x[a, b, k] * x[c, d, k]) for k in color), GRB.MINIMIZE)
    #                 model.update()
    #                 # continue
    #             else:
    #                 model.setObjective(quicksum((P* x[a,b,k]*x[c,d,k]) for k in color), GRB.MINIMIZE)
    #                 model.update()
                    # print(x[a,b,k]," ",x[c,d,k])
                
    model.update()
    # Optimize the model
    model.optimize()
    
    end = time.time()
    total_time = end-start
    
    # print("------------------------", model.status, "------------------------")
    
    qubo_coloring = {}
    # for v in model.getVars():
    #     # print('%s %g' % (v.VarName, v.X))
    #     if int(v.X) == 1:
            # print(v.VarName)

    for a, b, k in x:
        if int(x[a, b, k].X) == 1:
            qubo_coloring[(a, b)] = k
    
    # qubo_coloring = {}
    # for a,b in edge_list:
    #     for k in range(1, colors+1):
    #         if x[a,b,k] == 1:
    #             qubo_coloring[(a,b)] = k
    
    # print(qubo_coloring)
    
    # Check if the coloring is valid
    for a, b in qubo_coloring.keys():
        for c,d in qubo_coloring.keys():
            if (a,b)!=(c,d):
                if (a==c or a==d or b==c or b==d) and qubo_coloring[(a,b)] == qubo_coloring[(c,d)]:
                    qubo_coloring.clear()
                    break
        if len(qubo_coloring)==0:
            break
    
    return qubo_coloring, total_time
