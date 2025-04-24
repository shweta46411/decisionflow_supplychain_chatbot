# import pandas as pd
# from gurobipy import Model, GRB
# import os

# # Define paths
# DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
# TRANSPORTATION_FILE = os.path.join(DATA_DIR, "transportation.csv")
# DEMAND_FILE = os.path.join(DATA_DIR, "demands.csv")
# PROCESSING_FILE = os.path.join(DATA_DIR, "processing.csv")

# def run_optimization():
#     """Runs the Gurobi optimization model based on the latest datasets."""
    
#     # Load data
#     transportation_df = pd.read_csv(TRANSPORTATION_FILE)
#     demand_df = pd.read_csv(DEMAND_FILE)
#     processing_df = pd.read_csv(PROCESSING_FILE)

#     # Create Gurobi model
#     model = Model("Supply_Chain_Optimization")

#     # Decision variables
#     x, y = {}, {}
    
#     for _, row in transportation_df.iterrows():
#         s, r, t = row["from"], row["to"], row["coffee_type"]
#         x[s, r, t] = model.addVar(lb=0, ub=row["capacity"], vtype=GRB.CONTINUOUS, name=f"x_{s}_{r}_{t}")

#     for _, row in demand_df.iterrows():
#         c, t = row["cafe"], row["coffee_type"]
#         for r in processing_df[processing_df["entity_type"] == "roastery"]["entity"].unique():
#             y[r, c, t] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name=f"y_{r}_{c}_{t}")

#     # Objective function: Minimize cost
#     model.setObjective(
#         sum(transportation_df.loc[(transportation_df["from"] == s) &
#                                   (transportation_df["to"] == r) &
#                                   (transportation_df["coffee_type"] == t), "cost"].iloc[0] * x[s, r, t]
#             for s, r, t in x.keys()) +
#         sum(transportation_df.loc[(transportation_df["from"] == r) &
#                                   (transportation_df["to"] == c) &
#                                   (transportation_df["coffee_type"] == t), "cost"].iloc[0] * y[r, c, t]
#             for r, c, t in y.keys()),
#         GRB.MINIMIZE
#     )

#     # Optimize model
#     model.optimize()

#     # Extract results
#     results = []
#     if model.status == GRB.OPTIMAL:
#         for s, r, t in x.keys():
#             if x[s, r, t].x > 0:
#                 results.append({"From": s, "To": r, "Coffee Type": t, "Quantity": x[s, r, t].x, "Mode": "Supplier to Roastery"})

#         for r, c, t in y.keys():
#             if y[r, c, t].x > 0:
#                 results.append({"From": r, "To": c, "Coffee Type": t, "Quantity": y[r, c, t].x, "Mode": "Roastery to Cafe"})

#     return pd.DataFrame(results) if results else pd.DataFrame(columns=["From", "To", "Coffee Type", "Quantity", "Mode"])
import gurobipy as gp
from gurobipy import GRB
import pandas as pd

# Load datasets
demands_df = pd.read_csv("data/demands.csv")
processing_df = pd.read_csv("data/processing.csv")
transportation_df = pd.read_csv("data/transportation.csv")
import pandas as pd
from gurobipy import Model, GRB

