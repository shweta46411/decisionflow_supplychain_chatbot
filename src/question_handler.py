# import pandas as pd
# import os
# import streamlit as st
# from src.optimization_model import run_optimization  # Fetch optimized results
# from src.openai_handler import get_llm_summary  # LLM for structured insights

# # File Paths
# DATA_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data")
# DATASETS = {
#     "transportation": os.path.join(DATA_DIR, "transportation.csv"),
#     "demands": os.path.join(DATA_DIR, "demands.csv"),
#     "processing": os.path.join(DATA_DIR, "processing.csv")
# }

# # Load datasets
# dataframes = {name: pd.read_csv(path) for name, path in DATASETS.items() if os.path.exists(path)}

# # Run optimization on startup & cache results
# @st.cache_data
# def get_optimization_results():
#     return run_optimization()

# optimized_results = get_optimization_results()

# def classify_question(question):
#     optimization_keywords = ["optimal", "best", "minimum cost", "least cost", "efficient", "optimized", "allocation"]
#     descriptive_keywords = ["what", "how much", "which", "how many", "list", "most", "frequently", "ordered"]

#     question = question.lower()
    
#     if any(keyword in question for keyword in optimization_keywords):
#         return "optimization"
#     elif any(keyword in question for keyword in descriptive_keywords):
#         return "descriptive"
#     else:
#         return "unknown"

# def handle_optimization_question(question):
#     """Fetches the relevant answer from Gurobi results and enhances it with LLM."""
#     if optimized_results.empty:
#         return "⚠️ The optimization model has not produced any results yet."

#     optimized_results.columns = optimized_results.columns.str.lower()
#     relevant_data = optimized_results[optimized_results.apply(
#         lambda row: any(keyword in str(row).lower() for keyword in question.lower().split()), axis=1)]

#     if relevant_data.empty:
#         return "🔍 No specific optimized data found matching your query."

#     # Get LLM response based on the optimized results
#     llm_response = get_llm_summary(question, relevant_data)

#     # Display data and AI summary in Streamlit
#     st.subheader("📊 Optimized Results Matching Your Query:")
#     st.dataframe(relevant_data)

#     return f"**💡 LLM Insight:**\n{llm_response}"

# def handle_descriptive_question(question):
#     """Fetches the relevant data from CSV files and enhances it with LLM."""
#     results = []
    
#     for name, df in dataframes.items():
#         df.columns = df.columns.str.lower()
#         relevant_data = df[df.apply(
#             lambda row: any(keyword in str(row).lower() for keyword in question.lower().split()), axis=1)]

#         if not relevant_data.empty:
#             results.append((name, relevant_data.head(5)))  # Take the top 5 matches

#     if not results:
#         return "🔍 No relevant data found in the available files."

#     response_text = "📊 **Relevant Data Found in:**\n"
#     for dataset_name, df in results:
#         response_text += f"- **{dataset_name.capitalize()} Dataset** ({len(df)} records)\n"
#         st.subheader(f"📂 Data from `{dataset_name}`")
#         st.dataframe(df)  # Display in Streamlit

#         # Get LLM response for the found dataset
#         llm_response = get_llm_summary(question, df)
#         response_text += f"\n**💡 LLM Insight:** {llm_response}\n"

#     return response_text

# def handle_question(user_input):
#     """Routes user queries to either descriptive (Excel data) or optimization (Gurobi output)."""
#     question_type = classify_question(user_input)

#     if question_type == "descriptive":
#         return handle_descriptive_question(user_input)
#     elif question_type == "optimization":
#         return handle_optimization_question(user_input)
#     else:
#         return "❌ I can only answer based on logistics data available in the provided datasets."
import pandas as pd
import openai
#from src.optimization_model import run_optimization  # Fetch optimized results
import pandas as pd
from gurobipy import Model, GRB
import os
# Load datasets
# def process_question():
#     """Handles general queries based on available dataset"""
#     return "I received your question, but I need more information to answer."

# demands_df = pd.read_csv("data/demands.csv")
# processing_df = pd.read_csv("data/processing.csv")
# transportation_df = pd.read_csv("data/transportation.csv")


# Load datasets
demand_df = pd.read_csv("data/demands.csv")
processing_df = pd.read_csv("data/processing.csv")
transportation_df = pd.read_csv("data/transportation.csv")

