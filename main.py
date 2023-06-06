# Packages
import dash_bootstrap_components as dbc
from dash import dcc, html
import base64, json
from dash import Dash, dcc, html, Input, Output, callback, State, no_update
import plotly.graph_objs as go
import dash_bootstrap_components as dbc
import pandas as pd
from utility import *

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

example  = [{'question': 'What percentage of the Earth’s land area does Asia cover?', 'options': ['20 percent', '30 percent', '40 percent', '50 percent'], 'answer': '30 percent'}, {'question': 'What percentage of the world’s population does Asia have?', 'options': ['30 percent', '40 percent', '50 percent', '60 percent'], 'answer': '60 percent'}, {'question': 'Which continent occupies the western portion of the Eurasian supercontinent?', 'options': ['Europe', 'North America', 'South America', 'Africa'], 'answer': 'Europe'}, {'question': 'What is the debated border between Asia and Europe?', 'options': ['The Ural Mountains', 'The Himalayan Mountains', 'The Rocky Mountains', 'The Appalachian Mountains'], 'answer': 'The Ural Mountains'}, {'question': 'Which oceans border Asia?', 'options': ['Atlantic and Indian', 'Pacific and Atlantic', 'Pacific and Indian', 'Arctic and Antarctic'], 'answer': 'Arctic, Pacific, and Indian'}, {'question': 'How many major physical regions can Asia be divided into?', 'options': ['3', '4', '5', '6'], 'answer': '5'}, {'question': 'Which physical region of Asia includes freshwater environments?', 'options': ['Mountain systems', 'Plateaus', 'Plains, steppes, and deserts', 'Freshwater environments'], 'answer': 'Freshwater environments'}, {'question': 'Which physical region of Asia includes saltwater environments?', 'options': ['Mountain systems', 'Plateaus', 'Saltwater environments', 'Plains, steppes, and deserts'], 'answer': 'Saltwater environments'}, {'question': 'What is the western border of Asia?', 'options': ['Ural Mountains, Caucasus Mountains, and Caspian and Black Seas', 'Himalayan Mountains', 'Rocky Mountains', 'Appalachian Mountains'], 'answer': 'Ural Mountains, Caucasus Mountains, and Caspian and Black Seas'}, {'question': 'What is the eastern portion of the Eurasian supercontinent?', 'options': ['Europe', 'Asia', 'North America', 'South America'], 'answer': 'Asia'}]

text = """
Asia is the largest of the world’s continents, covering approximately 30 percent of the Earth’s land area. It is also the world’s most populous continent, with roughly 60 percent of the total population.

Asia makes up the eastern portion of the Eurasian supercontinent; Europe occupies the western portion. The border between the two continents is debated. However, most geographers define Asia’s western border as an indirect line that follows the Ural Mountains, the Caucasus Mountains, and the Caspian and Black Seas. Asia is bordered by the Arctic, Pacific, and Indian Oceans.

Asia’s physical geography, environment and resources, and human geography can be considered separately.

Asia can be divided into five major physical regions: mountain systems; plateaus; plains, steppes, and deserts; freshwater environments; and saltwater environments.
"""
def encode_image(image_file):
    """Standardize the image format

    Args:
        image_file (str): image directory

    Returns:
        str: encoded image file
    """
    encoded = base64.b64encode(open(image_file, "rb").read())
    return "data:image/png;base64,{}".format(encoded.decode())

logo = html.Img(id="logo",
    src=encode_image("img/quizify.png"),
    style={
        "verticalAlign": "center",
        "align": "center",
        "padding": "0px",
        "height": "3.5rem",
    },
)

navbar = html.Div(logo ,id = "nav-bar")

content = dbc.Container(
    [
        html.Div([
            html.Div("Insert your text", id="text-input-title"),
            dcc.Textarea(value = text, id="text-input"),
            html.Div([html.Label("Number of questions: ", id = "question-num-label"), 
                      dcc.Input(id="question-num-input",type="number",value=10, min=1, max=15)]),
            dbc.Button("Generate Quiz", id="generate-btn", className = "btn", style = {"width": "200px", "align": "center"}),
            ],
            id = "input-group"
            ),

        dcc.Loading(html.Div(children=str(example), id="quiz-content", style={"display": "none"})),
        html.Br(),

        #Question card
        html.Div([
                    html.Div(id="question-number-output"),
                    html.Div(id="question-output"),
                    dcc.RadioItems(id = "radio-answers"),
                    html.Div(
                        [
                            dbc.Button("Previous", className="btn" , id="previous-button", n_clicks=0,),
                            dbc.Button("Next", className="btn", id="next-button", n_clicks=0,),
                            dbc.Button("Submit", className="btn", id="submit-button", n_clicks=0,
                                       style={"display": "none"}),
                        ],
                        style={"display": "flex", "justify-content": "space-between"},
                        id = "button-group"
                    ),
                    html.Div(id = "answer")
                ],
            id="question-card",
        ),
        #Analysis
        dbc.Card(
            dbc.CardBody(
                [
                    dcc.Graph(id = "graph"),
                    html.Div(id = "correction"),
                    dbc.Button("Retake", color="primary", className="btn", id="retake-btn", n_clicks=0,),
                ],
                id = "analysis-card-body"
            ),
            style={"display": "none", "margin": "auto"},
            id = "analysis-card"
        ),
    ],
    style={"display": "block"}
)


# App layout
app.layout = html.Div([navbar, content])
    
