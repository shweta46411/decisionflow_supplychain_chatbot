from gurobipy import Model, GRB
import pandas as pd

def define_optimization_model(data):
    model = Model("ShippingOptimization")
    cities = data['customer_city'].unique()
    products = data['product_type'].unique()
    shipping_modes = data['shipping_mode'].unique()

    shipment_vars = {}
    for city in cities:
        for product in products:
            for mode in shipping_modes:
                if not data.loc[
                    (data['customer_city'] == city) &
                    (data['product_type'] == product) &
                    (data['shipping_mode'] == mode)
                ].empty:
                    shipment_vars[(city, product, mode)] = model.addVar(
                        vtype=GRB.CONTINUOUS, name=f"ship_{city}_{product}_{mode}"
                    )

    model.setObjective(
        sum(
            data.loc[
                (data['customer_city'] == city) &
                (data['product_type'] == product) &
                (data['shipping_mode'] == mode), 'price'
            ].values[0] * shipment_vars[(city, product, mode)]
            for city, product, mode in shipment_vars.keys()
        ),
        GRB.MINIMIZE
    )

    for city in cities:
        for product in products:
            demand = data.loc[
                (data['customer_city'] == city) &
                (data['product_type'] == product),
                'quantity'
            ].sum()

            if pd.isna(demand) or demand == 0:
                continue

            model.addConstr(
                sum(shipment_vars.get((city, product, mode), 0) for mode in shipping_modes) == demand,
                name=f"demand_{city}_{product}"
            )

    return model, shipment_vars

def solve_optimization_problem(model, shipment_vars):
    model.optimize()
    solution = {}
    if model.status == GRB.OPTIMAL:
        for var in model.getVars():
            if var.X > 0:
                solution[var.VarName] = var.X
    return solution
