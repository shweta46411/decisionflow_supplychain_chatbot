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

# import streamlit as st
# from src.optimization_model import run_optimization
# from src.openai_handler import chatbot_response

# from src.question_handler import handle_descriptive, classify_question  , run_what_if_scenario, handle_optimization

# # Set page configuration
# #st.set_page_config(page_title="LogiFlow AI Assistant", page_icon="🤖", layout="wide")
# # Placeholder Functions (Replace with actual implementations)
# # def handle_optimization(question):
# #     """Placeholder function for handling optimization-related queries."""
# #     return "⚙️ Optimization logic is not yet implemented. Coming soon!"

# # def run_what_if_scenario(question):
# #     """Placeholder function for handling 'What-If' scenario queries."""
# #     return "🔄 What-If scenario analysis is under development."


# # Custom CSS for styling text area & button
# st.markdown(
#     """
#     <style>
#         .main {
#             background-color: #F8F9FA;
#         }
#         .stChatMessage {
#             border-radius: 15px;
#             padding: 10px;
#         }
#         .user {
#             background-color: #E3F2FD;
#             text-align: right;
#         }
#         .bot {
#             background-color: #E8F5E9;
#             text-align: left;
#         }
#         .title {
#             font-size: 32px;
#             font-weight: bold;
#             color: #2C3E50;
#             text-align: center;
#         }
#         .subtitle {
#             font-size: 18px;
#             color: #5D6D7E;
#             text-align: center;
#             margin-bottom: 20px;
#         }
#         /* Change text area border to blue when focused */

#         textarea {
#             border: 1px solid #D1D9E6 !important; /* Light default border */
#             border-radius: 5px;
            
#         }
#         textarea:focus {
#             border: 1px solid #007BFF !important; /* Blue focus border */
#             box-shadow: 0 0 5px rgba(0, 123, 255, 0.5) !important; /* Light blue glow */
#             outline: none !important;
#         }
#         /* Override red error styles if present */
#         textarea:focus:invalid {
#             border:12px solid #007BFF !important; /* Ensure blue even if invalid */
#         }
#         /* Style the button */
#        div.stButton > button {
#             background-color: #1E90FF;
#             color: white !important;
#             border: none;
#             padding: 6px 12px;
#             font-size: 14px;
#             border-radius: 6px;
#             border-color: #1E90FF;
#             cursor: pointer;   
#             transition: background-color 0.3s ease-in-out;
#             display: inline-flex;
#             align-items: center;
#             gap: 5px;
#             width: auto;
#             justify-content: left;
#         }
#         /* Darker blue button on hover */
#         div.stButton > button:hover {
#             background-color: #005BB5;
#         }
#     </style>
#     """,
#     unsafe_allow_html=True,
# )

# # App Title with Bot Emoji
# st.markdown('<h1 class="title">🤖 LogiFlow AI Assistant</h1>', unsafe_allow_html=True)
# st.markdown('<h3 class="subtitle">Optimize Logistics. Streamline Operations.</h3>', unsafe_allow_html=True)

# # Chat interface
# # st.write("##### Smart Logistics Assistant!")
# # User Input Section
# question = st.text_area("💬 Type your question here:", height=70)

# # Submit Button
# col1, col2, col3 = st.columns([2, 1, 2])
# with col2:
#     submit_button = st.button("🚀 Submit")

# # Process User Input
# if submit_button:
#     if question.strip():  # Ensures input is not empty
#         # st.chat_message("user").write(question)  # Display user input

#         if question.lower() == "exit":
#             st.write("👋 Goodbye! Refresh the page to restart.")
#             st.stop()

#         # Classify question type
#         question_type = classify_question(question)

#         # Handle different question types
#         if question_type == "what-if":
#             st.info("🔄 Running What-If Scenario...")
#             response = run_what_if_scenario(question)

#         elif question_type == "optimization":
#             st.info("⚙️ Running Optimization...")
#             response = handle_optimization(question)

#         elif question_type == "descriptive":
#             st.info("📖 Fetching Descriptive Insights...")
#             response = handle_descriptive(question)

#         else:
#             response = "❓ I could not determine the question type. Please try again."

#         # Display Chatbot Response
#         st.chat_message("bot").write(response)

#     else:
#         st.warning("⚠️ Please enter a valid question.")