# Preview datasets
def preview_datasets():
    print("Demand Dataset:")
    print(demand_df.head())
    print("\nProcessing Dataset:")
    print(processing_df.head())
    print("\nTransportation Dataset:")
    print(transportation_df.head())

preview_datasets()

# Convert dataset content to structured CSV for GPT-4
demand_data = demand_df.to_csv(index=False)
processing_data = processing_df.to_csv(index=False)
transportation_data = transportation_df.to_csv(index=False)

system_prompt = f"""
You are a highly accurate supply chain chatbot that strictly answers only descriptive and optimization questions related to three datasets:

1. **Demands Dataset**: Contains the required amount of light and dark roasted coffee for each café.
2. **Processing Dataset**: Includes details about suppliers and roasteries, their capacities for light and dark roasted coffee, and their cost structures.
3. **Transportation Dataset**: Lists available transportation routes, costs, and capacity limits for moving coffee between suppliers, roasteries, and cafés.

### **Rules for Answering Questions**
- **Classify all questions as either:**
  - **Descriptive** (retrieving, filtering, or comparing dataset values)
  - **Optimization** (solving and interpreting Gurobi optimization results)
- **For descriptive questions:**
  - **Only use raw dataset values.** Never generate estimates or assumptions.
  - **List, compare, and sort relevant values** before returning an answer.
  - **Verify your final answer matches dataset values exactly.**
  - **If calculations are required, perform them step-by-step using real dataset values.**
  - **If uncertain, return:** "I could not determine the correct answer from the dataset."
- **For optimization questions:**
  - **Use only the structured optimization output from Gurobi.** Never assume values.
  - **Summarize the results clearly**, including total system cost and optimal transportation decisions.
  - **Filter the results based on the user’s specific question.**
  - **If the model did not find a solution, state:** "No optimal solution found."

### **Dataset Content:**
#### **Demands Dataset:**
```
{demand_data}
```
#### **Processing Dataset:**
```
{processing_data}
```
#### **Transportation Dataset:**
```
{transportation_data}
```
"""


