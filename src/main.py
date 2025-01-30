from src.question_handler import interpret_question
from src.optimization_model import define_optimization_model, solve_optimization_problem
from src.openai_handler import convert_to_human_readable
from src.utils import load_data


def main():
    # Step 1: Get planner's question
    question = input("Enter your predictive question: ")

    # Step 2: Interpret the question
    problem_details = interpret_question(question)
    if not problem_details:
        print("This question is outside the system's scope.")
        return

    # Step 3: Load data
    filepath = "data/DataSet_Sprint1.xlsx"  # Update path if needed
    data = load_data(filepath)
    if data is None:
        return

    # Step 4: Define the optimization problem
    model, shipment_vars = define_optimization_model(data)

    # Step 5: Solve the problem
    solution = solve_optimization_problem(model, shipment_vars)
    if not solution:
        print("No optimal solution found.")
        return

    # Step 6: Convert to human-readable format
    human_readable_output = convert_to_human_readable(solution)

    # Step 7: Display the response
    print("\nPlanner's Response:")
    print(human_readable_output)

if __name__ == "__main__":
    main()
