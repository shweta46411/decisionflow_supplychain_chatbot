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

import openai
import pandas as pd
from gurobipy import Model, GRB
import os
import pandas as pd
from src.openai_handler import call_gpt, safe_parse_json, chatbot_response
from src.optimization_model import run_optimization
from dotenv import load_dotenv
from src.utils import file_paths


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

def generate_system_prompt():
    demand_data = demand_df.to_csv(index=False)
    processing_data = processing_df.to_csv(index=False)
    transportation_data = transportation_df.to_csv(index=False)

    return f"""
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
router_history = []
descriptive_history = []
optimization_history = []
latest_optimization_results = None


def get_data_specification(question):
    prompt = f"""
You are a data assistant for a supply chain AI system. Your task is to decide:
→ Which CSV file to query
→ Which specific columns to extract
based on the user’s natural language question.

⚠️ IMPORTANT:
- Only choose from these three files: 'demands.csv', 'processing.csv', 'transportation.csv'
- Never mention or return any other file name
- Only include columns that exist in the file
- Your output must be a valid JSON with this format:
  {{ "file": "file_name.csv", "columns": ["col1", "col2", ...] }}

---

### ✅ FEW-SHOT EXAMPLES:

**Q:** What is the total demand?
→ {{ "file": "demands.csv", "columns": ["cafe", "coffee_type", "demand"] }}

**Q:** What is the total demand for light roast?
→ {{ "file": "demands.csv", "columns": ["cafe", "coffee_type", "demand"] }}

**Q:** Which café has the highest total demand?
→ {{ "file": "demands.csv", "columns": ["cafe", "coffee_type", "demand"] }}

**Q:** What is the demand for dark roast at café2?
→ {{ "file": "demands.csv", "columns": ["cafe", "coffee_type", "demand"] }}

**Q:** Which supplier has the highest capacity?
→ {{ "file": "processing.csv", "columns": ["entity", "entity_type", "capacity"] }}

**Q:** List all suppliers and their light roast capacity
→ {{ "file": "processing.csv", "columns": ["entity", "entity_type", "coffee_type", "capacity"] }}

**Q:** What are the costs for each supplier for dark roast?
→ {{ "file": "processing.csv", "columns": ["entity", "entity_type", "coffee_type", "cost"] }}

**Q:** Which roastery has the highest light roast capacity?
→ {{ "file": "processing.csv", "columns": ["entity", "entity_type", "coffee_type", "capacity"] }}

**Q:** What is the processing cost at roastery3 for dark roast?
→ {{ "file": "processing.csv", "columns": ["entity", "entity_type", "coffee_type", "cost"] }}

**Q:** Which transportation route has the highest capacity?
→ {{ "file": "transportation.csv", "columns": ["from", "to", "capacity"] }}

**Q:** Which transportation route has the lowest cost?
→ {{ "file": "transportation.csv", "columns": ["from", "to", "cost"] }}

**Q:** What is the transportation cost from supplier1 to roastery2 for light roast?
→ {{ "file": "transportation.csv", "columns": ["from", "to", "coffee_type", "cost"] }}

**Q:** Which transportation paths are available for dark roast?
→ {{ "file": "transportation.csv", "columns": ["from", "to", "coffee_type"] }}

**Q:** List all available transportation routes and costs
→ {{ "file": "transportation.csv", "columns": ["from", "to", "coffee_type", "cost"] }}

---

Now analyze the question:
"{question}"

