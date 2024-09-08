import pandas as pd
from dash import html, dcc, Output, Input, callback, ctx
import plotly.express as px
import dash_bootstrap_components as dbc

''' ------------------------------------------------- Funzioni -------------------------------------------------'''

def read_cities_df():
    df_list = []
    for paese in capitali:
        df_list.append(pd.read_csv(f'{path_citta}\\2013_{paese}.csv', delimiter='; ', engine='python'))
    return df_list


def extract_cities():
    capitali_list = []
    for capitale in df_capitali.itertuples():
        capitali_list.append(f'{capitale[4].strip()}, {capitale[2].strip()}')
    return sorted(capitali_list)


@callback(
    Output('layout-corrente-città', 'children'),
    [Input('radio-input-città', 'value')]
)
def aggiorna_layout(valore_radio):
    if valore_radio == 2:
        return layout_citta()
    elif valore_radio == 1:
        return layout_annuale_citta()
    else:
        return html.Div(children=''' Pagina non Disponibile. ''')

@callback([
    Output('dropdown-input-citta', 'label'),
    Output('tabella-annuale-max', 'children'),
    Output('tabella-annuale-min', 'children'),
    Output('grafico-annuale', 'figure'),

    [Input("0", "n_clicks"), Input("1", "n_clicks")]
])
def aggiorna_grafico_annuale(temperatura, pioggia):
    if not ctx.triggered:
        return ['Temperatura', tabelle_annuali[0], tabelle_annuali[1], grafici_annuali[0]]
    else:
        button_id = int(ctx.triggered_id) if not None else 'Seleziona un\'analisi'

        if button_id == 0:
            return [value[0], tabelle_annuali[0], tabelle_annuali[1], grafici_annuali[0]]
        elif button_id == 1:
            return [value[1], tabelle_annuali[2], tabelle_annuali[3], grafici_annuali[1]]

def costruisci_grafici(valore):
    grafico_città = px.line(df_città[valore], x=df_città[valore]["month_rain"],
                            y=[df_città[valore]['monthly_rain_value'], df_città[valore]['monthly_temp_value']],
                            labels={'month_rain': 'Mese', 'variable': 'Valori medi giornalieri', 'value': 'Valore'},
                            markers=True,
                            title=f"Analisi Pioggia-Temperatura di {capitali[valore]}")

    nuovi_nomi = {'monthly_rain_value': 'Pioggia', 'monthly_temp_value': 'Temperatura'}
    grafico_città.for_each_trace(lambda t: t.update(name=nuovi_nomi[t.name],
                                                    legendgroup=nuovi_nomi[t.name],
                                                    hovertemplate=t.hovertemplate.replace(t.name, nuovi_nomi[t.name]))
                                 )

    mappa = px.choropleth(locations=[df_capitali['st'][valore]], locationmode="USA-states",
                          color_continuous_scale='Inferno', range_color=(0, 1), color=[0], scope="usa",
                          title=f"Stai visualizzando i dati relativi alla città di {capitali[valore]}")
    mappa.update_geos(
            visible=True, resolution=110, scope="usa",
            showsubunits=True, subunitcolor="Black", subunitwidth=0.1
        )
    mappa.update_layout(coloraxis_showscale=False)
    return [mappa, grafico_città]

def costruisci_tabelle(valore):
    rows_città = [
        html.Th('Giorno più piovoso',
                style={'backgroundColor': '#1a0933', 'border': '1px solid white', 'text-align': 'center',
                       'vertical-align': 'middle', 'height': '40px'}),
        html.Tr(html.Td(
            f"{df_città[valore]['rainest_day'].iloc[0]} {df_città[valore]['rainest_month'].iloc[0]}, {df_città[valore]['max_rain'].iloc[0]} mm",
            style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})),

        html.Th('Giorno meno piovoso',
                style={'backgroundColor': '#1a0933', 'border': '1px solid white', 'text-align': 'center',
                       'vertical-align': 'middle', 'height': '40px'}),
        html.Tr(html.Td(
            f"{df_città[valore]['less_rainy_day'].iloc[0]} {df_città[valore]['less_rainy_month'].iloc[0]}, {df_città[valore]['min_rain'].iloc[0]} mm",
            style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})),

        html.Th('Giornata più calda',
                style={'backgroundColor': '#1a0933', 'border': '1px solid white', 'text-align': 'center',
                       'vertical-align': 'middle', 'height': '40px'}),
        html.Tr(html.Td(
            f"{df_città[valore]['max_temp'].iloc[0]} °C, registrati a {df_città[valore]['hotter_month'].iloc[0]}",
            style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})),

        html.Th('Giornata più fredda',
                style={'backgroundColor': '#1a0933', 'border': '1px solid white', 'text-align': 'center',
                       'vertical-align': 'middle', 'height': '40px'}),
        html.Tr(html.Td(
            f"{df_città[valore]['min_temp'].iloc[0]} °C, registrati a {df_città[valore]['colder_month'].iloc[0]}",
            style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}))
    ]

    heads_città = [[html.Thead(rows_città[0])], [html.Thead(rows_città[2])], [html.Thead(rows_città[4])],
                   [html.Thead(rows_città[6])]]
    bodies_città = [[html.Thead(rows_città[1])], [html.Thead(rows_città[3])], [html.Thead(rows_città[5])],
                    [html.Thead(rows_città[7])]]

    tabelle_città = [
        dbc.Table(heads_città[0] + bodies_città[0]),
        dbc.Table(heads_città[1] + bodies_città[1]),
        dbc.Table(heads_città[2] + bodies_città[2]),
        dbc.Table(heads_città[3] + bodies_città[3])
    ]
    return tabelle_città # [tabelle_città[0], tabelle_città[1], tabelle_città[2], tabelle_città[3]]