def classify_question(question):
    """Uses GPT-4 to classify a question as either 'descriptive' (dataset-based) or 'optimization' (Gurobi result-based)."""

    classification_prompt = f"""
    You are a highly intelligent supply chain chatbot. Your job is to correctly classify user questions into **one of two categories**:

    ### **1️⃣ Descriptive Questions**
    These questions **only require retrieving information from the raw dataset.**
    They **do not** require running any optimization model. They typically involve:
    - Listing values (e.g., demand, supply, capacity, transportation cost).
    - Identifying specific data points.
    - Comparing values directly from the dataset.

    **✅ Examples of Descriptive Questions:**
    - "What is the total demand for light roast coffee?"
    - "Which supplier has the highest capacity?"
    - "List all available transportation routes and costs."
    - "What is the processing cost at roastery3?"
    - "Which café orders the most dark roast coffee?"
    - "Show me the cheapest transportation route from suppliers to roasteries."

    **🚫 These questions should NOT be classified as 'optimization'.**

    ### **2️⃣ Optimization Questions**
    These questions **require running the Gurobi optimization model**
    to determine **optimal** supply chain decisions. They involve:
    - Computing optimized transportation flows.
    - Minimizing costs or maximizing efficiency.
    - Checking constraint satisfaction (e.g., full capacity usage).
    - Answering "what-if" scenario-based questions.

    **✅ Examples of Optimization Questions:**
    - "How much coffee is transported from suppliers to roasteries?"
    - "Which supplier is operating at full capacity?"
    - "What is the optimal total cost of the supply chain?"
    - "How much coffee should each supplier send to roasteries?"
    - "What is the best way to distribute coffee to minimize costs?"
    - "How should coffee be transported to meet café demand at the lowest cost?"
    - "Find the optimal distribution plan for dark roast coffee."
    - "What happens if supplier1 shuts down?"

    **🚫 These questions should NOT be classified as 'descriptive'.**

    **What-If Scenario Questions** → These require **modifying the optimization model with user-defined changes and rerunning Gurobi**.
       - Example: "What happens if Supplier1’s capacity is increased by 200 units?"
       - Example: "If transportation costs increase by 10%, what is the new optimal cost?"


    **🔹 Instructions for Classification:**
    - **Classify the following question as either 'descriptive' or 'optimization' or 'what-if'.**
    - **Respond with ONLY one word:** "descriptive" or "optimization" or "what-if".
    - **Do NOT provide any explanations or extra text.**

    **User Question:** "{question}"
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[{"role": "user", "content": classification_prompt}]
    )

    classification = response["choices"][0]["message"]["content"].strip().lower()

    # Ensure GPT-4 returns only "descriptive" or "optimization"
    if classification not in ["descriptive", "optimization","what-if"]:
        return "descriptive"  # Default to descriptive if GPT-4 gives an unexpected response

    return classification

# **Descriptive Question Handling**
def handle_descriptive(question):
    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": question}
        ]
    )
    return response["choices"][0]["message"]["content"]
def run_optimization(modified_data=None):

    global demand_df, processing_df, transportation_df, latest_optimization_results

    # **Ensure that the modified dataset persists across runs**
    if modified_data:
        if "demand" in modified_data:
            demand_df = modified_data["demand"]
        if "processing" in modified_data:
            processing_df = modified_data["processing"]
        if "transportation" in modified_data:
            transportation_df = modified_data["transportation"]

    # **Use the latest modified dataset if available**
    demand_df_used = demand_df
    processing_df_used = processing_df
    transportation_df_used = transportation_df

    model = Model("Supply_Chain_Optimization")
    # **Suppress solver output**
    model.setParam("OutputFlag", 0)

    # Variables for transportation from supplier to roastery
    x = {}
    for _, row in transportation_df.iterrows():
        s, r, t = row["from"], row["to"], row["coffee_type"]
        x[s, r, t] = model.addVar(lb=0, ub=row["capacity"], vtype=GRB.CONTINUOUS, name=f"x_{s}_{r}_{t}")

    # Variables for transportation from roasteries to cafes
    y = {}
    for _, row in demand_df.iterrows():
        c, t = row["cafe"], row["coffee_type"]
        for r in processing_df[processing_df["entity_type"] == "roastery"]["entity"].unique():
            y[r, c, t] = model.addVar(lb=0, vtype=GRB.CONTINUOUS, name=f"y_{r}_{c}_{t}")

    # Objective Function (User's Exact Version)
    model.setObjective(
        sum(transportation_df.loc[(transportation_df["from"] == s) &
                                  (transportation_df["to"] == r) &
                                  (transportation_df["coffee_type"] == t), "cost"].iloc[0] * x[s, r, t]
            for s, r, t in x.keys()) +
        sum(transportation_df.loc[(transportation_df["from"] == r) &
                                  (transportation_df["to"] == c) &
                                  (transportation_df["coffee_type"] == t), "cost"].iloc[0] * y[r, c, t]
            for r, c, t in y.keys()) +
        sum(processing_df.loc[(processing_df["entity"] == s) &
                              (processing_df["coffee_type"] == t), "cost"].iloc[0] * x[s, r, t]
            for s, r, t in x.keys()) +
        sum(processing_df.loc[(processing_df["entity"] == r) &
                              (processing_df["coffee_type"] == t), "cost"].iloc[0] * y[r, c, t]
            for r, c, t in y.keys()),
        GRB.MINIMIZE
    )

    # Constraints
    # Supplier Capacity Constraint
    for _, row in processing_df[processing_df["entity_type"] == "supplier"].iterrows():
        s, t = row["entity"], row["coffee_type"]
        model.addConstr(
            sum(x[s, r, t] for r in transportation_df[transportation_df["from"] == s]["to"].unique() if (s, r, t) in x)
            <= processing_df.loc[(processing_df["entity"] == s) & (processing_df["coffee_type"] == t), "capacity"].iloc[0],
            name=f"SupplierCapacity_{s}_{t}"
        )

    # Roastery Processing Capacity Constraint
    for _, row in processing_df[processing_df["entity_type"] == "roastery"].iterrows():
        r, t = row["entity"], row["coffee_type"]
        model.addConstr(
            sum(x[s, r, t] for s in transportation_df[transportation_df["to"] == r]["from"].unique() if (s, r, t) in x)
            <= processing_df.loc[(processing_df["entity"] == r) & (processing_df["coffee_type"] == t), "capacity"].iloc[0],
            name=f"RoasteryCapacity_{r}_{t}"
        )

    # Flow Conservation Constraint
    for r in processing_df[processing_df["entity_type"] == "roastery"]["entity"].unique():
        for t in ["light_roast", "dark_roast"]:
            model.addConstr(
                sum(x[s, r, t] for s in transportation_df[transportation_df["to"] == r]["from"].unique() if (s, r, t) in x)
                == sum(y[r, c, t] for c in demand_df["cafe"].unique() if (r, c, t) in y),
                name=f"FlowConservation_{r}_{t}"
            )

    # Transportation Capacity Constraint
    for _, row in transportation_df.iterrows():
        r, c, t, max_capacity = row["from"], row["to"], row["coffee_type"], row["capacity"]
        if (r, c, t) in y:
            model.addConstr(
                y[r, c, t] <= max_capacity,
                name=f"RoasteryToCafeCapacity_{r}_{c}_{t}"
            )

    # Demand Fulfillment Constraint
    for _, row in demand_df.iterrows():
        c, t, d = row["cafe"], row["coffee_type"], row["demand"]
        model.addConstr(
            sum(y[r, c, t] for r in transportation_df[transportation_df["to"] == c]["from"].unique() if (r, c, t) in y)
            == d,
            name=f"DemandFulfillment_{c}_{t}"
        )

    # Solve model
    model.optimize()

    # **Store updated optimization results globally**
    latest_optimization_results = {
        "status": "optimal" if model.status == GRB.OPTIMAL else "infeasible",
        "total_cost": model.objVal if model.status == GRB.OPTIMAL else None,
        "supplier_to_roastery": [
            {"from": s, "to": r, "coffee_type": t, "quantity": x[s, r, t].x}
            for s, r, t in x.keys() if x[s, r, t].x > 0
        ],
        "roastery_to_cafe": [
            {"from": r, "to": c, "coffee_type": t, "quantity": y[r, c, t].x}
            for r, c, t in y.keys() if y[r, c, t].x > 0
        ]
    }

    return latest_optimization_results
def handle_what_if(question):
    """Parses the what-if question, modifies the dataset, and runs a new Gurobi optimization."""

    # Use GPT-4 to extract what-if changes from the question
    modification_prompt = f"""
    You are an expert supply chain assistant. Extract the required dataset modifications from the following what-if question.

    **User Question:** "{question}"

    **Instructions:**
    - Identify whether the question modifies supplier capacity, demand, or transportation cost.
    - Return the modifications in structured JSON format.
    - Example response:
      {{"processing": [{{"entity": "supplier1", "coffee_type": "light_roast", "new_capacity": 1300}}]}}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[{"role": "user", "content": modification_prompt}]
    )

    # Extract structured modifications from response
    modifications = eval(response["choices"][0]["message"]["content"])  # Convert string to dict

    # Apply modifications
    modified_data = {}
    if "processing" in modifications:
        modified_processing = processing_df.copy()
        for mod in modifications["processing"]:
            modified_processing.loc[
                (modified_processing["entity"] == mod["entity"]) &
                (modified_processing["coffee_type"] == mod["coffee_type"]),
                "capacity"
            ] = mod["new_capacity"]
        modified_data["processing"] = modified_processing

    if "demand" in modifications:
        modified_demand = demand_df.copy()
        for mod in modifications["demand"]:
            modified_demand.loc[
                (modified_demand["cafe"] == mod["cafe"]) &
                (modified_demand["coffee_type"] == mod["coffee_type"]),
                "demand"
            ] = mod["new_demand"]
        modified_data["demand"] = modified_demand

    if "transportation" in modifications:
        modified_transportation = transportation_df.copy()
        for mod in modifications["transportation"]:
            modified_transportation.loc[
                (modified_transportation["from"] == mod["from"]) &
                (modified_transportation["to"] == mod["to"]) &
                (modified_transportation["coffee_type"] == mod["coffee_type"]),
                "cost"
            ] = mod["new_cost"]
        modified_data["transportation"] = modified_transportation

    # Run modified optimization model
    return run_optimization(modified_data)

