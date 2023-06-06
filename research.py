import dash_bootstrap_components as dbc
from dash import dcc, html
from dash import Dash, dcc, html, Input, Output, callback, State, no_update
import time

app = Dash(__name__)

app.layout = dcc.Loading(
    id="loading",
    type="circle",
    children=[
        html.Div([
            dcc.Input(id="input"),
            html.Div(id="output"),
            # Your other components go here...
        ])
    ]
)

@app.callback(Output("output", "children"), [Input("input", "value")])
def update_output(value):
    # Emulate a long computation
    time.sleep(2)
    return 'You have entered "{}"'.format(value)


if __name__ == "__main__":
    app.run_server(debug=True)
