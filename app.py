from dash import Dash, html
import dash_bootstrap_components as dbc

FONT_AWESOME = ["https://use.fontawesome.com/releases/v5.10.2/css/all.css"]

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, FONT_AWESOME], suppress_callback_exceptions = True)

app.layout = [html.Div(children='Hello World')]
app.title = "Meu Dashboard"
server = app.server