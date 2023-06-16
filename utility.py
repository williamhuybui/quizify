from newspaper import Article
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch, random, re

########### Load model ############
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

g1_model = AutoModelForSeq2SeqLM.from_pretrained("./models/g1_model/")
g2_model = AutoModelForSeq2SeqLM.from_pretrained("./models/g2_model/")
g1_tokenizer = AutoTokenizer.from_pretrained("./models/g1_tokenizer/")
g2_tokenizer = AutoTokenizer.from_pretrained("./models/g2_tokenizer/")

g1_model.eval()
g2_model.eval()
g1_model.to(device)
g2_model.to(device)

##########################

@torch.no_grad()
def question_generation_sampling(
    g1_model,
    g1_tokenizer,
    g2_model,
    g2_tokenizer,
    context,
    num_questions,
    device,
):
    qa_input_ids = prepare_qa_input(
            g1_tokenizer,
            context=context,
            device=device,
    )
    max_repeated_sampling = int(num_questions * 4) # sometimes generated question+answer is invalid
    num_valid_questions = 0
    questions = []
    for q_ in range(max_repeated_sampling):
        # Stage G.1: question+answer generation
        outputs = g1_model.generate(
            qa_input_ids,
            max_new_tokens=128,
            do_sample=True,
        )
        question_answer = g1_tokenizer.decode(outputs[0], skip_special_tokens=False)
        question_answer = question_answer.replace(g1_tokenizer.pad_token, "").replace(g1_tokenizer.eos_token, "")
        question_answer_split = question_answer.split(g1_tokenizer.sep_token)
        if len(question_answer_split) == 2:
            # valid Question + Annswer output
            num_valid_questions += 1
        else:
            continue
        question = question_answer_split[0].strip()
        answer = question_answer_split[1].strip()

        # Stage G.2: Distractor Generation
        distractor_input_ids = prepare_distractor_input(
            g2_tokenizer,
            context = context,
            question = question,
            answer = answer,
            device = device,
            separator = g2_tokenizer.sep_token,
        )
        outputs = g2_model.generate(
            distractor_input_ids,
            max_new_tokens=128,
            do_sample=True,
        )
        distractors = g2_tokenizer.decode(outputs[0], skip_special_tokens=False)
        distractors = distractors.replace(g2_tokenizer.pad_token, "").replace(g2_tokenizer.eos_token, "")
        distractors = re.sub("<extra\S+>", g2_tokenizer.sep_token, distractors)
        distractors = [y.strip() for y in distractors.split(g2_tokenizer.sep_token)]
        distractors = list(set(distractors))
        options = [answer] + distractors

        if len(options) == 2:
            options.append("All of the answer is correct")
            options.append("None of the answer is correct")
        elif len(options) == 3:
            options.append("None of the answer is correct")

        question_item = {
            'question': question,
            'options': options,
        }
        questions.append(question_item)
        if num_valid_questions == num_questions:
            break
    return questions


def prepare_qa_input(t5_tokenizer, context, device):
    """
    input: context
    output: question <sep> answer
    """
    encoding = t5_tokenizer(
        [context],
        return_tensors="pt",
    )
    input_ids = encoding.input_ids.to(device)
    return input_ids


def prepare_distractor_input(t5_tokenizer, context, question, answer, device, separator='<sep>'):
    """
    input: question <sep> answer <sep> article
    output: distractor1 <sep> distractor2 <sep> distractor3
    """
    input_text = question + ' ' + separator + ' ' + answer + ' ' + separator + ' ' + context
    encoding = t5_tokenizer(
        [input_text],
        return_tensors="pt",
    )
    input_ids = encoding.input_ids.to(device)
    return input_ids

def generate_multiple_choice_question(
    context
):
    num_questions = 1
    question_item = question_generation_sampling(
        g1_model, g1_tokenizer,
        g2_model, g2_tokenizer,
        context, num_questions, device
    )[0]
    question = question_item['question']
    options = question_item['options']
    answer = options[0]
    random.shuffle(options) # shuffle options
    question_json = {
        'question': question,
        'options': options,
        'answer': options[0]
    }
    return question_json


def split_into_sentences(text: str) -> list[str]:
    """
    Split the text into sentences.

    If the text contains substrings "<prd>" or "<stop>", they would lead 
    to incorrect splitting because they are used as markers for splitting.

    :param text: text to be split into sentences
    :type text: str

    :return: list of sentences
    :rtype: list[str]
    """
    alphabets = "([A-Za-z])"
    prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
    suffixes = "(Inc|Ltd|Jr|Sr|Co)"
    starters = "(Mr|Mrs|Ms|Dr|Prof|Capt|Cpt|Lt|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
    acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
    websites = "[.](com|net|org|io|gov|edu|me)"
    digits = "([0-9])"
    multiple_dots = r'\.{2,}'

    # Preprocess text
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    text = re.sub(digits + "[.]" + digits, "\\1<prd>\\2", text)
    text = re.sub(multiple_dots, lambda match: "<prd>" * len(match.group(0)) + "<stop>", text)
    if "Ph.D" in text:
        text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + alphabets + "[.]", " \\1<prd>", text)
    if "”" in text:
        text = text.replace(".”", "”.")
    if "\"" in text:
        text = text.replace(".\"", "\".")
    if "!" in text:
        text = text.replace("!\"", "\"!")
    if "?" in text:
        text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")

    # Split text into sentences
    sentences = text.split("<stop>")
    sentences = [s.strip() for s in sentences]
    if sentences and not sentences[-1]:
        sentences = sentences[:-1]
    
    return sentences


def combine_sentences(text, word_limit=50):
    """
    Combine sentences into chunks based on a word limit.

    :param text: text containing sentences
    :type text: str
    :param word_limit: maximum number of words in each chunk, defaults to 33
    :type word_limit: int, optional
    :return: list of chunks
    :rtype: list[str]
    """
    sentences = split_into_sentences(text)
    chunks = []

    # Combine sentences into chunks with a word limit
    while sentences:
        chunk = sentences.pop(0)
        while len(chunk.split()) < word_limit and sentences:
            chunk += ' ' + sentences.pop(0)
        chunks.append(chunk)
    
    return chunks


def multiple_choice_generator(text, n_questions=10):
    """
    Generate multiple-choice questions based on text chunks.

    :param text: input text
    :type text: str
    :param num_q: number of questions to generate, defaults to 10
    :type num_q: int, optional
    :return: list of generated questions
    :rtype: list[str]
    """

    quiz_content = []
    chunks = combine_sentences(text)
    random.shuffle(chunks) #Randomly select content
    # Generate multiple-choice questions from text chunks
    for i in range(n_questions*2):
        chunk = chunks[i % len(chunks)]
        tmp = generate_multiple_choice_question(chunk)  # Function to generate question
        print(tmp)
        quiz_content.append(tmp)
        if len(quiz_content) == n_questions:
            break

    print("Quiz content:", quiz_content)
    return quiz_content

##### For scrapping Wiki
def Scraping(url):
    article = Article(url)
    article.download()
    article.parse()
    res = article.text
    if  len(res)==0:
        return "Please enter a valid URL"  
    return res