def handle_optimization(question):
    """Handles optimization-related questions by extracting real results from the Gurobi model."""

    global latest_optimization_results

    # **Ensure that an optimization has been run at least once**
    if latest_optimization_results is None:
        return "⚠️ No optimization results available. Run an optimization first."

    question_lower = question.lower().strip()

    # **2️⃣ Handling Supplier → Roastery Shipments**
    if "how much coffee is transported from suppliers to roasteries" in question_lower:
        supplier_roastery_shipments = latest_optimization_results["supplier_to_roastery"]

        if not supplier_roastery_shipments:
            return "✅ No coffee was transported from suppliers to roasteries in the optimal solution."

        transport_data = "\n".join(
            f"✅ {shipment['from']} → {shipment['to']} ({shipment['coffee_type']}): {shipment['quantity']} units"
            for shipment in supplier_roastery_shipments
        )

        return f"📦 **Optimized Supplier → Roastery Shipments:**\n{transport_data}"

    # **3️⃣ Handling Roastery → Café Shipments**
    if "how much coffee is transported from roasteries to cafés" in question_lower:
        roastery_cafe_shipments = latest_optimization_results["roastery_to_cafe"]

        if not roastery_cafe_shipments:
            return "✅ No coffee was transported from roasteries to cafés in the optimal solution."

        transport_data = "\n".join(
            f"✅ {shipment['from']} → {shipment['to']} ({shipment['coffee_type']}): {shipment['quantity']} units"
            for shipment in roastery_cafe_shipments
        )

        return f"📦 **Optimized Roastery → Café Shipments:**\n{transport_data}"

    # **4️⃣ Handling Total Cost Inquiry**
    if "total cost" in question_lower or "cost after optimization" in question_lower:
        total_cost = latest_optimization_results["total_cost"]
        return f"💰 **The total optimized cost of the supply chain is:** **${total_cost:,.2f}**."

     ###Handling Supplier Unused Capacity Inquiry**
    if "which supplier has unused capacity" in question_lower or "supplier unused capacity" in question_lower:
        # **Extract supplier capacities for each coffee type**
        supplier_capacities = {}
        for _, row in processing_df[processing_df["entity_type"] == "supplier"].iterrows():
            supplier = row["entity"]
            coffee_type = row["coffee_type"]
            capacity = row["capacity"]

            if supplier not in supplier_capacities:
                supplier_capacities[supplier] = {}

            supplier_capacities[supplier][coffee_type] = capacity

        # **Initialize supplier shipment totals per coffee type**
        supplier_shipments = {supplier: {"light_roast": 0, "dark_roast": 0} for supplier in supplier_capacities}

        # **Check if supplier_to_roastery exists in results**
        if "supplier_to_roastery" in latest_optimization_results and latest_optimization_results["supplier_to_roastery"]:
            for shipment in latest_optimization_results["supplier_to_roastery"]:
                supplier_shipments[shipment["from"]][shipment["coffee_type"]] += shipment["quantity"]

        # **Compute unused capacity per supplier per coffee type**
        unused_capacity = {
            supplier: {
                coffee_type: max(0, supplier_capacities[supplier][coffee_type] - supplier_shipments[supplier][coffee_type])
                for coffee_type in supplier_capacities[supplier]
            }
            for supplier in supplier_capacities
        }

        # **Ensure that all suppliers (used or unused) are listed correctly**
        unused_capacity_text = "\n".join(
            f"✅ {supplier} ({coffee_type}): {unused} units unused (Total Capacity: {supplier_capacities[supplier][coffee_type]}, Used: {supplier_shipments[supplier][coffee_type]})"
            for supplier in unused_capacity
            for coffee_type, unused in unused_capacity[supplier].items()
        )

        return f"📊 **Supplier Unused Capacities:**\n{unused_capacity_text}"


    # **8️⃣ If the Question is Complex, Delegate to GPT-4 for Further Analysis**
    query_prompt = f"""
    You are a supply chain optimization expert. Based on the provided optimization results, extract and summarize only the most relevant information needed to answer the user's specific question.

    ### **User's Question:**
    "{question}"

    ### **Optimization Results:**
    - **Total System Cost**: ${latest_optimization_results["total_cost"]:,.2f}
    - **Supplier → Roastery Shipments**:
      {latest_optimization_results["supplier_to_roastery"]}
    - **Roastery → Café Shipments**:
      {latest_optimization_results["roastery_to_cafe"]}
    - **Unmet Demand**: {latest_optimization_results.get("unmet_demand", "None")}
    - **Suppliers at Full Capacity**: {latest_optimization_results.get("full_capacity_suppliers", "None")}

    #### **Answering Guidelines:**
    - **If the question asks about total cost**, return only the total system cost.
    - **If the question asks about supplier shipments**, list only supplier → roastery values.
    - **If the question asks about café fulfillment**, list only roastery → café values.
    - **If the question asks whether demand was met**, confirm if all cafés received the required quantity.
    - **If constraints or feasibility issues exist**, highlight any unmet demand or over-capacity issues.
    - **If the model did not find a solution, state:** "No optimal solution found."
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query_prompt}
        ]
    )

    return response["choices"][0]["message"]["content"]
def extract_modifications_from_question(question):
    """Uses GPT-4 to extract structured dataset modifications from a what-if question."""

    modification_prompt = f"""
    You are an AI assistant that interprets what-if questions related to supply chain optimization.
    Your task is to extract dataset modifications from the user's question and return them in structured JSON format.

    **User Question:** "{question}"

    **Instructions:**
    - Identify whether the question modifies **supplier capacity, demand, or transportation cost**.
    - Return only the modifications in a structured JSON format with the exact field names used in the datasets.
    - Example responses:
      {{"demand": [{{"cafe": "cafe3", "coffee_type": "light_roast", "change": 10}}]}}
      {{"processing": [{{"entity": "supplier1", "coffee_type": "dark_roast", "change": 200}}]}}
      {{"transportation": [{{"from": "supplier1", "to": "roastery1", "coffee_type": "light_roast", "change_percentage": 5}}]}}
    """

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[{"role": "user", "content": modification_prompt}]
    )

    modifications = eval(response["choices"][0]["message"]["content"])  # Convert string to dict
    return modifications

def apply_modifications(modifications):
    """Applies dataset modifications based on extracted what-if parameters."""

    modified_data = {}

    # **Update Demand Dataset**
    if "demand" in modifications:
        modified_demand = demand_df.copy()
        for mod in modifications["demand"]:
            modified_demand.loc[
                (modified_demand["cafe"] == mod["cafe"]) &
                (modified_demand["coffee_type"] == mod["coffee_type"]),
                "demand"
            ] += mod["change"]  # Increase or decrease demand
        modified_data["demand"] = modified_demand

    # **Update Supplier/Roastery Capacities (Processing Dataset)**
    if "processing" in modifications:
        modified_processing = processing_df.copy()
        for mod in modifications["processing"]:
            modified_processing.loc[
                (modified_processing["entity"] == mod["entity"]) &
                (modified_processing["coffee_type"] == mod["coffee_type"]),
                "capacity"
            ] += mod["change"]  # Increase or decrease capacity
        modified_data["processing"] = modified_processing

    # **Update Transportation Costs**
    if "transportation" in modifications:
        modified_transportation = transportation_df.copy()
        for mod in modifications["transportation"]:
            modified_transportation.loc[
                (modified_transportation["from"] == mod["from"]) &
                (modified_transportation["to"] == mod["to"]) &
                (modified_transportation["coffee_type"] == mod["coffee_type"]),
                "cost"
            ] *= (1 + mod["change_percentage"] / 100)  # Adjust cost by percentage
        modified_data["transportation"] = modified_transportation

    return modified_data
def run_what_if_scenario(question):
    """Handles a what-if scenario by modifying the dataset and rerunning optimization."""

    global demand_df, processing_df, transportation_df

    # **Extract modification details using GPT-4**
    modifications = extract_modifications_from_question(question)

    # **Apply modifications to the dataset**
    modified_data = apply_modifications(modifications)

    # **Persist modifications globally**
    if "demand" in modified_data:
        demand_df = modified_data["demand"]
    if "processing" in modified_data:
        processing_df = modified_data["processing"]
    if "transportation" in modified_data:
        transportation_df = modified_data["transportation"]

    # **Run optimization with the modified dataset**
    global latest_optimization_results
    latest_optimization_results = run_optimization(modified_data)

    return "✅ What-If Scenario Completed! Optimization has been re-run with your modifications."
