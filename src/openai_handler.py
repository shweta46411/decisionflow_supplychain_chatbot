import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# def get_llm_summary(question, data):
#     """Uses OpenAI API to generate insights based strictly on the provided data."""
#     try:
#         # Format data into a readable structure for LLM
#         formatted_data = data.to_dict(orient='records')

#         # Construct prompt
#         prompt = (
#             f"Answer the following question based only on the provided dataset.\n"
#             f"**Question:** {question}\n"
#             f"**Dataset:** {formatted_data}\n"
#             f"Provide a clear, data-backed answer without assumptions. "
#             f"If the dataset lacks enough information, say: 'The data does not provide a definitive answer'."
#         )

#         # OpenAI request
#         response = openai.ChatCompletion.create(
#             model="gpt-4-turbo",
#             temperature=0,
#             messages=[
#                 {"role": "system", "content": "You are a data assistant providing structured insights."},
#                 {"role": "user", "content": prompt}
#             ]
#         )
        
#         return response['choices'][0]['message']['content']

#     except Exception as e:
#         return f"⚠️ Error in generating LLM response: {e}"
import openai
import pandas as pd

# Load datasets
demands_df = pd.read_csv("data/demands.csv")
processing_df = pd.read_csv("data/processing.csv")
transportation_df = pd.read_csv("data/transportation.csv")

# Convert dataset content to string for GPT-4
demand_data = demands_df.to_string(index=False)
processing_data = processing_df.to_string(index=False)
transportation_data = transportation_df.to_string(index=False)

# Define system prompt enforcing dataset-based answers
system_prompt = f"""
You are a highly accurate supply chain chatbot. Your answers must come from these datasets:

1. **Demands Dataset**: Required amount of light/dark roasted coffee for each café.
2. **Processing Dataset**: Supplier & roastery details, capacities, and cost structures.
3. **Transportation Dataset**: Routes, costs, and capacity limits.

🔹 **Rules for Answering Questions:**
- **Strictly use dataset values.** Never make up data.
- **List and compare all relevant values** before answering.
- **Sort and identify correct values.**
- **If uncertain, respond: "I could not determine the correct answer from the dataset."**

🔹 **Dataset Content:**
#### **Demands Dataset:**
{demand_data}

#### **Processing Dataset:**
{processing_data}

#### **Transportation Dataset:**
{transportation_data}
"""

def chatbot_response(query):
    """Handles all queries using GPT-4 while enforcing dataset-based answers."""
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": query}
        ]
    )
    return response["choices"][0]["message"]["content"]