def run_optimization(demand_df, processing_df, transportation_df):
    # demand_df = pd.read_csv("data/demands.csv")
    # processing_df = pd.read_csv("data/processing.csv")
    # transportation_df = pd.read_csv("data/transportation.csv")

    model = Model("Supply_Chain_Optimization")
    model.setParam("OutputFlag", 0)  # silent mode

    # Supplier → Roastery
    x = {}
    for _, row in transportation_df.iterrows():
        s, r, t = row["from"], row["to"], row["coffee_type"]
        x[s, r, t] = model.addVar(lb=0, ub=row["capacity"], vtype=GRB.CONTINUOUS)

    # Roastery → Café
    y = {}
    for _, row in demand_df.iterrows():
        c, t = row["cafe"], row["coffee_type"]
        for r in processing_df[processing_df["entity_type"] == "roastery"]["entity"].unique():
            y[r, c, t] = model.addVar(lb=0, vtype=GRB.CONTINUOUS)

    # Objective: total cost
    model.setObjective(
        sum(transportation_df.loc[
                (transportation_df["from"] == s) &
                (transportation_df["to"] == r) &
                (transportation_df["coffee_type"] == t), "cost"
            ].iloc[0] * x[s, r, t]
            for s, r, t in x) +
        sum(transportation_df.loc[
                (transportation_df["from"] == r) &
                (transportation_df["to"] == c) &
                (transportation_df["coffee_type"] == t), "cost"
            ].iloc[0] * y[r, c, t]
            for r, c, t in y) +
        sum(processing_df.loc[
                (processing_df["entity"] == s) &
                (processing_df["coffee_type"] == t), "cost"
            ].iloc[0] * x[s, r, t]
            for s, r, t in x) +
        sum(processing_df.loc[
                (processing_df["entity"] == r) &
                (processing_df["coffee_type"] == t), "cost"
            ].iloc[0] * y[r, c, t]
            for r, c, t in y),
        GRB.MINIMIZE
    )

    # Constraints
    for _, row in processing_df[processing_df["entity_type"] == "supplier"].iterrows():
        s, t = row["entity"], row["coffee_type"]
        model.addConstr(
            sum(x[s, r, t] for r in transportation_df[transportation_df["from"] == s]["to"].unique() if (s, r, t) in x)
            <= row["capacity"]
        )

    for _, row in processing_df[processing_df["entity_type"] == "roastery"].iterrows():
        r, t = row["entity"], row["coffee_type"]
        model.addConstr(
            sum(x[s, r, t] for s in transportation_df[transportation_df["to"] == r]["from"].unique() if (s, r, t) in x)
            <= row["capacity"]
        )

    for r in processing_df[processing_df["entity_type"] == "roastery"]["entity"].unique():
        for t in demand_df["coffee_type"].unique():
            model.addConstr(
                sum(x[s, r, t] for s in transportation_df[transportation_df["to"] == r]["from"].unique() if (s, r, t) in x)
                == sum(y[r, c, t] for c in demand_df["cafe"].unique() if (r, c, t) in y)
            )

    for _, row in transportation_df.iterrows():
        r, c, t, cap = row["from"], row["to"], row["coffee_type"], row["capacity"]
        if (r, c, t) in y:
            model.addConstr(y[r, c, t] <= cap)

    for _, row in demand_df.iterrows():
        c, t, d = row["cafe"], row["coffee_type"], row["demand"]
        model.addConstr(
            sum(y[r, c, t] for r in transportation_df[transportation_df["to"] == c]["from"].unique() if (r, c, t) in y)
            == d
        )

    model.optimize()

    result = {
        "status": "optimal" if model.status == GRB.OPTIMAL else "infeasible",
        "total_cost": model.objVal if model.status == GRB.OPTIMAL else None,
        "supplier_to_roastery": [
            {"from": s, "to": r, "coffee_type": t, "quantity": x[s, r, t].x}
            for s, r, t in x if x[s, r, t].x > 0
        ],
        "roastery_to_cafe": [
            {"from": r, "to": c, "coffee_type": t, "quantity": y[r, c, t].x}
            for r, c, t in y if y[r, c, t].x > 0
        ]
    }

    return result

# def run_optimization():
#     """Optimization model using Gurobi"""
#     model = gp.Model("Supply_Chain_Optimization")

#     # Define decision variables
#     x = {}
#     for _, row in transportation_df.iterrows():
#         s, r, t = row["from"], row["to"], row["coffee_type"]
#         x[s, r, t] = model.addVar(lb=0, ub=row["capacity"], vtype=GRB.CONTINUOUS, name=f"x_{s}_{r}_{t}")

#     # Define objective function (minimizing cost)
#     model.setObjective(
#         gp.quicksum(transportation_df.loc[
#             (transportation_df["from"] == s) & (transportation_df["to"] == r) & (transportation_df["coffee_type"] == t), "cost"].iloc[0] * x[s, r, t]
#             for s, r, t in x.keys()),
#         GRB.MINIMIZE
#     )

#     # Optimize model
#     model.optimize()

#     if model.status == GRB.OPTIMAL:
#         return f"Optimization completed. Total cost: ${model.objVal:.2f}"
#     else:
#         return "Optimization could not find an optimal solution."

import pandas as pd
from gurobipy import Model, GRB
import os

# Define paths
DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
TRANSPORTATION_FILE = os.path.join(DATA_DIR, "transportation.csv")
DEMAND_FILE = os.path.join(DATA_DIR, "demands.csv")
PROCESSING_FILE = os.path.join(DATA_DIR, "processing.csv")

# def run_optimization():
#     """Run supply chain optimization with dynamically loaded data."""
#     global latest_optimization_results  
#     # Load datasets dynamically
#     transportation_df = pd.read_csv(TRANSPORTATION_FILE)
#     demand_df = pd.read_csv(DEMAND_FILE)
#     processing_df = pd.read_csv(PROCESSING_FILE)

#     # Initialize the Gurobi model
#     model = Model("Supply_Chain_Optimization")
#     model.setParam("OutputFlag", 0)  # Suppress solver output

#     # Decision variables for transportation from supplier to roastery
#     x = {}
#     for _, row in transportation_df.iterrows():
#         s, r, t = row["from"], row["to"], row["coffee_type"]
#         x[s, r, t] = model.addVar(lb=0, ub=row["capacity"], vtype=GRB.CONTINUOUS, name=f"x_{s}_{r}_{t}")

