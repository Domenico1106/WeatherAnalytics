from dash import html, dcc, Output, Input, callback, ctx
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc

'''------------------------------------------------- Funzioni -------------------------------------------------'''

def costruisci_tabella(button_id):
    rows_pioggia = [
        html.Th('Giorno più piovoso',
                style={'backgroundColor': '#1a0933', 'border': '1px solid white', 'text-align': 'center',
                       'vertical-align': 'middle', 'height': '40px'}, colSpan = 2),
        html.Tr([html.Td(pioggia_giornaliera[button_id]['rainiest_country_state'].iloc[0], style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(
                     f"{int(pioggia_giornaliera[button_id]['rainiest_day'].iloc[0])} {pioggia_giornaliera[button_id]['rainiest_month'].iloc[0]}, {pioggia_giornaliera[button_id]['rainiest_value'].iloc[0]} mm",
                     style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})
                 ]),
        html.Th('Giorno meno piovoso',
                style={'backgroundColor': '#1a0933', 'border': '1px solid white', 'text-align': 'center',
                       'vertical-align': 'middle', 'height': '40px'}, colSpan = 2),
        html.Tr([html.Td(pioggia_giornaliera[button_id]['less_rainy_country_state'].iloc[0], style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(
                     f"{int(pioggia_giornaliera[button_id]['less_rainy_day'].iloc[0])} {pioggia_giornaliera[button_id]['less_rainy_month'].iloc[0]}, {pioggia_giornaliera[button_id]['less_rainy_value'].iloc[0]} mm",
                     style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})
                 ])

    ]
    heads_pioggia = [[html.Thead(rows_pioggia[0])], [html.Thead(rows_pioggia[2])]]
    bodies_pioggia = [[html.Thead(rows_pioggia[1])], [html.Thead(rows_pioggia[3])]]
    tabelle_pioggia = [
        dbc.Table(heads_pioggia[0] + bodies_pioggia[0]),
        dbc.Table(heads_pioggia[1] + bodies_pioggia[1])
    ]

    return [tabelle_pioggia[1], tabelle_pioggia[0]]


@callback([
    Output('dropdown-input', 'label'),
    Output('tabella-mensile-meno-piovosa', 'children'),
    Output('tabella-mensile-più-piovosa', 'children'),
    Output('grafico-mensile', 'figure'),
    [Input("0", "n_clicks"), Input("1", "n_clicks"),
     Input("2", "n_clicks"), Input("3", "n_clicks"),
     Input("4", "n_clicks"), Input("5", "n_clicks"),
     Input("6", "n_clicks"), Input("7", "n_clicks"),
     Input("8", "n_clicks"), Input("9", "n_clicks"),
     Input("10", "n_clicks"), Input("11", "n_clicks"),
     ],
])
def aggiorna_grafico_mensile(gennaio, febbraio, marzo, aprile, maggio, giugno, luglio, agosto, settembre, ottobre,
                             novembre, dicembre):
    if not ctx.triggered:
        grafico_default = px.scatter_geo(df_mensili_ordinati[0],
                                         title='Pioggia media giornaliera nelle capitali degli Stati Uniti a Gennaio',
                                         scope='usa', lat='latitude', lon='longitude',
                                         hover_name="country_state", size='rain', color='country_state', labels={'country_state': 'Città'}
                                         )
        grafico_default.update_geos(
            visible=True, resolution=110, scope="usa",
            showsubunits=True, subunitcolor="Black", subunitwidth=0.1
        )
        tabella_default_meno_piovosa = costruisci_tabella(0)[0]
        tabella_default_piu_piovosa = costruisci_tabella(0)[1]
        return ["Gennaio", tabella_default_meno_piovosa, tabella_default_piu_piovosa, grafico_default]
    else:

        button_id = int(ctx.triggered_id) if not None else 'Seleziona un mese'
        grafico = px.scatter_geo(df_mensili_ordinati[button_id],
                                 title='Pioggia media giornaliera nelle capitali degli Stati Uniti a ' + mesi[
                                     button_id], scope='usa', lat='latitude', lon='longitude',
                                 hover_name="country_state", size='rain', color='country_state', labels={'country_state': 'Città'})
        grafico.update_geos(
            visible=True, resolution=110, scope="usa",
            showsubunits=True, subunitcolor="Black", subunitwidth=0.1
        )

        tabella_meno_piovosa = costruisci_tabella(button_id)[0]
        tabella_piu_piovosa = costruisci_tabella(button_id)[1]
        return [mesi[button_id], tabella_meno_piovosa, tabella_piu_piovosa, grafico]


def read_monthly_df():
    df_list = []
    for mese in mesi:
        df_list.append(pd.read_csv(f'{path_piogge}\\2013_{mese}_Pioggia.csv', delimiter='; ', engine='python'))
    return df_list