Return ONLY the final JSON output with "file" and "columns".
"""

    response = openai.ChatCompletion.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {"role": "system", "content": "You are a helpful assistant that only returns valid JSON with 'file' and 'columns'."},
            {"role": "user", "content": prompt}
        ]
    )
    output = response.choices[0].message.content.strip()
    if not output.startswith("{"):
        raise ValueError("I’m here to help with supply chain data. Try asking about demand, capacity, or transportation costs!")
    return safe_parse_json(output)
    

def load_filtered_data(spec):
    valid_files = list(file_paths.keys())
    selected_file = spec.get("file")

    if selected_file not in valid_files:
        raise ValueError(
            f"❌ Invalid file requested by GPT: '{selected_file}'.\n"
            f"Allowed files: {valid_files}\n"
            f"Full spec: {spec}"
        )

    file_path = file_paths[selected_file]
    df_full = pd.read_csv(file_path)

    # Validate columns
    expected_columns = set(spec.get("columns", []))
    missing_cols = expected_columns - set(df_full.columns)

    if missing_cols:
        raise ValueError(
            f"❌ Missing columns in '{selected_file}': {missing_cols}\n"
            f"Available columns: {list(df_full.columns)}"
        )

    # Filter to only requested columns
    df = df_full[spec["columns"]]
    return df, df.to_string(index=False)


# 🔁 Global router memory
router_history = []
# Track last optimization intent
last_optimization_intent = None


def classify_question(question):
    """Uses GPT-4 to classify a question and logs the result to router_history."""

    question_lower = question.lower().strip()
    vague_phrases = ["how about", "what about", "based on that", "then", "next", "and", "also"]
    optimization_phrases = [
        "from roasteries to cafes",
        "from suppliers to roasteries",
        "how much is transported",
        "how much was shipped",
        "delivered",
        "distributed",
        "transportation quantity",
        "flow"
    ]

    is_follow_up = any(p in question_lower for p in vague_phrases)
    mentions_optimization_signal = any(p in question_lower for p in optimization_phrases)
    previous_type = router_history[-1]["type"] if router_history else None
    previous_question = router_history[-1]["question"].lower() if router_history else ""


    classification_prompt = f"""
    You are a highly intelligent supply chain chatbot. Your job is to correctly classify user questions into **one of three categories**:

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

    if classification not in ["descriptive", "optimization", "what-if"]:
        raise ValueError(f"❌ Unexpected classification: '{classification}'")

    if is_follow_up and previous_type:
    # 🧠 Special case: continuation of transportation flow questions
      if (
          "suppliers to roasteries" in previous_question
          and "roasteries to cafes" in question_lower
      ):
          print(f"[DEBUG] Follow-up to supplier→roastery flow → interpreting as optimization (roastery→cafe)")
          router_history.append({"question": question, "type": "optimization"})
          return "optimization"

      # 🧠 Special case: follow-up to demand-fulfillment question
      if "demand met" in previous_question and "cafe" in question_lower:
          print(f"[DEBUG] Follow-up to a demand fulfillment question → keep optimization type")
          router_history.append({"question": question, "type": "optimization"})
          return "optimization"

      # Case A: vague follow-up with no strong new signal
      if not mentions_optimization_signal:
          if classification != previous_type:
              print(f"[DEBUG] Vague follow-up → GPT classification differs → using GPT type: {classification}")
              router_history.append({"question": question, "type": classification})
              return classification
          else:
              print(f"[DEBUG] Vague follow-up with no new signal → inheriting previous type: {previous_type}")
              router_history.append({"question": question, "type": previous_type})
              return previous_type

      # Case B: vague follow-up but optimization signals present → enforce optimization
      if mentions_optimization_signal and previous_type == "optimization":
          print(f"[DEBUG] Optimization signals in follow-up → keeping optimization")
          router_history.append({"question": question, "type": "optimization"})
          return "optimization"

      # Case C: trust GPT if clearly contradicts
      if classification != previous_type:
          print(f"[DEBUG] Vague follow-up, GPT classification differs → using GPT type: {classification}")
          router_history.append({"question": question, "type": classification})
          return classification


    # ✅ Normal case
    print(f"[DEBUG] Classified '{question}' as → {classification}")
    router_history.append({"question": question, "type": classification})
    return classification

# **Descriptive Question Handling**
# 🔁 Global descriptive memory
descriptive_history = []
optimization_history = []

# **Descriptive Question Handling**
def handle_descriptive(question):
    global descriptive_history

    # Step 1: Add user question to memory
    descriptive_history.append({"role": "user", "content": question})

    # Step 2: Get file and columns to load
    spec = get_data_specification(question)

    # Step 3: Load relevant columns from the appropriate dataset
    df, data_str = load_filtered_data(spec)

    # Step 4: Prepare GPT messages with memory + filtered data
    memory_window = descriptive_history[-10:]  # Up to 5 turns of memory

    messages = [
        {"role": "system", "content": f"""You are a helpful supply chain assistant.

Use the following filtered dataset to answer the user's question. Do not make assumptions. Stick only to the data provided.

### Filtered Data:
{data_str}
"""}
    ] + memory_window

    # Step 5: Ask GPT-4
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0
    )

    # Step 6: Append GPT response to memory
    answer = response.choices[0]["message"]["content"].strip()
    descriptive_history.append({"role": "assistant", "content": answer})

    return answer




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
import pandas as pd
from src.utils import file_paths

