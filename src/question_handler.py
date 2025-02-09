import pandas as pd
import openai
import os
import streamlit as st
# Load Dataset
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "DatasetA.xlsx")  

# Ensure dataset is loaded
df = None
if os.path.exists(DATA_PATH):
    df = pd.read_excel(DATA_PATH)
else:
    print("❌ Dataset not found!")

# OpenAI API Key (Make sure to set this as an environment variable)


# ✅ Check if running in a local environment
if os.path.exists(".env"):
    from dotenv import load_dotenv
    load_dotenv()  # Only loads in local development

# ✅ Fetch API key from either .env (local) or Streamlit Secrets (production)
openai.api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")

# ✅ Raise an error if the API key is missing
if not openai.api_key:
    raise ValueError("⚠️ OpenAI API Key is missing! Set it in Streamlit Secrets (Production) or .env (Local).")


# ✅ Correct way to initialize the OpenAI client
import openai

# ✅ Correct OpenAI client initialization
# client = openai.OpenAI()

# def get_openai_response(prompt, model="gpt-4-turbo"):
#     response = client.chat.completions.create(  # ✅ Correct API call
#         model=model,
#         messages=[{"role": "user", "content": prompt}]
#     )
#     return response.choices[0].message.content  # ✅ Correct response retrieval





def get_openai_response(prompt, model="gpt-4-turbo"):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]


def classify_question(question):
    """Classifies if the question is descriptive based on keywords."""
    descriptive_keywords = ["what", "how much", "which", "how many", "list", "most", "frequently", "ordered"]
    question = question.lower()
    return "descriptive" if any(keyword in question for keyword in descriptive_keywords) else "unknown"

def handle_question(user_input):
    """Handles user queries by checking dataset first, then OpenAI."""
    question_type = classify_question(user_input)
    if question_type == "descriptive":
        return handle_descriptive(user_input)
    else:
        return get_openai_response(user_input)

def handle_descriptive(question):
    """Handles descriptive queries by searching the dataset and calling OpenAI if needed."""
    if df is None:
        return "Dataset not found!"

    try:
        # Convert column names to lowercase
        df.columns = df.columns.str.lower()

        # Find relevant rows based on question keywords
        relevant_data = df[df.apply(lambda row: any(keyword in str(row).lower() for keyword in question.lower().split()), axis=1)]

        # If no relevant data is found, use a small sample
        if relevant_data.empty:
            relevant_data = df.head(10)

        # Convert data to dictionary for structured response
        sample_data = relevant_data.to_dict(orient="records")

        # Create structured prompt for OpenAI
        prompt = (
            f"You are a data assistant. Answer the following question strictly based on the provided dataset.\n\n"
            f"Question: {question}\n"
            f"Data:\n{sample_data}\n"
            f"Be concise and consistent in your answers. If the information is not available, say 'The data does not provide a clear answer'."
        )

        # Call OpenAI for response
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            temperature=0,
            messages=[
                {"role": "system", "content": "You are a precise data analyst."},
                {"role": "user", "content": prompt}
            ]
        )

        return response['choices'][0]['message']['content']

    except Exception as e:
        return f"Error in descriptive question handling: {e}"
