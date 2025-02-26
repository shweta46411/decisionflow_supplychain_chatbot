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

def run_optimization():
    """Optimization model using Gurobi"""
    model = gp.Model("Supply_Chain_Optimization")

    # Define decision variables
    x = {}
    for _, row in transportation_df.iterrows():
        s, r, t = row["from"], row["to"], row["coffee_type"]
        x[s, r, t] = model.addVar(lb=0, ub=row["capacity"], vtype=GRB.CONTINUOUS, name=f"x_{s}_{r}_{t}")

    # Define objective function (minimizing cost)
    model.setObjective(
        gp.quicksum(transportation_df.loc[
            (transportation_df["from"] == s) & (transportation_df["to"] == r) & (transportation_df["coffee_type"] == t), "cost"].iloc[0] * x[s, r, t]
            for s, r, t in x.keys()),
        GRB.MINIMIZE
    )

    # Optimize model
    model.optimize()

    if model.status == GRB.OPTIMAL:
        return f"Optimization completed. Total cost: ${model.objVal:.2f}"
    else:
        return "Optimization could not find an optimal solution."

