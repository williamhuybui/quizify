import openai
openai.api_key = "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"
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
    List of Python dict (executable code): 
    """
    q_dict = eval(question_generator(prompt))
    return q_dict


# text = """The Netflix movie, Hunger, has been in and out of the streamer's top 10 movies list in recent weeks. It is a look into the cutthroat world of culinary artistry and the elite chefs who strive for perfection in not only the taste of their cuisine but also its appearance. Hunger is the story of a girl named Aoy (Chutimon Chuengcharoensukying) who runs her family's Thai noodle restaurant in the Royal Quarter of the capital city of Bangkok and is forced to make a decision about whether to leave the comfort of her familiar day-to-day life with her loving family to join an elite group of chefs and pursue taking the next step in her career. She has long admired Chef Paul (Nopachai Chaiyanam) from afar and so, she makes the decision to learn under his tutelage at the prestigious Hunger restaurant. After making this tough choice, her life starts to spin out of control as kitchen politics and interpersonal relationships threaten to derail everything she has worked for. It's a blunt commentary by director Sitisiri Mongkolsiri on class division and the artificial qualities valued by the wealthy class.
# Chef Paul, called "The High Priest" of Thai dining, runs a restaurant called Hunger. He is the top chef in Bangkok and is idolized by everyone in the food business and foodies who want to be associated with the prestige of his name. He comes across very much like a Thai equivalent of Chef Slowik (Ralph Fiennes) in 2022's The Menu (just a little less psychopathic and homicidal). He is austere, stone-faced, and intimidating. He insults his employees and routinely assaults them physically and emotionally. He runs a very tight ship and takes the art of cooking so seriously that his presence in the kitchen makes for a palpably tense workplace environment. Aoy's first encounter with Chef Paul doesn't go well, and she is climbing an uphill battle to win his respect for the rest of the movie.
# After being introduced to the seven-person staff, Aoy starts to seek out her niche within the group of apprentices. From her first day in the kitchen, Chef Paul is breathing down her neck and watching her every move to make sure she's good enough for him to devote his precious time to her development. Naturally, Chef Paul doesn't think she can do anything right and scolds her to the point of tears. Aoy starts to stay after hours toiling away at her craft (even falling asleep one night on the kitchen floor) in order to please Chef Paul, but she still struggles with adapting to his unique and strict code of conduct. It is a veritable boot camp for the culinary arts and Aoy has a steep learning curve.
# After suffering burns all over her arms and learning how to properly prepare meat to Chef Paul's standards, she has earned a chance to work with the crew as they cater high-profile events throughout Bangkok. Chef Paul meticulously cooks in front of Thai dignitaries and honored guests like a surgical performance artist and is routinely met with rounds of applause. Ominous music plays as the wealthy patrons aggressively and hastily slurp down their raw and fleshy cuts of bloodied meat and special sauces. Meanwhile, Aoy is assigned menial work and is harshly judged under Paul. She is already missing the love and simplicity of her family-run restaurant where cooking was fun, and she was with her family members.
# """
# n_question = 2
# res = multiple_choice_generator(text, n_question)
# print(res)