#     # Decision variables for transportation from roasteries to cafes
#     y = {}
#     for _, row in demand_df.iterrows():
#         c, t = row["cafe"], row["coffee_type"]
#         for r in processing_df[processing_df["entity_type"] == "roastery"]["entity"].unique():
#             y[r, c, t] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name=f"y_{r}_{c}_{t}")

#     # Objective Function: Minimize total cost (transportation + processing)
#     model.setObjective(
#         sum(transportation_df.loc[(transportation_df["from"] == s) &
#                                   (transportation_df["to"] == r) &
#                                   (transportation_df["coffee_type"] == t), "cost"].iloc[0] * x[s, r, t]
#             for s, r, t in x.keys()) +
#         sum(transportation_df.loc[(transportation_df["from"] == r) &
#                                   (transportation_df["to"] == c) &
#                                   (transportation_df["coffee_type"] == t), "cost"].iloc[0] * y[r, c, t]
#             for r, c, t in y.keys()) +
#         sum(processing_df.loc[(processing_df["entity"] == s) &
#                               (processing_df["coffee_type"] == t), "cost"].iloc[0] * x[s, r, t]
#             for s, r, t in x.keys()) +
#         sum(processing_df.loc[(processing_df["entity"] == r) &
#                               (processing_df["coffee_type"] == t), "cost"].iloc[0] * y[r, c, t]
#             for r, c, t in y.keys()),
#         GRB.MINIMIZE
#     )

#     # Supplier Capacity Constraint
#     for _, row in processing_df[processing_df["entity_type"] == "supplier"].iterrows():
#         s, t = row["entity"], row["coffee_type"]
#         model.addConstr(
#             sum(x[s, r, t] for r in transportation_df[transportation_df["from"] == s]["to"].unique() if (s, r, t) in x)
#             <= processing_df.loc[(processing_df["entity"] == s) & (processing_df["coffee_type"] == t), "capacity"].iloc[0],
#             name=f"SupplierCapacity_{s}_{t}"
#         )

#     # Roastery Processing Capacity Constraint
#     for _, row in processing_df[processing_df["entity_type"] == "roastery"].iterrows():
#         r, t = row["entity"], row["coffee_type"]
#         model.addConstr(
#             sum(x[s, r, t] for s in transportation_df[transportation_df["to"] == r]["from"].unique() if (s, r, t) in x)
#             <= processing_df.loc[(processing_df["entity"] == r) & (processing_df["coffee_type"] == t), "capacity"].iloc[0],
#             name=f"RoasteryCapacity_{r}_{t}"
#         )

#     # Flow Conservation Constraint
#     for r in processing_df[processing_df["entity_type"] == "roastery"]["entity"].unique():
#         for t in demand_df["coffee_type"].unique():
#             model.addConstr(
#                 sum(x[s, r, t] for s in transportation_df[transportation_df["to"] == r]["from"].unique() if (s, r, t) in x)
#                 == sum(y[r, c, t] for c in demand_df["cafe"].unique() if (r, c, t) in y),
#                 name=f"FlowConservation_{r}_{t}"
#             )

#     # Transportation Capacity Constraint
#     for _, row in transportation_df.iterrows():
#         r, c, t, max_capacity = row["from"], row["to"], row["coffee_type"], row["capacity"]
#         if (r, c, t) in y:
#             model.addConstr(
#                 y[r, c, t] <= max_capacity,
#                 name=f"RoasteryToCafeCapacity_{r}_{c}_{t}"
#             )

#     # Demand Fulfillment Constraint
#     for _, row in demand_df.iterrows():
#         c, t, d = row["cafe"], row["coffee_type"], row["demand"]
#         model.addConstr(
#             sum(y[r, c, t] for r in transportation_df[transportation_df["to"] == c]["from"].unique() if (r, c, t) in y)
#             == d,
#             name=f"DemandFulfillment_{c}_{t}"
#         )

#     # Solve model
#     model.optimize()

#     # Store optimization results
#     latest_optimization_results = {
#         "status": "optimal" if model.status == GRB.OPTIMAL else "infeasible",
#         "total_cost": model.objVal if model.status == GRB.OPTIMAL else None,
#         "supplier_to_roastery": [
#             {"from": s, "to": r, "coffee_type": t, "quantity": x[s, r, t].x}
#             for s, r, t in x.keys() if x[s, r, t].x > 0
#         ],
#         "roastery_to_cafe": [
#             {"from": r, "to": c, "coffee_type": t, "quantity": y[r, c, t].x}
#             for r, c, t in y.keys() if y[r, c, t].x > 0
#         ]
#     }

#     return latest_optimization_results
