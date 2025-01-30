def interpret_question(question):
    question = question.strip().lower()
    
    cost_keywords = ["minimize shipping costs", "reduce shipping expenses", "reduce costs", "minimize costs"]
    inventory_keywords = ["allocate inventory", "meet demand", "optimize inventory"]

    for keyword in cost_keywords:
        if keyword in question:
            return {
                "objective": "minimize_cost",
                "constraints": ["meet_demand"],
                "decision_variables": ["shipment_quantity"]
            }

    for keyword in inventory_keywords:
        if keyword in question:
            return {
                "objective": "optimize_inventory",
                "constraints": ["meet_demand"],
                "decision_variables": ["inventory_allocation"]
            }

    return None
