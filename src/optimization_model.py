from gurobipy import Model, GRB

def optimize_planning():
    model = Model("OptimizationModel")
    
    # Define variables
    x = model.addVar(vtype=GRB.CONTINUOUS, name="x")
    y = model.addVar(vtype=GRB.CONTINUOUS, name="y")

    # Objective function
    model.setObjective(3*x + 2*y, GRB.MAXIMIZE)

    # Constraints
    model.addConstr(x + 2*y <= 10, "Constraint1")
    model.addConstr(2*x + y <= 8, "Constraint2")

    # Optimize the model
    model.optimize()

    return {var.varName: var.x for var in model.getVars()}
