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
# import streamlit as st
# from src.optimization_model import run_optimization
# from src.openai_handler import chatbot_response
# from src.question_handler import handle_descriptive, classify_question, run_what_if_scenario, handle_optimization

# # Set Page Configuration
# st.set_page_config(page_title="LogiFlow AI Assistant", page_icon="🤖", layout="wide")

# # Initialize session state for chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []

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

#         /* Chat message styling */
#         .chat-container {
#             max-height: 500px;
#             overflow-y: auto;
#             padding: 10px;
#         }
#         .chat-message {
#             padding: 10px;
#             border-radius: 15px;
#             margin-bottom: 5px;
#             max-width: 80%;
#         }
#         .user-message {
#             background-color: #E3F2FD !important; /* Light Blue */
#             text-align: right;
#             align-self: flex-end;
#         }
#         .bot-message {
#             background-color: #E8F5E9 !important; /* Light Green */
#             text-align: left;
#             align-self: flex-start;
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

# # Chat History Display

# chat_container = st.container()

# # Display previous messages from session
# with chat_container:
#     for msg in st.session_state.messages:
#         role, text = msg["role"], msg["text"]
#         if role == "user":
#             st.markdown(f'<div class="chat-message user-message">🧑‍💼 {text}</div>', unsafe_allow_html=True)
#         else:
#             st.markdown(f'<div class="chat-message bot-message">🤖 {text}</div>', unsafe_allow_html=True)

# # User Input Section
# question = st.text_area("💬 Type your question here:", height=80)

# # Submit Button
# submit_button = st.button("🚀 Ask LogiFlow")

# # Process User Input
# if submit_button:
#     if question.strip():
#         # Save user message to session state
#         st.session_state.messages.append({"role": "user", "text": question})
        
#         # Display user message
#         st.markdown(f'<div class="chat-message user-message">🧑‍💼 {question}</div>', unsafe_allow_html=True)

#         # Exit condition
#         if question.lower() == "exit":
#             st.warning("👋 Goodbye! Refresh the page to restart.")
#             st.stop()

#         # Classify question type
#         question_type = classify_question(question)

#         # Handle different question types
#         if question_type == "what-if":
#             response = run_what_if_scenario(question)

#         elif question_type == "optimization":
#             response = handle_optimization(question)

#         elif question_type == "descriptive":
#             response = handle_descriptive(question)

#         else:
#             response = "❓ I couldn't determine the question type. Please try again."

#         # Save bot response to session state
#         st.session_state.messages.append({"role": "bot", "text": response})

#         # Display bot message
#         st.markdown(f'<div class="chat-message bot-message">🤖 {response}</div>', unsafe_allow_html=True)

#         # Rerun the app to update UI with new messages
#         st.rerun()  # ✅ Updated from `st.experimental_rerun()`

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

# import streamlit as st
# from src.question_handler import classify_question, handle_descriptive, run_what_if_scenario, handle_optimization

# # 🛠️ Streamlit Page Config
# st.set_page_config(page_title="LogiFlow AI Assistant", page_icon="🤖", layout="wide")

# # 🧠 Session State for Chat History
# if "messages" not in st.session_state:
#     st.session_state.messages = []
# def clear_input_text():
#     st.session_state.input_text = ""
# # 🎨 Inject Custom CSS
# st.markdown("""
#     <style>
#         .main { background-color: #F8F9FA; }
#         .title { font-size: 32px; font-weight: bold; color: #2C3E50; text-align: center; margin-bottom: 5px; }
#         .subtitle { font-size: 18px; color: #5D6D7E; text-align: center; margin-bottom: 20px; }
#         .chat-message { padding: 10px; border-radius: 15px; margin-bottom: 5px; max-width: 80%; }
#         .user-message { background-color: #E3F2FD !important; text-align: right; align-self: flex-end; }
#         .bot-message { background-color: #E8F5E9 !important; text-align: left; align-self: flex-start; }
#         div.stButton > button {
#             background-color: #1E90FF; color: white !important; border: none;
#             padding: 10px 20px; font-size: 16px; border-radius: 6px;
#             transition: background-color 0.3s ease-in-out;
#         }
#         div.stButton > button:hover { background-color: #005BB5; }
#         .footer { text-align: center; color: gray; font-size: 14px; margin-top: 20px; }
#     </style>
# """, unsafe_allow_html=True)