@callback(
    Output('layout-corrente', 'children'),
    [Input('radio_temp-input', 'value')]
)
def aggiorna_layout(valore_radio):
    if valore_radio == 2:
        return layout_mensile()
    elif valore_radio == 1:
        return layout_annuale()
    else:
        return html.Div(children=''' Pagina non Disponibile. ''')


@callback(
    Output('grafico-pioggia', 'figure'),
    [Input('checklist-input', 'value')]
)
def aggiorna_grafico_annuale(colonne):
    data_frame = df_annuale[df_annuale['mese'].isin(colonne)]
    barchart = px.bar(data_frame, x='mese', y='pioggia',
                      title='Pioggia media giornaliera durante i mesi dell\'anno 2013')
    barchart.update_layout(xaxis_title="mesi", yaxis_title="pioggia(mm)")
    barchart.update_traces(width=0.5)
    return barchart


def layout_annuale():
    return html.Div([
        grafico_annuale,
        checklist
    ])


def layout_mensile():
    return html.Div([
        dropdown,
        html.Br(),
        grafico_mensile,
        html.Br(),
        dbc.Row([
            tabella_mensile_meno_piovosa,
            tabella_mensile_piu_piovosa
        ])
    ])

def layout():
    return html.Div([
        html.Div(children='Dati sulle precipitazioni nelle capitali degli Stati Uniti nell\'anno 2013',
                 style={'textAlign': 'center', 'fontSize': '20px', 'margin-top': '25px',
                        'color': 'white', 'fontFamily': 'Verdana, sans-serif', 'textShadow': '0 0 8px #4c8a9e, 0 0 15px #4c8a9e, 0 0 20px #4c8a9e, 0 0 25px #4c8a9e'}),
        radio,
        html.Br(),
        html.Div(id='layout-corrente')
    ])


''' ------------------------------------------------- Variabili -------------------------------------------------'''

mesi = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre',
        'Novembre', 'Dicembre']
column_names = ['wban', 'state', 'st', 'country', 'latitude', 'longitude']

# path_piogge = '..\\..\\backend\\risultati_piogge'
# path_capitali = '..\\..\\backend\\dataset\\QCLCD\\wban_stato_capitale.csv'

path_piogge = 'pathTo\\yourBackendResultRain'
path_capitali = 'pathTo\\dataset\\wban_stato_capitale.csv'

# lettura dei dataframe da file .csv
df_annuale = pd.read_csv(f'{path_piogge}\\2013_Pioggia.csv', delimiter='; ', engine='python')
df_mensili = read_monthly_df()
df_capitali = pd.read_csv(f'{path_capitali}', names=column_names, delimiter=', ', engine='python').sort_values(by=['wban'], ignore_index=True)

# ordinamento dataframe per quantità di pioggia
df_mensili_ordinati = []

pioggia_giornaliera = []

for dataframe in df_mensili:
    dataframe = dataframe.sort_values(by=['wban_mensile'], ignore_index=True)
    dataframe['latitude'] = df_capitali['latitude']
    dataframe['longitude'] = df_capitali['longitude']
    df_mensili_ordinati.append(dataframe.sort_values(by=['rain'], ignore_index=True, ascending=False))

for i in range(len(mesi)):
    pioggia_giornaliera.append(df_mensili_ordinati[i].loc[df_mensili_ordinati[i]['wban_mensile'] == 25309].loc[:,
                               'rainiest_day':'less_rainy_value'])



''' ------------------------------------------------- Componenti -------------------------------------------------'''

radio = dbc.Row(
    dbc.RadioItems(
        options=[
            {"label": "Resoconto Annuale", "value": 1},
            {"label": "Analisi Mensile", "value": 2},

        ],
        id="radio_temp-input",
        style={"margin-left": "60px", "margin-top": "-25px"},
        value=1,
        inline=True,
    ),
)

grafico_mensile = dbc.Row([
    dcc.Graph(id='grafico-mensile')
])

tabella_mensile_meno_piovosa = dbc.Col(id='tabella-mensile-meno-piovosa')
tabella_mensile_piu_piovosa = dbc.Col(id='tabella-mensile-più-piovosa')

dropdown = dbc.DropdownMenu(
    [dbc.DropdownMenuItem(mese, id=str(x)) for x, mese in enumerate(mesi)],
    id='dropdown-input',
    label="Seleziona un mese",
    style={'margin-top': '-55px', 'margin-left': '1275px'}
)

grafico_annuale = dcc.Graph(id='grafico-pioggia', style={"margin-top": "15px"})

checklist = dbc.Row(
    [
        dbc.Checklist(
            options=[
                {"label": mese, "value": mese} for mese in mesi
            ],
            style={"backgroundColor": 'white', 'color': 'black', 'textAlign': 'center'},
            value=mesi,
            id="checklist-input",
            switch=True,
            inline=True
        )
    ]
)
