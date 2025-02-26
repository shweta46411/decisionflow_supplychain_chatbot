# import streamlit as st


# # Set page config
# st.set_page_config(page_title="LogiFlow Data Assistant", layout="wide")
# from src.question_handler import handle_question
# from src.optimization_model import run_optimization
# st.title("LogiFlow Data Assistant 🤖")
# st.subheader("Optimize Logistics. Streamline Operations.")

# # Run Optimization Model on App Load (Silent Execution)
# @st.cache_data
# def get_optimized_data():
#     return run_optimization()

# _ = get_optimized_data()  # Runs in background

# # User Input for Questions
# user_input = st.text_input("Ask me anything about logistics:", "")

# # Process User Question
# if st.button("Send"):
#     if user_input.strip():
#         try:
#             response = handle_question(user_input)

#             if isinstance(response, str):  # LLM Response or Error
#                 st.write("🤖 Bot:", response)
#             else:  # If dataset response is found
#                 st.write("📊 Data related to your query:")
#                 st.dataframe(response)

#         except Exception as e:
#             st.error(f"An error occurred: {str(e)}")
#     else:
#         st.warning("Please enter a question!")

# # Footer
# st.markdown("---")
# st.markdown("🚀 Built with Streamlit | Powered by Gurobi & OpenAI")

import streamlit as st
from src.optimization_model import run_optimization
from src.openai_handler import chatbot_response
from src.question_handler import process_question

# Set page configuration
st.set_page_config(page_title="LogiFlow AI Assistant", page_icon="🤖", layout="wide")

# Custom CSS for styling text area & button
st.markdown(
    """
    <style>
        .main {
            background-color: #F8F9FA;
        }
        .stChatMessage {
            border-radius: 15px;
            padding: 10px;
        }
        .user {
            background-color: #E3F2FD;
            text-align: right;
        }
        .bot {
            background-color: #E8F5E9;
            text-align: left;
        }
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
        }
        .subtitle {
            font-size: 18px;
            color: #5D6D7E;
            text-align: center;
            margin-bottom: 20px;
        }
        /* Change text area border to blue when focused */

        textarea {
            border: 1px solid #D1D9E6 !important; /* Light default border */
            border-radius: 5px;
            
        }
        textarea:focus {
            border: 1px solid #007BFF !important; /* Blue focus border */
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5) !important; /* Light blue glow */
            outline: none !important;
        }
        /* Override red error styles if present */
        textarea:focus:invalid {
            border:12px solid #007BFF !important; /* Ensure blue even if invalid */
        }
        /* Style the button */
       div.stButton > button {
            background-color: #1E90FF;
            color: white !important;
            border: none;
            padding: 6px 12px;
            font-size: 14px;
            border-radius: 6px;
            border-color: #1E90FF;
            cursor: pointer;   
            transition: background-color 0.3s ease-in-out;
            display: inline-flex;
            align-items: center;
            gap: 5px;
            width: auto;
            justify-content: left;
        }
        /* Darker blue button on hover */
        div.stButton > button:hover {
            background-color: #005BB5;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# App Title with Bot Emoji
st.markdown('<h1 class="title">🤖 LogiFlow AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subtitle">Optimize Logistics. Streamline Operations.</h3>', unsafe_allow_html=True)

# Chat interface
# st.write("##### Smart Logistics Assistant!")
user_input = st.text_area("Type your question here...", height=70)

col1, col2 = st.columns([1, 2])

submit_button = st.button("🚀 Submit", use_container_width=False)

# Process user input
if submit_button:
    if user_input:
        # st.chat_message("user").write(user_input)  # Show user message in chat format
        
        if "optimize" in user_input.lower():
            response = run_optimization()
        else:
            response = chatbot_response(user_input)
        
        st.chat_message("bot").write(response)  # Show bot response in chat format
    else:
        st.warning("⚠️ Please enter a question.")

# Footer
st.markdown(
    """
    <br><hr>
    <div style="text-align: center; color: gray; font-size: 14px;">
        Built with Streamlit | AI-Powered Logistics Assistant
    </div>
    """,
    unsafe_allow_html=True,
)

