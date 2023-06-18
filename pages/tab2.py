# Packages
import dash_bootstrap_components as dbc
from dash import dcc, html
import base64, json
from dash import Dash, dcc, html, Input, Output, callback, State, no_update
import plotly.graph_objs as go
import pandas as pd
from utility import *
import config

text = config.text_2
example = config.example_2

layout = dbc.Container(
    [
        # URL
        html.Div(
            [
                html.Div("Insert a Wikiperdia URL", id="url-input-title"),
                dcc.Input(
                    value="https://en.wikipedia.org/wiki/Databricks", id="url-input"
                ),
                dbc.Button("Extract", id="extract-btn", className="btn"),
            ],
            id="input-group-2",
        ),
        html.Br(),
        # Text result
        html.Div(
            [
                html.Div("Content", id="content-title"),
                dcc.Textarea(value = text, id="url-content-input", maxLength = 10000),
                html.Div(
                    [
                        html.Label("Number of questions: ", id="question-num-label-2"),
                        dcc.Input(
                            id="question-num-input-2",
                            type="number",
                            value=6,
                            min=1,
                            max=15,
                        ),
                    ]
                ),
                dbc.Button("Generate Quiz", id="generate-btn-2", className="btn"),
            ],
            id="input-group-3",
        ),
        dcc.Store(id="save-answer-2", data={}),
        html.Div(id="save-answer-display-2",style={'display': 'none'}), #TEST
        dbc.Spinner(dcc.Store(data=example, id="quiz-content-2"), color = "#03738C"),
        html.Br(),

        #Question card
        html.Div([
        html.Div(id="question-number-output-2"),
                     html.Div(id="question-output-2"),
                     dcc.RadioItems(id = "radio-answers-2"),
                     html.Div(
                         [
                             dbc.Button("Previous", className="btn quiz-btn" , id="previous-button-2", n_clicks=0,),
                             dbc.Button("Next", className="btn quiz-btn", id="next-button-2", n_clicks=0,),
                             dbc.Button("Submit", className="btn quiz-btn", id="submit-button-2", n_clicks=0,
                                        style={"display": "none"}),
                         ],
                         style={"display": "flex", "justify-content": "space-between"},
                     ),
                     html.Div(id = "answer-2")
                 ],
             id="question-card-2",
         ),
        
        #Analysis
        dbc.Card(
             dbc.CardBody(
                 [
                     dcc.Graph(id = "graph-2"),
                     html.Div(id = "correction-2"),
                     dbc.Button("Retake", color="primary", className="btn quiz-btn", id="retake-btn-2", n_clicks=0,),
                 ],
                 id = "analysis-card-body-2"
             ),
             style={"display": "none", "margin": "auto"},
             id = "analysis-card-2"
        ),
    ],
    style={"display": "block"},
)


@callback(
    Output("url-content-input", "value"),
    Input("extract-btn", "n_clicks"),
    State("url-input", "value"),
)
def update_output(n_clicks, url):
    if n_clicks and url:
        content = Scraping(url) 
        return content[:5000]
    return no_update


@callback(
    [
        Output("question-number-output-2", "children"),
        Output("question-output-2", "children"),
        Output("radio-answers-2", "options"),
        Output("radio-answers-2", "value"),
        Output("previous-button-2", "style"),
        Output("next-button-2", "style"),
        Output("submit-button-2", "style"),
    ],
    [
        Input("next-button-2", "n_clicks"),
        Input("previous-button-2", "n_clicks"),
        Input("quiz-content-2", 'data'),
        Input('save-answer-2', 'data')
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
        Output("quiz-content-2", "data"), 
        Output("save-answer-2", "data", allow_duplicate=True)
    ],
    Input("generate-btn-2", "n_clicks"),
    [
        State("question-num-input-2", "value"),
        State("url-content-input", "value")
    ],
    prevent_initial_call = True,
)
def generate_question(n_clicks, n_question, text):
    quiz_content = multiple_choice_generator(text, n_question)
    # print(quiz_content)

    return quiz_content, {}

@callback(
        [
            Output('save-answer-2', 'data', allow_duplicate=True),
            Output('save-answer-display-2', 'children'),
        ],
        [
        Input("quiz-content-2", "data"),
        Input("radio-answers-2", "value"),
        Input("next-button-2", "n_clicks"),
        Input("previous-button-2", "n_clicks"),
        Input('save-answer-2', 'data')
        ],
    prevent_initial_call = True,
)
def display_your_selection(quiz_content, answer, next_clicks, prev_clicks, save_answer):
    question_index = next_clicks - prev_clicks
    # print(quiz_content)
    save_answer[quiz_content[question_index]['question']] = answer 
    if answer:
        return save_answer, str(save_answer)
    else:
        return no_update, no_update


#Display "you done" when hit submit button
@callback(
    [
    Output("question-card-2", "style"),
    Output("analysis-card-2", "style"),
    Output("graph-2", "figure"),
    Output("correction-2", "children"),
    ],
    Input("submit-button-2", "n_clicks"),
    [
        State('quiz-content-2', 'data'),
        State('save-answer-2', "data")
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
    Output("question-number-output-2", "children", allow_duplicate=True),
    Output("question-output-2", "children", allow_duplicate=True),
    Output("radio-answers-2", "options", allow_duplicate=True),
    Output("radio-answers-2", "value", allow_duplicate=True),
    Output("previous-button-2", "style", allow_duplicate=True),
    Output("next-button-2", "style", allow_duplicate=True),
    Output("submit-button-2", "style", allow_duplicate=True),
    Output("previous-button-2", "n_clicks"),
    Output("next-button-2", "n_clicks"),
    Output("save-answer-2", 'data'),
    Output("question-card-2", "style", allow_duplicate=True),
    Output("analysis-card-2", "style", allow_duplicate=True),
    ],
    [Input("retake-btn-2", "n_clicks"), 
     Input("generate-btn-2", "n_clicks"),
     Input("quiz-content-2", 'data'),
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