# # 🔖 Title and Subtitle
# st.markdown('<h1 class="title">🤖 LogiFlow AI Assistant</h1>', unsafe_allow_html=True)
# st.markdown('<h3 class="subtitle">Optimize Logistics. Streamline Operations.</h3>', unsafe_allow_html=True)

# # 💬 Chat Display
# chat_container = st.container()
# with chat_container:
#     for msg in st.session_state.messages:
#         role, text = msg["role"], msg["text"]
#         role_class = "user-message" if role == "user" else "bot-message"
#         emoji = "🧑‍💼" if role == "user" else "🤖"
#         st.markdown(f'<div class="chat-message {role_class}">{emoji} {text}</div>', unsafe_allow_html=True)

# # 📝 Input Section
# question = st.text_area("💬 Type your question here:", height=80, key="input_text")

# submit_button = st.button("🚀 Ask LogiFlow", on_click=clear_input_text)

# # 🚀 On Submit
# if submit_button and st.session_state.input_text.strip():
#     question = st.session_state.input_text.strip()

#     st.session_state.messages.append({"role": "user", "text": question})
#     st.markdown(f'<div class="chat-message user-message">🧑‍💼 {question}</div>', unsafe_allow_html=True)

#     try:
#         question_type = classify_question(question)

#         if question_type == "descriptive":
#             response = handle_descriptive(question)
#         elif question_type == "optimization":
#             response = handle_optimization()
#         elif question_type == "what-if":
#             response = run_what_if_scenario(question)
#         else:
#             response = "❓ I couldn't determine the question type. Please try again."

#     except Exception as e:
#         response = f"🤖 I'm having trouble answering that. Please rephrase your question."

#     st.session_state.messages.append({"role": "bot", "text": response})
#     st.session_state.input_text = ""  # ✅ clear textbox
#     st.rerun()

# elif submit_button:
#     st.warning("⚠️ Please enter a valid question.")


# # 📎 Footer
# st.markdown("""
#     <div class="footer">
#         🚀 Built with Streamlit | AI-Powered Logistics Assistant
#     </div>
# """, unsafe_allow_html=True)

# import streamlit as st
# from src.question_handler import classify_question, handle_descriptive, run_what_if_scenario, handle_optimization

# # 🛠️ Page setup
# st.set_page_config(page_title="LogiFlow AI Assistant", page_icon="🤖", layout="wide")

# # 🧠 Session state setup
# if "messages" not in st.session_state:
#     st.session_state.messages = []

# if "input_text" not in st.session_state:
#     st.session_state.input_text = ""

# if "show_spinner" not in st.session_state:
#     st.session_state.show_spinner = False

# # ✅ Handle question input
# def handle_question():
#     question = st.session_state.input_text.strip()

#     if not question:
#         st.warning("⚠️ Please enter a valid question.")
#         return

#     st.session_state.messages.append({"role": "user", "text": question})
#     st.session_state.show_spinner = True  # Show "Thinking..." message

#     try:
#         question_type = classify_question(question)

#         if question_type == "descriptive":
#             response = handle_descriptive(question)
#         elif question_type == "optimization":
#             response = handle_optimization()
#         elif question_type == "what-if":
#             response = run_what_if_scenario(question)
#         else:
#             response = "❓ I couldn't determine the question type. Please try again."

#     except Exception:
#         response = "🤖 Hmm, I wasn’t able to process that. Try asking in a different way?"

#     st.session_state.messages.append({"role": "bot", "text": response})
#     st.session_state.input_text = ""
#     st.session_state.show_spinner = False  # Hide spinner

