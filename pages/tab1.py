# Packages
import dash_bootstrap_components as dbc
from dash import dcc, html
import base64, json
from dash import Dash, dcc, html, Input, Output, callback, State, no_update
import plotly.graph_objs as go
import pandas as pd
from utility import *
import config

text = config.text_1
example = config.example_1 

layout = dbc.Container(
    [
        html.Div([
            html.Div("Insert your text", id="text-input-title"),
            dcc.Textarea(value = text, id="text-input", maxLength = 10000),
            html.Div([html.Label("Number of questions: ", id = "question-num-label"), 
                      dcc.Input(id="question-num-input",type="number",value=10, min=1, max=15)]),
            dbc.Button("Generate Quiz", id="generate-btn", className = "btn"),
            ],
            id = "input-group"
            ),
        dcc.Store(id='save-answer', data = {}),
        html.Div(id='save-answer-display', style={'display': 'none'}), #TEST
        dbc.Spinner(dcc.Store(data = example, id="quiz-content"), color = "#03738C"),
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

@callback(
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
        Input("quiz-content", 'data'),
        Input('save-answer', 'data')
    ],
)
def update_question_output(next_clicks, prev_clicks, quiz_questions, save_answer):
    question_index = (next_clicks - prev_clicks) % len(quiz_questions)
    #Logic for button
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
    options_div = [{'label': f"{option}", 'value': option} for option in options]
    value =  save_answer[question] if question in save_answer else None

    return question_number, question, options_div, value, prev_btn_style, next_btn_style, submit_btn_style

@callback(
    [
        Output("quiz-content", "data"), 
        Output("save-answer", "data", allow_duplicate=True)
    ],
    Input("generate-btn", "n_clicks"),
    [
        State("question-num-input", "value"),
        State("text-input", "value")
    ],
    prevent_initial_call = True,
)
def generate_question(n_clicks, n_question, text):
    quiz_content = multiple_choice_generator(text, n_question)
    # print(quiz_content)

    return quiz_content, {}

@callback(
        [
            Output('save-answer', 'data', allow_duplicate=True),
            Output('save-answer-display', 'children'),
        ],
        [
        Input("quiz-content", "data"),
        Input("radio-answers", "value"),
        Input("next-button", "n_clicks"),
        Input("previous-button", "n_clicks"),
        Input('save-answer', 'data')
        ],
    prevent_initial_call = True,
)
def display_your_selection(quiz_content, answer, next_clicks, prev_clicks, save_answer):
    question_index = next_clicks - prev_clicks
    # print(quiz_content)

    quiz_content = eval(str(quiz_content))
    print('Save answer', save_answer)
    # save_answer = save_answer)
    save_answer[quiz_content[question_index]['question']] = answer 
    if answer:
        return save_answer, str(save_answer)
    else:
        return no_update, no_update


#Display "you done" when hit submit button
@callback(
    [
    Output("question-card", "style"),
    Output("analysis-card", "style"),
    Output("graph", "figure"),
    Output("correction", "children"),
    ],
    Input("submit-button", "n_clicks"),
    [
        State('quiz-content', 'data'),
        State('save-answer', "data")
    ],
    prevent_initial_call = True,
)
def update_submit(submit_clicks, quiz_content, save_answer):
    if submit_clicks:
        #Load submission
        result = pd.DataFrame({})
        result['question'] = [q['question'] for q in quiz_content] 
        result['answer'] = [q['answer'] for q in quiz_content] 
        result['user_answer'] = [save_answer[q['question']] if q['question'] in save_answer else "you skipped!" for q in quiz_content]
        result['is_correct'] = result['answer']==result['user_answer']

        graph = go.Figure(data=[go.Pie(
                labels=['Correct', 'Incorrect'],
                values=[result['is_correct'].sum(), len(result)-result['is_correct'].sum()],
                hole=.6
        )])

        graph.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                  marker=dict(colors=["#00a699", "#ff0018b0"], line=dict(color='#000000', width=1)))
        
        ans = []
        for i in range(len(result)):
            q, a, c = result.iloc[i].to_dict()["question"], result.iloc[i].to_dict()["user_answer"], result.iloc[i].to_dict()["answer"]
            ans.append(html.Div(f"Question {i+1}: {q}", id = "solution-question"))
            ans.append(html.Div(f"Your answer: {a}", id = "solution-answer", 
                                style = {"color": "red"} if not result.iloc[i].to_dict()['is_correct'] else {"color": "green"}))
            ans.append(html.Div(f"Correct answer: {c}", id = "solution-correct"))
            ans.append(html.Hr())
        
        return {"display": "none"}, {"display": "flex"}, graph, html.Div(ans)
    else:
        return no_update
    
@callback(
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
    Output("save-answer", 'data'),
    Output("question-card", "style", allow_duplicate=True),
    Output("analysis-card", "style", allow_duplicate=True),
    ],
    [Input("retake-btn", "n_clicks"), 
     Input("generate-btn", "n_clicks"),
     Input("quiz-content", 'data'),
     ],
    prevent_initial_call = True,
)
def retake(retake_click, generate_click, quiz_questions):
    if retake_click or generate_click:
        question_index = 0
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
        options_div = [{'label': f"{option}", 'value': option} for option in options]
        value =  None

        return question_number, question, options_div, value, prev_btn_style, next_btn_style, submit_btn_style, 0, 0, {}, {"display": "block"}, {"display": "none"}
    else:
        return no_update