# # Footer
# st.markdown(
#     """
#     <br><hr>
#     <div style="text-align: center; color: gray; font-size: 14px;">
#         🚀 Built with Streamlit | AI-Powered Logistics Assistant
#     </div>
#     """,
#     unsafe_allow_html=True,
# )

# import streamlit as st
# from src.optimization_model import run_optimization
# from src.openai_handler import chatbot_response
# from src.question_handler import handle_descriptive, classify_question, run_what_if_scenario, handle_optimization

# # Set Page Configuration
# #st.set_page_config(page_title="LogiFlow AI Assistant", page_icon="🤖", layout="wide")

# # Inject Custom CSS for Better Styling
# st.markdown("""
#     <style>
#         /* Page background */
#         .main {
#             background-color: #F8F9FA;
#         }
        
#         /* Title and subtitle styling */
#         .title {
#             font-size: 32px;
#             font-weight: bold;
#             color: #2C3E50;
#             text-align: center;
#             margin-bottom: 5px;
#         }
#         .subtitle {
#             font-size: 18px;
#             color: #5D6D7E;
#             text-align: center;
#             margin-bottom: 20px;
#         }

#         /* Chat styling */
#         .stChatMessage {
#             border-radius: 15px;
#             padding: 10px;
#             margin-bottom: 10px;
#         }
#         .user-message {
#             background-color: #E3F2FD !important; /* Light Blue */
#             text-align: right;
#             border-radius: 15px;
#             padding: 10px;
#         }
#         .bot-message {
#             background-color: #E8F5E9 !important; /* Light Green */
#             text-align: left;
#             border-radius: 15px;
#             padding: 10px;
#         }

#         /* Input area styling */
#         textarea {
#             border: 1px solid #D1D9E6 !important;
#             border-radius: 8px;
#             font-size: 16px;
#         }
#         textarea:focus {
#             border: 1px solid #007BFF !important;
#             box-shadow: 0 0 5px rgba(0, 123, 255, 0.5) !important;
#         }

#         /* Button styling */
#         div.stButton > button {
#             background-color: #1E90FF;
#             color: white !important;
#             border: none;
#             padding: 10px 20px;
#             font-size: 16px;
#             border-radius: 6px;
#             cursor: pointer;
#             transition: background-color 0.3s ease-in-out;
#         }
#         div.stButton > button:hover {
#             background-color: #005BB5;
#         }

#         /* Footer Styling */
#         .footer {
#             text-align: center;
#             color: gray;
#             font-size: 14px;
#             margin-top: 20px;
#         }
#     </style>
#     """, unsafe_allow_html=True)

# # App Title and Subtitle
# st.markdown('<h1 class="title">🤖 LogiFlow AI Assistant</h1>', unsafe_allow_html=True)
# st.markdown('<h3 class="subtitle">Optimize Logistics. Streamline Operations.</h3>', unsafe_allow_html=True)

# # Chat Interface
# st.write("#### 💬 Ask your logistics-related question below:")

# # User Input Section
# question = st.text_area("Enter your question:", height=80)

# # Submit Button
# submit_button = st.button("🚀 Ask LogiFlow")

# # Process User Input
# if submit_button:
#     if question.strip():
#         # Display user input message with custom styling
#         st.markdown(f'<div class="user-message">🧑‍💼 {question}</div>', unsafe_allow_html=True)

#         # Exit condition
#         if question.lower() == "exit":
#             st.warning("👋 Goodbye! Refresh the page to restart.")
#             st.stop()

#         # Classify question type
#         question_type = classify_question(question)

#         # Handle different question types
#         if question_type == "what-if":
#             st.info("🔄 Running What-If Scenario...")
#             response = run_what_if_scenario(question)

#         elif question_type == "optimization":
#             st.info("⚙️ Running Optimization...")
#             response = handle_optimization(question)

#         elif question_type == "descriptive":
#             st.info("📖 Fetching Descriptive Insights...")
#             response = handle_descriptive(question)

#         else:
#             response = "❓ I couldn't determine the question type. Please try again."

#         # Display chatbot response with custom styling
#         st.markdown(f'<div class="bot-message">🤖 {response}</div>', unsafe_allow_html=True)

#     else:
#         st.warning("⚠️ Please enter a valid question.")

