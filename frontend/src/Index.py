from dash import dcc, html, dash, Input, Output
from pages import Pioggia, Temperatura, Città, Regressione
import dash_bootstrap_components as dbc
''' ------------------------------------------------- Inizializzazione app -------------------------------------------------'''

app = dash.Dash(__name__, suppress_callback_exceptions=True,
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}],
                external_stylesheets=[dbc.themes.VAPOR]
                )

''' ------------------------------------------------- Componenti -------------------------------------------------'''

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Home", href="/"),
                    style={"margin-left": "-246.5%"}),
        dbc.NavItem(dbc.NavLink("Capitali", href='/pages/citta')),
        dbc.NavItem(dbc.NavLink("Pioggia", href='/pages/pioggia')),
        dbc.NavItem(dbc.NavLink("Temperatura", href='/pages/temperatura')),
        dbc.NavItem(dbc.NavLink("Regressione", href='/pages/regressione'))
    ],
    color="dark",
    dark=True
)

description = html.Div(className='description', children="Applicazione Web "
                                                         "per l'analisi di dati meteorologici "
                                                         "delle capitali degli Stati Uniti dell'anno 2013")

credits = html.Div(className='credits', children="Progetto a cura di: Carreri Domenico, Cavallo Giuseppe, Mandarino Francesco")

app.layout = html.Div(children=[
        html.Link(
            rel='stylesheet',
            href='/static/style.css',
        ),
        dcc.Location(id='url', refresh=False),
        navbar,
        html.Div(id='page-content', children = [])
    ])


home = html.Div(children=[
    html.Link(
        rel='stylesheet',
        href='/static/style.css',
    ),
    html.Div(className='title', children='WeatherAnalytics', style={'textAlign': 'center'}),
    description,
    credits
])

''' ------------------------------------------------- Funzioni -------------------------------------------------'''

@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/pages/pioggia':
        return Pioggia.layout()
    if pathname == '/pages/temperatura':
        return Temperatura.layout()
    if pathname == '/pages/citta':
        return Città.layout()
    if pathname == '/pages/regressione':
        return Regressione.layout()
    else:
        return home

''' ------------------------------------------------- Main ------------------------------------------------- '''

if __name__ == '__main__':
    app.run_server()