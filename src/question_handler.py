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

# Load datasets
demands_df = pd.read_csv("data/demands.csv")
processing_df = pd.read_csv("data/processing.csv")
transportation_df = pd.read_csv("data/transportation.csv")

def process_question():
    """Handles general queries based on available dataset"""
    return "I received your question, but I need more information to answer."
