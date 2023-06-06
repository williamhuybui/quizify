import openai
openai.api_key = "your_API"
def question_generator(prompt, model = "gpt-3.5-turbo"):
    """
    Receive a prompt and return the output from ChatGPT
    """

    response = openai.ChatCompletion.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
    )
    return response["choices"][0]["message"]["content"]

def multiple_choice_generator(text, n_question):
    example = [
    {
        "question": "Who was the first President of the United States?",
        "options": [
            "George Washington",
            "Thomas Jefferson",
            "Abraham Lincoln",
            "Benjamin Franklin",
        ],
        "answer": "George Washington",
    },
    {
        "question": "Which event marked the beginning of the American Revolutionary War?",
        "options": [
            "Boston Tea Party",
            "Declaration of Independence",
            "Battle of Bunker Hill",
            "Boston Massacre",
        ],
        "answer": "Battle of Bunker Hill",
    }
    ]
    prompt = f""" Create {n_question} 4-multiple choice questions from the below text using the the following list of dict format example.
    Example: {example}
    Text:{text}
    List of dict: 
    """
    q_dict = eval(question_generator(prompt))
    return q_dict

