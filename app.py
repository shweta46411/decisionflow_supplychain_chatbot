import streamlit as st
from src.question_handler import handle_question


# Dynamically adjust path to recognize src as a module
import streamlit as st
from src.question_handler import handle_question  # ✅ Now it should work


# Streamlit UI
st.title("Supply Chain Data Assistantt 🤖 ")

# User Input
user_input = st.text_input("Ask me anything:")

# Button to Send Message
if st.button("Send"):
    if user_input.strip():
        response = handle_question(user_input)

        if isinstance(response, str):  # If OpenAI response or error
            st.write("🤖 Bot:", response)
        else:  # If dataset response is found
            st.write("📊 Data related to your query:")
            st.dataframe(response)
    else:
        st.warning("Please enter a question!")


st.markdown("---")  # Adds a separator line for clean UI
st.markdown("#### 💡Try asking:")
sample_questions = [
    "📦 *What are the most frequently ordered product types?",
    "🏙️ *How many orders were placed in each customer city?",
    "🚚 *Which shipping mode is used the most for delivering products?",
    "💰 *What is the total revenue generated from all sales?"
]

# Display questions in a lighter shade to make them feel like subtle suggestions
for question in sample_questions:
    st.markdown(f"<div style='color:gray; font-size:14px;'> {question}</div>", unsafe_allow_html=True)