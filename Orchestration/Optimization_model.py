import gurobipy




def mtztw(n,c,e,l):#############################################################
    """mtzts: model for the traveling salesman problem with time windows
    Parameters:
        - n: number of nodes
        - c[i,j]: cost for traversing arc (i,j)
        - e[i]: earliest date for visiting node i
        - l[i]: latest date for visiting node i
    Returns a model, ready to be solved.
    """

    model = gurobipy.Model("tsptw - mtz")
    x,u = {},{}
    for i in range(1,n+1):
        u[i] = model.addVar(lb=e[i], ub=l[i], vtype="C", name="u(%s)"%i)
        for j in range(1,n+1):
            if i != j:
                x[i,j] = model.addVar(vtype="B", name="x(%s,%s)"%(i,j))
    model.update()

    for i in range(1,n+1):
        model.addConstr(gurobipy.quicksum(x[i,j] for j in range(1,n+1) if j != i) == 1, "Out(%s)"%i)
        model.addConstr(gurobipy.quicksum(x[j,i] for j in range(1,n+1) if j != i) == 1, "In(%s)"%i)

    for i in range(1,n+1):
        for j in range(2,n+1):
            if i != j:
                M = max(l[i] + c[i,j] - e[j], 0)
                model.addConstr(u[i] - u[j] + M*x[i,j] <= M-c[i,j], "MTZ(%s,%s)"%(i,j))

    model.setObjective(gurobipy.quicksum(c[i,j]*x[i,j] for (i,j) in x),gurobipy.GRB.MINIMIZE)

    model.update()
    model.__data = x,u
    return model





def mtz2tw(n,c,e,l):
    """mtz: model for the traveling salesman problem with time windows
    (based on Miller-Tucker-Zemlin's one-index potential formulation, stronger constraints)
    Parameters:
        - n: number of nodes
        - c[i,j]: cost for traversing arc (i,j)
        - e[i]: earliest date for visiting node i
        - l[i]: latest date for visiting node i
    Returns a model, ready to be solved.
    """
    model = gurobipy.Model("tsptw - mtz-strong")
    x,u = {},{}
    for i in range(1,n+1):
        u[i] = model.addVar(lb=e[i], ub=l[i], vtype="C", name="u(%s)"%i)
        for j in range(1,n+1):
            if i != j:
                x[i,j] = model.addVar(vtype="B", name="x(%s,%s)"%(i,j))
    model.update()

    for i in range(1,n+1):
        model.addConstr(gurobipy.quicksum(x[i,j] for j in range(1,n+1) if j != i) == 1, "Out(%s)"%i)
        model.addConstr(gurobipy.quicksum(x[j,i] for j in range(1,n+1) if j != i) == 1, "In(%s)"%i)

        for j in range(2,n+1):
            if i != j:
                M1 = max(l[i] + c[i,j] - e[j], 0)
                M2 = max(l[i] + min(-c[j,i], e[j]-e[i]) - e[j], 0)
                model.addConstr(u[i] + c[i,j] - M1*(1-x[i,j]) + M2*x[j,i] <= u[j], "LiftedMTZ(%s,%s)"%(i,j))

    for i in range(2,n+1):
        model.addConstr(e[i] + gurobipy.quicksum(max(e[j]+c[j,i]-e[i],0) * x[j,i] for j in range(1,n+1) if i != j) \
                        <= u[i], "LiftedLB(%s)"%i)

        model.addConstr(u[i] <= l[i] - \
                        gurobipy.quicksum(max(l[i]-l[j]+c[i,j],0) * x[i,j] for j in range(2,n+1) if i != j), \
                        "LiftedUB(%s)"%i)

    model.setObjective(gurobipy.quicksum(c[i,j]*x[i,j] for (i,j) in x),gurobipy.GRB.MINIMIZE)

    model.update()
    model.__data = x,u
    return model


def tsptw2(n,c,e,l):
    """tsptw2: model for the traveling salesman problem with time windows
    (based on Miller-Tucker-Zemlin's formulation, two-index potential)
    Parameters:
        - n: number of nodes
        - c[i,j]: cost for traversing arc (i,j)
        - e[i]: earliest date for visiting node i
        - l[i]: latest date for visiting node i
    Returns a model, ready to be solved.
    """
    model = gurobipy.Model("tsptw2")
    x,u = {},{}
    for i in range(1,n+1):
        for j in range(1,n+1):
            if i != j:
                x[i,j] = model.addVar(vtype="B", name="x(%s,%s)"%(i,j))
                u[i,j] = model.addVar(vtype="C", name="u(%s,%s)"%(i,j))
    model.update()

    for i in range(1,n+1):
        model.addConstr(gurobipy.quicksum(x[i,j] for j in range(1,n+1) if j != i) == 1, "Out(%s)"%i)
        model.addConstr(gurobipy.quicksum(x[j,i] for j in range(1,n+1) if j != i) == 1, "In(%s)"%i)

    for j in range(2,n+1):
        model.addConstr(gurobipy.quicksum(u[i,j] + c[i,j]*x[i,j] for i in range(1,n+1) if i != j) -
                        gurobipy.quicksum(u[j,k] for k in range(1,n+1) if k != j) <= 0, "Relate(%s)"%j)

    for i in range(1,n+1):
        for j in range(1,n+1):
            if i != j:
                model.addConstr(e[i]*x[i,j] <= u[i,j], "LB(%s,%s)"%(i,j))
                model.addConstr(u[i,j] <= l[i]*x[i,j], "UB(%s,%s)"%(i,j))

    model.setObjective(gurobipy.quicksum(c[i,j]*x[i,j] for (i,j) in x),gurobipy.GRB.MINIMIZE)

    model.update()
    model.__data = x,u
    return model