@callback([
    Output('stato', 'figure'),
    Output('pioggia-temperatura', 'figure'),
    Output('più-piovoso', 'children'),
    Output('meno-piovoso', 'children'),
    Output('più-caldo', 'children'),
    Output('più-freddo', 'children'),

    [Input('select-città', "value")]
])
def aggiorna_grafico_città(valore):
    if not ctx.triggered:
        tabelle_default = costruisci_tabelle(0)
        mappa_default = costruisci_grafici(0)[0]
        grafico_default = costruisci_grafici(0)[1]
        return [mappa_default, grafico_default, tabelle_default[0], tabelle_default[1], tabelle_default[2], tabelle_default[3]]
    else:
        tabelle = costruisci_tabelle(int(valore))
        mappa = costruisci_grafici(int(valore))[0]
        grafico = costruisci_grafici(int(valore))[1]
        return [mappa, grafico, tabelle[0], tabelle[1], tabelle[2], tabelle[3]]

def layout_citta():
    return html.Div([
        html.Br(),
        select,
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(id='stato')),
            dbc.Col(dcc.Graph(id='pioggia-temperatura'))
        ]),
        html.Br(),
        dbc.Row([
            dbc.Col(id='più-piovoso'),
            dbc.Col(id='meno-piovoso'),
            dbc.Col(id='più-caldo'),
            dbc.Col(id='più-freddo'),
        ])
    ])


def layout_annuale_citta():
    return html.Div([
        html.Br(),
        dropdown,
        html.Br(),
        dbc.Row([
            dbc.Col([dcc.Graph(id='grafico-annuale')]),
            dbc.Col([
                dbc.Row([
                    dbc.Col(id='tabella-annuale-max'),
                    dbc.Col(id='tabella-annuale-min'),
                ])
            ]),
        ]),
    ])


def layout():
    return html.Div([
        html.Div(children='Dati sulle Capitali negli Stati Uniti nell\'anno 2013',
                 style={'textAlign': 'center', 'fontSize': '20px', 'margin-top': '25px',
                        'color': 'white', 'fontFamily': 'Verdana, sans-serif',
                        'textShadow': '0 0 8px #4c8a9e, 0 0 15px #4c8a9e, 0 0 20px #4c8a9e, 0 0 25px #4c8a9e'}),
        radio,
        html.Div(id='layout-corrente-città')
    ])


''' ------------------------------------------------- Variabili -------------------------------------------------'''

column_names = ['wban', 'state', 'st', 'country', 'latitude', 'longitude']

# path_citta = '..\\..\\backend\\risultati_citta'
# path_capitali = '..\\..\\backend\\dataset\\QCLCD\\wban_stato_capitale.csv'

path_citta = 'pathTo\\yourBackendResultCity'
path_capitali = 'pathTo\\dataset\\wban_stato_capitale.csv'

# lettura dei dataframe da file .csv
df_capitali = pd.read_csv(path_capitali, delimiter=', ', engine='python', names=column_names).sort_values(by='country',
                                                                                                          ignore_index=True)
capitali = extract_cities()
df_annuale = pd.read_csv(f'{path_citta}\\2013_Citta.csv', delimiter='; ', engine='python')
df_città = read_cities_df()
df_annuale_temp_ordinato = df_annuale.sort_values(by='temp_country_state', ignore_index=True)
df_annuale_rain_ordinato = df_annuale.sort_values(by='rain_country_state', ignore_index=True)
value = ['Temperatura', 'Pioggia']