def construct_question_components(question_index, quiz_questions):
    """
    This function constructs the required components for displaying a question 
    based on the given index and returns them.
    """
    if (question_index == len(quiz_questions)-1) and (len(quiz_questions)>1):
        prev_btn_style = {"display": "block"}
        next_btn_style = {"display": "none"}
        submit_btn_style = {"display": "block"}
    elif question_index == 0:
        prev_btn_style = {"display": "none"}
        next_btn_style = {"display": "flex", 'margin-left': 'auto'}
        submit_btn_style = {"display": "none"}
    else:
        prev_btn_style = {"display": "block"}
        next_btn_style = {"display": "block"}
        submit_btn_style = {"display": "none"}

    question_number = f"Question {question_index + 1}:"
    question = quiz_questions[question_index]["question"]
    options = quiz_questions[question_index]["options"]

    #Load log
    log = pd.read_csv("log.csv")
    answer = log.loc[question_index, "user_answer"]

    options = [{'label': f"{option}", 'value': option} for option in options]
    value = answer if answer else None
    return question_number, question, options, value, prev_btn_style, next_btn_style, submit_btn_style

@app.callback(
    [
        Output("question-number-output", "children"),
        Output("question-output", "children"),
        Output("radio-answers", "options"),
        Output("radio-answers", "value"),
        Output("previous-button", "style"),
        Output("next-button", "style"),
        Output("submit-button", "style"),
    ],
    [
        Input("next-button", "n_clicks"),
        Input("previous-button", "n_clicks"),
        Input("quiz-content", 'children')
    ],
)
def update_question_output(next_clicks, prev_clicks, quiz_questions):
    quiz_questions = eval(quiz_questions)
    question_index = (next_clicks - prev_clicks) % len(quiz_questions)
    return construct_question_components(question_index, quiz_questions)

@app.callback(
    Output("quiz-content", "children"),
    Input("generate-btn", "n_clicks"),
    [
        State("question-num-input", "value"),
        State("text-input", "value")
    ],
    prevent_initial_call = True,
)
def generate_question(n_clicks, n_question, text):
    res = multiple_choice_generator(text, n_question)
    print(res)
    print(n_question)

    df = pd.DataFrame(res)
    df["user_answer"] = [""] * len(df)
    df.to_csv("log.csv",index = False)

    return str(res)

@app.callback(
        Output("answer", "children"),
        [Input("radio-answers", "value"),
         Input("next-button", "n_clicks"),
        Input("previous-button", "n_clicks")]
)
def update_question_output(answer, next_clicks, prev_clicks):
    question_index = next_clicks - prev_clicks
    log = pd.read_csv("log.csv")
    log.loc[question_index, "user_answer"] = answer
    log.to_csv("log.csv", index = False)
    if answer:
        return "Your answer: " + answer
    else:
        return no_update


#Display "you done" when hit submit button
@app.callback(
    [
    Output("question-card", "style"),
    Output("analysis-card", "style"),
    Output("graph", "figure"),
    Output("correction", "children"),
    ],
    Input("submit-button", "n_clicks"),
    prevent_initial_call = True,
)
def update_submit(submit_clicks):
    if submit_clicks:
        #Load submission
        log = pd.read_csv("log.csv")
        log["correct"] = log["user_answer"] == log["answer"]
        log["user_answer"].fillna("you skipped!", inplace = True)
        result_dict = {}
        result_dict["correct"] = log["correct"].sum()
        result_dict["wrong"] = len(log) - result_dict["correct"]
        graph = go.Figure(data=[go.Pie(
                labels=list(result_dict.keys()),
                values=list(result_dict.values(),),
                hole=.6
        )])
        graph.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=["#00a699", "#ff0018b0"], line=dict(color='#000000', width=1)))
        ans = []
        for i in range(len(log)):
            q, a, c = log.iloc[i].to_dict()["question"], log.iloc[i].to_dict()["user_answer"], log.iloc[i].to_dict()["answer"]
            ans.append(html.Div(f"Question {i+1}: {q}", id = "solution-question"))
            ans.append(html.Div(f"Your answer: {a}", id = "solution-answer", 
                                style = {"color": "red"} if not log.iloc[i].to_dict()['correct'] else {"color": "green"}))
            ans.append(html.Div(f"Correct answer: {c}", id = "solution-correct"))
            ans.append(html.Hr())
        
        return {"display": "none"}, {"display": "flex"}, graph, html.Div(ans)
    else:
        return no_update
    
@app.callback(
    [
    Output("question-number-output", "children", allow_duplicate=True),
    Output("question-output", "children", allow_duplicate=True),
    Output("radio-answers", "options", allow_duplicate=True),
    Output("radio-answers", "value", allow_duplicate=True),
    Output("previous-button", "style", allow_duplicate=True),
    Output("next-button", "style", allow_duplicate=True),
    Output("submit-button", "style", allow_duplicate=True),
    Output("previous-button", "n_clicks"),
    Output("next-button", "n_clicks"),
    Output("question-card", "style", allow_duplicate=True),
    Output("analysis-card", "style", allow_duplicate=True),
    ],
    [Input("retake-btn", "n_clicks"), 
     Input("generate-btn", "n_clicks"),
     Input("quiz-content", 'children')],
    prevent_initial_call = True,
)
def retake(retake_click, generate_click, quiz_questions):
    quiz_questions = eval(quiz_questions)
    if retake_click or generate_click:
        # Reset the log file
        if len(quiz_questions)!=0:
            df = pd.DataFrame(quiz_questions )
            df["user_answer"] = [""] * len(df)
            df.to_csv("log.csv",index = False)

        question_number, question, options, value, prev_btn_style, next_btn_style, submit_btn_style = construct_question_components(0, quiz_questions)
        return (question_number, question, options, value, prev_btn_style, 
                next_btn_style, submit_btn_style, 0, 0, 
                {"display": "block"}, {"display": "none"})
    else:
        return no_update

if __name__ == "__main__":
    app.run_server(debug=True)
# if __name__ == "__main__":
#     app.run_server(host="0.0.0.0", port=8050)
