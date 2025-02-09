import openai
import os
from dotenv import load_dotenv

# Load API key from .env file
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def handle_descriptive(question, df):
    """Uses OpenAI API to answer descriptive questions based on dataset."""
    try:
        prompt = f"Answer the following question based on the data provided: {question}\n\nData: {df.to_dict(orient='records')}"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a data assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error in descriptive question handling: {e}"