''' ------------------------------------------------- Componenti -------------------------------------------------'''

radio = dbc.Row(
    dbc.RadioItems(
        options=[
            {"label": "Tutte le Città", "value": 1},
            {"label": "Singola Città", "value": 2},
        ],
        id="radio-input-città",
        style={"margin-left": "60px", "margin-top": "-25px"},
        value=1,
        inline=True,
    ),
)

options = [{'label': citta, 'value': index} for index, citta in enumerate(capitali)]
select = dbc.Select(
    id="select-città",
    options= options,
    value = capitali[0],
    style={'width': '244.2px', 'height': '36px', 'margin-top': '-55px', 'margin-left': '1245px', 'backgroundColor': '#6f42c1', 'color':'white'}
)

grafici_annuali = [
    px.choropleth(scope = 'usa', locations = [el for el in df_capitali['st']], range_color=(-2, 26),
                  locationmode = "USA-states", labels={'color': 'Temperatura °C', 'locations': 'Stato'},
                  color_continuous_scale='RdYlBu_r', color=[el for el in df_annuale_temp_ordinato['temp']],
                  title='Analisi Medie Temperature negli USA nel 2013'),

    px.choropleth(scope='usa', locations=[el for el in df_capitali['st']], range_color=(0, 6),
                  locationmode="USA-states", labels={'color': 'Pioggia mm', 'locations': 'Stato'},
                  color_continuous_scale='Blues', color=[el for el in df_annuale_rain_ordinato['rain']],
                  title='Analisi Medie Piogge negli USA nel 2013')
]

rows_city = [
    html.Th('Top 10 delle città più calde', colSpan=2,
            style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center',
                   'border': '1px solid white',
                   'height': '40px', 'vertical-align': 'middle'}),
    [html.Tr([html.Td(df_annuale['temp_country_state'].iloc[i],
                      style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
              html.Td(f"{df_annuale['temp'].iloc[i]} °C",
                      style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]) for
     i in range(10)],
    html.Th('Top 10 delle città più fredde', colSpan=2,
            style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center',
                   'border': '1px solid white',
                   'height': '40px', 'vertical-align': 'middle'}),
    [html.Tr([html.Td(df_annuale['temp_country_state'].iloc[-i - 1],
                      style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
              html.Td(f"{df_annuale['temp'].iloc[-i - 1]} °C",
                      style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]) for
     i in range(10)],
    html.Th('Top 10 delle città più piovose', colSpan=2,
            style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center',
                   'border': '1px solid white',
                   'height': '40px', 'vertical-align': 'middle'}),
    [html.Tr([html.Td(df_annuale['rain_country_state'].iloc[i],
                      style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
              html.Td(f"{df_annuale['rain'].iloc[i]} mm",
                      style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]) for
     i in range(10)],
    html.Th('Top 10 delle città meno piovose', colSpan=2,
            style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center',
                   'border': '1px solid white',
                   'height': '40px', 'vertical-align': 'middle'}),
    [html.Tr([html.Td(df_annuale['rain_country_state'].iloc[-i - 1],
                      style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
              html.Td(f"{df_annuale['rain'].iloc[-i - 1]} mm",
                      style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]) for
     i in range(10)],
]

heads_city = [[html.Thead([rows_city[0]])], [html.Thead([rows_city[2]])], [html.Thead([rows_city[4]])],
              [html.Thead([rows_city[6]])]]
bodies_city = [[html.Tbody([rows_city[1][i]]) for i in range(len(rows_city[1]))],
               [html.Tbody([rows_city[3][i]]) for i in range(len(rows_city[3]))],
               [html.Tbody([rows_city[5][i]]) for i in range(len(rows_city[5]))],
               [html.Tbody([rows_city[7][i]]) for i in range(len(rows_city[7]))], ]

tabelle_annuali = [
    dbc.Table(
        heads_city[0] + bodies_city[0],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    ),

    dbc.Table(
        heads_city[1] + bodies_city[1],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    ),

    dbc.Table(
        heads_city[2] + bodies_city[2],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    ),
    dbc.Table(
        heads_city[3] + bodies_city[3],
        bordered=True,
        hover=True,
        responsive=True,
        striped=True
    ),
]

dropdown = dbc.DropdownMenu(
    [dbc.DropdownMenuItem(valore, id=str(x)) for x, valore in enumerate(value)],
    id='dropdown-input-citta',
    label='Seleziona un\'analisi',
    style={'margin-top': '-55px', 'margin-left': '1275px'},
)