# # 🎨 Custom CSS (unchanged)
# st.markdown("""
#     <style>
#         .main { background-color: #F8F9FA; }
#         .title { font-size: 32px; font-weight: bold; color: #2C3E50; text-align: center; margin-bottom: 5px; }
#         .subtitle {
#             font-size: 18px;
#             color: #5D6D7E;
#             text-align: center;
#             margin-bottom: 10px;
#         }
#         .chat-message {
#             padding: 10px;
#             border-radius: 15px;
#             margin-bottom: 4px;
#             max-width: 80%;
#             line-height: 1.5;
#         }
#         .user-message {
#             background-color: #E3F2FD !important;
#             text-align: right;
#             margin-left: auto;
#         }
#         .bot-message {
#             background-color: #E8F5E9 !important;
#             text-align: left;
#             margin-right: auto;
#         }
#         div.stButton > button {
#             background-color: #1E90FF;
#             color: white !important;
#             border: none;
#             padding: 10px 20px;
#             font-size: 16px;
#             border-radius: 6px;
#             transition: background-color 0.3s ease-in-out;
#         }
#         div.stButton > button:hover {
#             background-color: #005BB5;
#         }
#         .footer {
#             text-align: center;
#             color: gray;
#             font-size: 14px;
#             margin-top: 20px;
#         }
#     </style>
# """, unsafe_allow_html=True)

# # 🔖 Title and subtitle
# st.markdown('<h1 class="title">🤖 LogiFlow AI Assistant</h1>', unsafe_allow_html=True)
# st.markdown('<h3 class="subtitle">Optimize Logistics. Streamline Operations.</h3>', unsafe_allow_html=True)

# # 💬 Chat display
# with st.container():
#     for msg in st.session_state.messages:
#         role = msg["role"]
#         role_class = "user-message" if role == "user" else "bot-message"
#         emoji = "🧑‍💼" if role == "user" else "🤖"
#         st.markdown(f'<div class="chat-message {role_class}">{emoji} {msg["text"]}</div>', unsafe_allow_html=True)

# # 📝 Text input and button
# st.text_area("💬 Type your question here:", height=80, key="input_text")
# st.button("🚀 Ask LogiFlow", on_click=handle_question)

# # ⏳ Spinner message below button
# if st.session_state.show_spinner:
#     st.markdown(
#         "<div style='padding-top:10px; font-size:16px;'>⏳ <b>Thinking...</b></div>",
#         unsafe_allow_html=True
#     )

# # 📎 Footer
# st.markdown("""
#     <div class="footer">
#         🚀 Built with Streamlit | AI-Powered Logistics Assistant
#     </div>
# """, unsafe_allow_html=True)
import streamlit as st
from src.question_handler import classify_question, handle_descriptive, run_what_if_scenario, handle_reset, handle_continue,handle_optimization


# 🔧 Page config
st.set_page_config(page_title="LogiFlow Chat", page_icon="🤖", layout="wide")

# 🧠 Session state setup
if "messages" not in st.session_state:
    st.session_state.messages = []
if "input_text" not in st.session_state:
    st.session_state.input_text = ""
if "thinking" not in st.session_state:
    st.session_state.thinking = False
# 🧶 Main handler

def handle_question():
    question = st.session_state.input_text.strip()
    if not question:
        return
    st.session_state.thinking = True
    st.session_state.messages.append({"role": "user", "text": question})
    st.session_state.input_text = ""

    try:
        question_type = classify_question(question)

        if question_type == "reset":
    # reset globals in question_handler (you'll need to implement handle_reset)
            response = handle_reset()  

        elif question_type == "continue":
    # keep using the last what‐if data
            response = handle_continue()

        elif question_type == "descriptive":
            response = handle_descriptive(question)

        elif question_type == "optimization":
            response = handle_optimization(question)

        elif question_type == "what-if":
    # run and then append the conversational follow-up
            summary = run_what_if_scenario(question)
            response = (
            summary
             + "\n\nAll set! I’ve applied that change. "
            + "Would you like to keep exploring this scenario, or should we switch back to the original numbers? "
            + "Just say ‘keep going’ or ‘reset.’"
        )

        else:
            response = "❓ I couldn't determine the question type. Please try again."
    
    except Exception as e: 
            response = "🧠 Hmm, I wasn’t able to process that. Try rephrasing it."
            print("Error:", Exception)
            print("What-If Error:", e)
            import traceback; traceback.print_exc()

    st.session_state.messages.append({"role": "bot", "text": response})
    st.session_state.thinking = False