# # Footer
# st.markdown(
#     """
#     <div class="footer">
#         🚀 Built with Streamlit | AI-Powered Logistics Assistant
#     </div>
#     """,
#     unsafe_allow_html=True
# )
import streamlit as st
from src.optimization_model import run_optimization
from src.openai_handler import chatbot_response
from src.question_handler import handle_descriptive, classify_question, run_what_if_scenario, handle_optimization

# Set Page Configuration
st.set_page_config(page_title="LogiFlow AI Assistant", page_icon="🤖", layout="wide")

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inject Custom CSS for Better Styling
st.markdown("""
    <style>
        /* Page background */
        .main {
            background-color: #F8F9FA;
        }

        /* Title and subtitle styling */
        .title {
            font-size: 32px;
            font-weight: bold;
            color: #2C3E50;
            text-align: center;
            margin-bottom: 5px;
        }
        .subtitle {
            font-size: 18px;
            color: #5D6D7E;
            text-align: center;
            margin-bottom: 20px;
        }

        /* Chat message styling */
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
            padding: 10px;
        }
        .chat-message {
            padding: 10px;
            border-radius: 15px;
            margin-bottom: 5px;
            max-width: 80%;
        }
        .user-message {
            background-color: #E3F2FD !important; /* Light Blue */
            text-align: right;
            align-self: flex-end;
        }
        .bot-message {
            background-color: #E8F5E9 !important; /* Light Green */
            text-align: left;
            align-self: flex-start;
        }

        /* Input area styling */
        textarea {
            border: 1px solid #D1D9E6 !important;
            border-radius: 8px;
            font-size: 16px;
        }
        textarea:focus {
            border: 1px solid #007BFF !important;
            box-shadow: 0 0 5px rgba(0, 123, 255, 0.5) !important;
        }

        /* Button styling */
        div.stButton > button {
            background-color: #1E90FF;
            color: white !important;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            border-radius: 6px;
            cursor: pointer;
            transition: background-color 0.3s ease-in-out;
        }
        div.stButton > button:hover {
            background-color: #005BB5;
        }

        /* Footer Styling */
        .footer {
            text-align: center;
            color: gray;
            font-size: 14px;
            margin-top: 20px;
        }
    </style>
    """, unsafe_allow_html=True)

# App Title and Subtitle
st.markdown('<h1 class="title">🤖 LogiFlow AI Assistant</h1>', unsafe_allow_html=True)
st.markdown('<h3 class="subtitle">Optimize Logistics. Streamline Operations.</h3>', unsafe_allow_html=True)

# Chat History Display

chat_container = st.container()

# Display previous messages from session
with chat_container:
    for msg in st.session_state.messages:
        role, text = msg["role"], msg["text"]
        if role == "user":
            st.markdown(f'<div class="chat-message user-message">🧑‍💼 {text}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="chat-message bot-message">🤖 {text}</div>', unsafe_allow_html=True)

# User Input Section
question = st.text_area("💬 Type your question here:", height=80)

# Submit Button
submit_button = st.button("🚀 Ask LogiFlow")

# Process User Input
if submit_button:
    if question.strip():
        # Save user message to session state
        st.session_state.messages.append({"role": "user", "text": question})
        
        # Display user message
        st.markdown(f'<div class="chat-message user-message">🧑‍💼 {question}</div>', unsafe_allow_html=True)

        # Exit condition
        if question.lower() == "exit":
            st.warning("👋 Goodbye! Refresh the page to restart.")
            st.stop()

        # Classify question type
        question_type = classify_question(question)

        # Handle different question types
        if question_type == "what-if":
            response = run_what_if_scenario(question)

        elif question_type == "optimization":
            response = handle_optimization(question)

        elif question_type == "descriptive":
            response = handle_descriptive(question)

        else:
            response = "❓ I couldn't determine the question type. Please try again."

        # Save bot response to session state
        st.session_state.messages.append({"role": "bot", "text": response})

        # Display bot message
        st.markdown(f'<div class="chat-message bot-message">🤖 {response}</div>', unsafe_allow_html=True)

        # Rerun the app to update UI with new messages
        st.rerun()  # ✅ Updated from `st.experimental_rerun()`

    else:
        st.warning("⚠️ Please enter a valid question.")

# Footer
st.markdown(
    """
    <div class="footer">
        🚀 Built with Streamlit | AI-Powered Logistics Assistant
    </div>
    """,
    unsafe_allow_html=True
)
