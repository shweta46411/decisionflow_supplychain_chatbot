import streamlit as st
from optimization_model import define_optimization_model, solve_optimization_problem
from openai_handler import convert_to_human_readable
from question_handler import interpret_question
from utils import load_data

# Streamlit App Title
st.set_page_config(page_title="Optimization Chatbot", page_icon="📊")
st.title("📊 Supply Chain Optimization Assistant")

# Input Section
st.subheader("Ask a supply chain-related question:")
question = st.text_area("Enter your question here:", placeholder="How can I minimize shipping costs?")

# Submit Button 
if st.button("Submit"):
    if not question.strip():
        st.warning("Please enter a question before submitting.")
    else:
        # Interpret Question
        problem_details = interpret_question(question)
        if not problem_details:
            st.error("This question is outside the system's scope.")
        else:
            st.success("Valid question detected! Processing...")

            # Load Dataset
            data_path = "data/DataSet_Sprint1.xlsx"  # Ensure correct path
            data = load_data(data_path)
            
            if data is None:
                st.error("Error loading dataset. Please check the file path.")
            else:
                # Define Optimization Model
                model, shipment_vars = define_optimization_model(data)
                
                # Solve Optimization Model
                solution = solve_optimization_problem(model, shipment_vars)
                
                if not solution:
                    st.error("No optimal solution found.")
                else:
                    # Convert solution to human-readable format using OpenAI API
                    human_readable_output = convert_to_human_readable(solution)
                    
                    # Display results
                    st.subheader("🔍 Optimization Results")
                    st.json(solution)  # Display raw optimization variables
                    
                    st.subheader("📝 Human-Readable Explanation")
                    st.write(human_readable_output)  # Display AI-generated explanation
