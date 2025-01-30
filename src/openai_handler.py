import openai

def convert_to_human_readable(solution):
    prompt = f"Convert the following solution into a human-readable format:\n\n{solution}"
    
    # Use the latest supported model
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=500,
    )
    
    return response['choices'][0]['message']['content']