# 🌈 CSS
st.markdown("""
    <style>
        .main { background-color: #F8F9FA; }
        .chat-container { max-width: 800px; margin: auto; }
        .message { padding: 1rem; border-radius: 10px; margin-bottom: 1rem; font-size: 16px; line-height: 1.5; }
        .user { background-color: #f0f4ff; text-align: right; border: 1px solid #d6e1ff; }
        .bot { background-color: #e6f5ea; text-align: left; border: 1px solid #bfe5d0; }
        .avatar { font-size: 20px; font-weight: bold; margin-bottom: 0.2rem; }
        .footer { text-align: center; margin-top: 30px; color: gray; font-size: 13px; }
        .sticky-header {
            position: sticky;
            top: 0;
            background-color: #F8F9FA;
            z-index: 1000;
            padding-top: 10px;
            padding-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
        }
    </style>
""", unsafe_allow_html=True)



st.markdown("""
<div class='chat-container' style='text-align: center; padding-top: 1rem;'>
    <div style='display: inline-flex; flex-direction: column; align-items: center; gap: 0.5rem;'>
        <h1 style='margin: 0; font-size: 40px;'>🤖 LogiFlow AI Assistant</h1>
        <p style='color: #5D6D7E; font-size: 15px; margin: 0;'>Optimize Logistics. Streamline Operations.</p>
    </div>
</div>
""", unsafe_allow_html=True)

# 💬 Chat history
with st.container():
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for msg in st.session_state.messages:
        role = msg["role"]
        bubble_class = "user" if role == "user" else "bot"
        icon = "👩‍💼" if role == "user" else "🤖"
        st.markdown(f"<div class='message {bubble_class}'><div class='avatar'>{icon}</div>{msg['text']}</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 🖋️ Text input
# 🖋️ Text input with embedded SVG Enter icon
# 🖋️ Text input with SVG icon inside
# 🖋️ Input box with SVG enter icon inside (streamlit-compatible)

st.markdown("""
<style>
.input-container {
    position: relative;
    max-width: 800px;
    margin: 1rem auto 0 auto; /* changed from 2rem top */
   
}

/* 🔧 Prevent overflow clipping */
[data-baseweb="input"] {
    min-height: 60px !important;
    border: none !important;
    box-shadow: none !important;
    overflow: visible !important;
}

/* ✅ Main input style */
input[type="text"] {
    min-height: 60px !important;
    font-size: 17px !important;
    padding: 14px 45px 14px 20px !important;
    border-radius: 6px !important;
    border: 1px solid #D1D9E6 !important;
    box-sizing: border-box;
    transition: border 0.3s ease, box-shadow 0.3s ease;
    background-color: #f4f6f9 !important;
}

/* ✨ Focus blue border + soft glow */
input[type="text"]:focus {
    border: 1px solid #8AC8FF !important;
    box-shadow: 0 0 6px rgba(0, 123, 255, 0.4) !important;
    outline: none !important;
}

/* ✅ Suppress red invalid border */
input[type="text"]:focus:invalid {
    border: 1px solid #8AC8FF !important;
    box-shadow: 0 0 6px rgba(0, 123, 255, 0.4) !important;
}

/* 🧠 Enter icon */
.enter-icon {
    position: absolute;
    right: 16px;
    top: 50%;
    transform: translateY(-178%);
    font-size: 20px;
    opacity: 0.3;
    pointer-events: none;
}
</style>
""", unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="input-container">', unsafe_allow_html=True)

    st.text_input(
        label="💬 Enter a query for analysis or insights",
        key="input_text",
        placeholder="Type your question here..",
        on_change=handle_question
    )
    if st.session_state.get("thinking", False):
        st.markdown("""
            <div style='text-align: left; padding-top: 5px; font-size: 14px; color: #888; max-width: 800px; margin: 0 auto;'>
                🤖 Thinking...
            </div>
        """, unsafe_allow_html=True)
        st.write("Thinking state:", st.session_state.thinking)
    st.markdown('<span class="enter-icon">⏎</span>', unsafe_allow_html=True)
   
    st.markdown('</div>', unsafe_allow_html=True)
    

    

# if st.session_state.thinking:
#     st.markdown("""
#         <div class='chat-container'>
#             <div class='message bot'>
#                 <div class='avatar'>🤖</div>
#                 Thinking...
#             </div>
#         </div>
#     """, unsafe_allow_html=True)





# 📅 Footer
st.markdown("""
    <div class='footer'>🚀 Built with Streamlit | AI-powered Logistics Assistant</div>
""", unsafe_allow_html=True)