demand_df = pd.read_csv(file_paths["demands.csv"])
processing_df = pd.read_csv(file_paths["processing.csv"])
def handle_optimization(question):
    """Retrieves the latest optimization results and answers the user's question."""

    global latest_optimization_results

    # **Ensure that an optimization has been run at least once**
    if latest_optimization_results is None:
        print("\n⚠️ No prior optimization found. Running optimization now...")
        latest_optimization_results = run_optimization()  # Run optimization if never executed

    # Convert the question to lowercase for easier handling
    question_lower = question.lower().strip()

    # **1️⃣ Handling Total Cost Inquiry**
    if "total cost" in question_lower or "cost after optimization" in question_lower:
        total_cost = latest_optimization_results["total_cost"]
        return f"💰 **The total optimized cost of the supply chain is:** **${total_cost:,.2f}**."

    # ✅ Roastery → Café Shipments (Supports follow-up questions)
    if any(p in question_lower for p in [
        "roasteries to cafes",
        "coffee to cafes",
        "cafe shipments",
        "delivered to cafes",
        "cafe delivery",
        "how much coffee is transported from roasteries to cafes"
    ]):
        roastery_cafe_shipments = latest_optimization_results.get("roastery_to_cafe", [])

        if not roastery_cafe_shipments:
            return "✅ No coffee was transported from roasteries to cafés in the optimal solution."

        # Group shipments for cleaner output
        shipment_log = {}
        for shipment in roastery_cafe_shipments:
            key = (shipment["from"], shipment["to"])
            if key not in shipment_log:
                shipment_log[key] = {}
            shipment_log[key][shipment["coffee_type"]] = shipment["quantity"]

        summary_lines = []
        for (roastery, cafe), types in shipment_log.items():
            light = types.get("light_roast", 0)
            dark = types.get("dark_roast", 0)
            summary_lines.append(
                f"✅ {roastery} → {cafe}: {light:.0f} units of light roast, {dark:.0f} units of dark roast"
            )

        total_quantity = sum(s["quantity"] for s in roastery_cafe_shipments)

        return f"""📦 **Optimized Roastery → Café Shipments:**
    {chr(10).join(summary_lines)}

    📊 **Total Verified Quantity Transported:** {total_quantity:.0f} units
    """
    # ✅ Supplier → Roastery Shipments (Supports follow-up questions)
    # ✅ Supplier → Roastery Shipments (Supports follow-up questions)
    if any(p in question_lower for p in [
        "suppliers to roasteries",
        "supplier shipments",
        "coffee from suppliers",
        "how much coffee is transported from suppliers to roasteries"
    ]):
        supplier_roastery_shipments = latest_optimization_results.get("supplier_to_roastery", [])

        if not supplier_roastery_shipments:
            return "✅ No coffee was transported from suppliers to roasteries in the optimal solution."

        # Group shipments for cleaner output
        shipment_log = {}
        for shipment in supplier_roastery_shipments:
            key = (shipment["from"], shipment["to"])
            if key not in shipment_log:
                shipment_log[key] = {}
            shipment_log[key][shipment["coffee_type"]] = shipment["quantity"]

        summary_lines = []
        for (supplier, roastery), types in shipment_log.items():
            light = types.get("light_roast", 0)
            dark = types.get("dark_roast", 0)
            summary_lines.append(
                f"✅ {supplier} → {roastery}: {light:.0f} units of light roast, {dark:.0f} units of dark roast"
            )

        total_quantity = sum(s["quantity"] for s in supplier_roastery_shipments)

        return f"""📦 **Optimized Supplier → Roastery Shipments:**
    {chr(10).join(summary_lines)}

    📊 **Total Verified Quantity Transported:** {total_quantity:.0f} units
    """

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

    # ✅ Demand fulfillment check for a specific café
    if "demand met" in question_lower or ("cafe" in question_lower and "how about" in question_lower):
        target_cafe = None
        for cafe_name in demand_df["cafe"].unique():
            if cafe_name.lower() in question_lower:
                target_cafe = cafe_name
                break

        if not target_cafe:
            return "❌ Could not determine which café you're asking about."

        # Extract actual demand
        actual_demand = demand_df[demand_df["cafe"] == target_cafe].set_index("coffee_type")["demand"].to_dict()

        # Extract optimized shipments
        shipments = [s for s in latest_optimization_results["roastery_to_cafe"] if s["to"] == target_cafe]
        received = {"light_roast": 0, "dark_roast": 0}
        for s in shipments:
            received[s["coffee_type"]] += s["quantity"]

        summary = []
        for t in ["light_roast", "dark_roast"]:
            summary.append(
                f"- {t.replace('_', ' ').title()}: Received {received[t]:.1f}, Demand {actual_demand.get(t, 0)}"
            )

        # Check fulfillment
        all_met = all(abs(received[t] - actual_demand.get(t, 0)) < 1e-3 for t in actual_demand)
        fulfillment_text = "✅ All demand was met." if all_met else "⚠️ Demand was not fully met."

        return f"""📦 **Demand Fulfillment for {target_cafe}:**
    {chr(10).join(summary)}

    {fulfillment_text}
    """

    # **6️⃣ If the Question is Complex, Delegate to GPT-4 for Further Analysis**
    else:
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
              {"role": "system", "content": generate_system_prompt()},
              {"role": "user", "content": query_prompt}
          ]
      )

      return response["choices"][0]["message"]["content"]

# Track last optimization question
last_optimization_question = None

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
