# Packages
import dash_bootstrap_components as dbc
from dash import dcc, html
import base64
from dash.dependencies import Input, Output  # correction here
from dash import Dash
from pages import tab1, tab2


# Define a function
app = Dash(
    "Quizify",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
)
app.title = "Quizify"
server = app.server

def encode_image(image_file):
    """Standardize the image format
    Args:
        image_file (str): image directory
    Returns:
        str: encoded image file
    """
    encoded = base64.b64encode(open(image_file, "rb").read())
    return "data:image/png;base64,{}".format(encoded.decode())


logo = html.Img(
    id="logo",
    src=encode_image("img/quizify.png"),
)
logo_alt = html.Img(
    id="logo_alt",
    src=encode_image("img/quizify_short.png"),
)
# Layout
nav_bar = html.Div(
    [
        logo,
        logo_alt,
        html.A(html.Button('Text', id = 'text-nav', className="nav-active"), href = '/'),
        html.A(html.Button('Wiki', id = 'url-nav', className="nav-inactive"), href = '/url-composer')
    ],
    id="nav-bar",
)
app.layout = html.Div(
    [
        nav_bar,
        dcc.Location(id="url", refresh=False),
        html.Div(id="page-content", children=[], className="container-fluid"),
    ]
)

@app.callback(
        [Output("page-content", "children"), Output("text-nav", "className"), Output("url-nav", "className")], 
        Input("url", "pathname")
        )
def display_page(pathname):
    if pathname == "/":
        return tab1.layout, "nav-active", "nav-inactive"  # should return the layout attribute
    elif pathname == "/url-composer":
        return tab2.layout, "nav-inactive", "nav-active"  # should return the layout attribute
    else: 
        return "404", "", ""

if __name__ == "__main__":
    app.run_server(
        debug = True
        )
