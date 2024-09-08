from dash import html, dcc, Output, Input, callback, ctx
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
''' ------------------------------------------------- Funzioni -------------------------------------------------'''

def read_monthly_avg_df():
    df_list = []
    for mese in mesi:
        df_list.append(pd.read_csv(f'{path_temperature}\\2013_{mese}_Medie_Temperature.csv', delimiter = '; ', engine = 'python'))
    return df_list

def read_monthly_df():
    df_list = []
    for mese in mesi:
        df_list.append(pd.read_csv(f'{path_temperature}\\2013_{mese}_Temperature.csv', delimiter = '; ', engine = 'python'))
    return df_list

@callback(
    Output('layout-corrente-temp', 'children'),
    [Input('radio-input-temp', 'value')]
)
def aggiorna_layout(valore_radio):
    if valore_radio == 2:
        return layout_mensile_temp()
    elif valore_radio == 1:
        return layout_annuale_temp()
    else:
        return html.Div(children=''' Pagina non Disponibile. ''')

def colora_righe(nome_colonna):
    ris = []
    for i in range(len(mesi)):
        if df_annuale[nome_colonna].iloc[i] < 0:
            ris.append(html.Td(df_annuale[nome_colonna].iloc[i], style={'backgroundColor': '#828BD9', 'text-shadow': '1px 0 #000, -1px 0 #000, 0 1px #000, 0 -1px #000, 1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000', 'border': '1px solid black'}))
        elif 0 < df_annuale[nome_colonna].iloc[i] < 5:
            ris.append(html.Td(df_annuale[nome_colonna].iloc[i], style={'backgroundColor': '#8AB0FF', 'text-shadow': '1px 0 #000, -1px 0 #000, 0 1px #000, 0 -1px #000, 1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000', 'border': '1px solid black'}))
        elif 5 < df_annuale[nome_colonna].iloc[i] < 10:
            ris.append(html.Td(df_annuale[nome_colonna].iloc[i], style={'backgroundColor': '#FFFF99', 'text-shadow': '1px 0 #000, -1px 0 #000, 0 1px #000, 0 -1px #000, 1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000', 'border': '1px solid black'}))
        elif 10 < df_annuale[nome_colonna].iloc[i] < 15:
            ris.append(html.Td(df_annuale[nome_colonna].iloc[i], style={'backgroundColor': '#FFCC66', 'text-shadow': '1px 0 #000, -1px 0 #000, 0 1px #000, 0 -1px #000, 1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000', 'border': '1px solid black'}))
        elif 15 < df_annuale[nome_colonna].iloc[i] < 20:
            ris.append(html.Td(df_annuale[nome_colonna].iloc[i], style={'backgroundColor': '#FFA500', 'text-shadow': '1px 0 #000, -1px 0 #000, 0 1px #000, 0 -1px #000, 1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000', 'border': '1px solid black'}))
        elif 20 < df_annuale[nome_colonna].iloc[i] < 25:
            ris.append(html.Td(df_annuale[nome_colonna].iloc[i], style={'backgroundColor': '#FF8C00', 'text-shadow': '1px 0 #000, -1px 0 #000, 0 1px #000, 0 -1px #000, 1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000', 'border': '1px solid black'}))
        elif 25 < df_annuale[nome_colonna].iloc[i] < 30:
            ris.append(html.Td(df_annuale[nome_colonna].iloc[i], style={'backgroundColor': '#FF4040', 'text-shadow': '1px 0 #000, -1px 0 #000, 0 1px #000, 0 -1px #000, 1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000', 'border': '1px solid black'}))
        else:
            ris.append(html.Td(df_annuale[nome_colonna].iloc[i], style={'backgroundColor': '#FF0000', 'text-shadow': '1px 0 #000, -1px 0 #000, 0 1px #000, 0 -1px #000, 1px 1px #000, -1px -1px #000, 1px -1px #000, -1px 1px #000', 'border': '1px solid black'}))
    return ris




def costruisci_tabella(button_id):
    rows_mensili = [
        html.Th('Temperature Medie', colSpan=2,
                style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center',
                       'border': '1px solid white',
                       'height': '40px', 'vertical-align': 'middle'}),
        html.Tr([html.Td('Massima',
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(
                     f"{df_mensili[button_id]['avg_max_country_state'].iloc[0]}, {df_mensili[button_id]['avg_max_temp'].iloc[0]} °C",
                     style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
        html.Tr([html.Td('Minima',
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(
                     f"{df_mensili[button_id]['avg_min_country_state'].iloc[0]}, {df_mensili[button_id]['avg_min_temp'].iloc[0]} °C",
                     style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),

        html.Th('Temperature Massime', colSpan=2,
                style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center',
                       'border': '1px solid white',
                       'height': '40px', 'vertical-align': 'middle'}),
        html.Tr([html.Td('Massima',
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(
                     f"{df_mensili[button_id]['max_max_country_state'].iloc[0]}, {df_mensili[button_id]['max_max_temp'].iloc[0]} °C",
                     style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
        html.Tr([html.Td('Minima',
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(
                     f"{df_mensili[button_id]['max_min_country_state'].iloc[0]}, {df_mensili[button_id]['max_min_temp'].iloc[0]} °C",
                     style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),

        html.Th('Temperature Minime', colSpan=2,
                style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center',
                       'border': '1px solid white',
                       'height': '40px', 'vertical-align': 'middle'}),
        html.Tr([html.Td('Massima',
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(
                     f"{df_mensili[button_id]['min_max_country_state'].iloc[0]}, {df_mensili[button_id]['min_max_temp'].iloc[0]} °C",

                     style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
        html.Tr([html.Td('Minima',
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(
                     f"{df_mensili[button_id]['min_min_country_state'].iloc[0]}, {df_mensili[button_id]['min_min_temp'].iloc[0]} °C",
                     style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),

        html.Th('Escursione Termica', colSpan=2,
                style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center',
                       'border': '1px solid white',
                       'height': '40px', 'vertical-align': 'middle'}),
        html.Tr([html.Td('Media',
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(f"{df_mensili[button_id]['avg_exc_temp'].iloc[0]} °C",
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
        html.Tr([html.Td('Massima',
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(f"{df_mensili[button_id]['max_exc_temp'].iloc[0]} °C",
                         style={'text-align': 'center', 'border': '1px solid white',
                                'backgroundColor': '#1a0933ad'})], ),
        html.Tr([html.Td('Minima',
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
                 html.Td(f"{df_mensili[button_id]['min_exc_temp'].iloc[0]} °C",
                         style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),

    ]

    heads_mensili = [[html.Thead(rows_mensili[0])], [html.Thead(rows_mensili[3])], [html.Thead(rows_mensili[6])],
                     [html.Thead(rows_mensili[9])]]

    bodies_mensili = [[html.Tbody([rows_mensili[1], rows_mensili[2]])],
                      [html.Tbody([rows_mensili[4], rows_mensili[5]])],
                      [html.Tbody([rows_mensili[7], rows_mensili[8]])],
                      [html.Tbody([rows_mensili[10], rows_mensili[11], rows_mensili[12]])], ]

    tabelle_mensili = [
        dbc.Table(
            heads_mensili[0] + bodies_mensili[0],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True
        ),
        dbc.Table(
            heads_mensili[1] + bodies_mensili[1],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True
        ),
        dbc.Table(
            heads_mensili[2] + bodies_mensili[2],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True
        ),
        dbc.Table(
            heads_mensili[3] + bodies_mensili[3],
            bordered=True,
            hover=True,
            responsive=True,
            striped=True
        ),
    ]

    tabelle_informative_mensili = dbc.Row([
        dbc.Col(tabelle_mensili[0]),
        dbc.Col(tabelle_mensili[1]),
        dbc.Col(tabelle_mensili[2]),
        dbc.Col(tabelle_mensili[3])
    ])
    return tabelle_informative_mensili


@callback([
    Output('dropdown-input-temp', 'label'),
    Output('tabella-mensile-temp', 'children'),
    Output('grafico-mensile-temp', 'figure'),
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

        grafico_temperature_mensili_default = px.histogram(data_frame= df_medie_mensili[0], x='day', y=['Tmax', 'Tavg', 'Tmin'], barmode='group', title=f'Temperature di {mesi[0]}',
                                                           labels={'variable': 'Temperatura'}, opacity=1,
                                                           color_discrete_sequence=['#FF4040', '#FFA500', '#828BD9'], nbins=50)
        grafico_temperature_mensili_default.update_layout(xaxis_title=f"Giorni di {mesi[0]}", yaxis_title="Medie Temperature °C")


        nuovi_nomi = {'Tmax': 'Massima', 'Tavg': 'Media', 'Tmin':'Minima'}
        grafico_temperature_mensili_default.for_each_trace(lambda t: t.update(name=nuovi_nomi[t.name],
                                                    legendgroup=nuovi_nomi[t.name],
                                                    hovertemplate=t.hovertemplate.replace(t.name, nuovi_nomi[t.name]))
                                 )


        tabella_default = costruisci_tabella(0)
        return ["Gennaio", tabella_default, grafico_temperature_mensili_default]
    else:

        button_id = int(ctx.triggered_id) if not None else 'Seleziona un mese'

        grafico_temperature_mensili = px.histogram(data_frame= df_medie_mensili[button_id], x='day', y=['Tmax', 'Tavg', 'Tmin'], barmode='group', title=f'Temperature di {mesi[button_id]}',
                                                       labels={'variable': 'Legenda'}, opacity=1,
                                                       color_discrete_sequence=['#FF4040', '#FFA500', '#828BD9'], nbins=50)
        grafico_temperature_mensili.update_layout(xaxis_title= f"Giorni di {mesi[button_id]}", yaxis_title="Medie Temperature °C")
        nuovi_nomi = {'Tmax': 'Massima', 'Tavg': 'Media', 'Tmin': 'Minima'}
        grafico_temperature_mensili.for_each_trace(lambda t: t.update(name=nuovi_nomi[t.name],
                                                                              legendgroup=nuovi_nomi[t.name],
                                                                              hovertemplate=t.hovertemplate.replace(
                                                                                  t.name, nuovi_nomi[t.name]))
                                                           )

        tabella = costruisci_tabella(button_id)
        return [mesi[button_id], tabella, grafico_temperature_mensili]

def layout_mensile_temp():
    return html.Div([
        dropdown,
        html.Br(),
        grafico_mensile,
        html.Br(),
        tabella_mensile
    ])


def layout_annuale_temp():
    return html.Div([
        html.Br(),
        tabella_annuale_temp,
        tabelle_informative
    ])
def layout():
    return html.Div([
        html.Div(children='Dati sulle temperature nelle capitali degli Stati Uniti nell\'anno 2013',
                 style={'textAlign': 'center', 'fontSize': '20px', 'margin-top': '25px',
                        'color': 'white', 'fontFamily': 'Verdana, sans-serif',
                        'textShadow': '0 0 8px #4c8a9e, 0 0 15px #4c8a9e, 0 0 20px #4c8a9e, 0 0 25px #4c8a9e'}),
        radio,
        html.Br(),
        html.Div(id='layout-corrente-temp')
    ])


''' ------------------------------------------------- Variabili -------------------------------------------------'''

mesi = ['Gennaio', 'Febbraio', 'Marzo', 'Aprile', 'Maggio', 'Giugno', 'Luglio', 'Agosto', 'Settembre', 'Ottobre', 'Novembre', 'Dicembre']

# path_temperature = '..\\..\\backend\\risultati_temperature'

path_temperature = 'pathTo\\yourBackendResultTemp'

# lettura dei dataframe da file .csv
df_info_anno = pd.read_csv(f'{path_temperature}\\2013_Temperature.csv', delimiter = '; ', engine = 'python')
df_annuale = pd.read_csv(f'{path_temperature}\\2013_Temperature_Annuali.csv', delimiter='; ', engine='python')
df_mensili = read_monthly_df()
df_medie_mensili = read_monthly_avg_df()

''' ------------------------------------------------- Componenti -------------------------------------------------'''
radio = dbc.Row(
    dbc.RadioItems(
        options=[
            {"label": "Resoconto Annuale", "value": 1},
            {"label": "Analisi Mensile", "value": 2},
        ],
        id="radio-input-temp",
        style={"margin-left": "60px", "margin-top": "-25px"},
        value=1,
        inline=True,
    ),
)

dropdown = dbc.DropdownMenu(
    [dbc.DropdownMenuItem(mese, id=str(x)) for x, mese in enumerate(mesi)],
    id='dropdown-input-temp',
    label="Seleziona un mese",
    style={'margin-top': '-55px', 'margin-left': '1275px'},
    # value='Gennaio'
)

rows_annuali = [
    html.Th('Medie di Temperature registrate presso le capitali degli Stati Uniti', colSpan=13,
            style={'text-align': 'center', 'width': '250px', 'border': '1px solid white', 'backgroundColor': '#1a0933',
                   'height': '40px', 'vertical-align': 'middle'}),

    html.Tr([html.Td(' ',
                     style={'width': '250px', 'border': '1px solid white'})] + [
                html.Td(mese, style={'border': '1px solid white'}) for mese in mesi]),
    html.Tr([html.Td('Temperatura Media (°C)',
                     style={'width': '250px', 'border': '1px solid white'})] + colora_righe('avgTemp')),
    html.Tr([html.Td('Temperatura Massima (°C)',
                     style={'width': '250px', 'border': '1px solid white'})] + colora_righe('maxTemp')),
    html.Tr([html.Td('Temperatura Minima (°C)',
                     style={'width': '250px', 'border': '1px solid white'})] + colora_righe('minTemp'))]

table_head_annuale = [html.Thead(rows_annuali[0])]
table_body_annuale = [html.Tbody([rows_annuali[1], rows_annuali[2], rows_annuali[3], rows_annuali[4]])]

tabella_annuale_temp = dbc.Table(
    table_head_annuale + table_body_annuale,
    bordered=True,
    hover=True,
    responsive=True,
    striped=True
)

row_tab_max_temp = [
    html.Th('Temperatura Massima registrata nel 2013', colSpan='2', style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center', 'border': '1px solid white', 'height': '40px', 'vertical-align': 'middle'}),
    html.Tr([html.Td(f"{df_info_anno['max_temp'].iloc[0]} °C, {df_info_anno['max_month'].iloc[0]}", style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}), html.Td(df_info_anno['max_country_state'].iloc[0], style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
]
tab_max_temp_head = [html.Thead(row_tab_max_temp[0])]
tab_max_temp_body = [html.Tbody(row_tab_max_temp[1])]

tab_max_temp = dbc.Table(
    tab_max_temp_head+tab_max_temp_body,
    bordered=True,
    hover=True,
    responsive=True,
    striped=True
)

row_tab_min_temp = [

    html.Th('Temperatura Minima registrata nel 2013', colSpan='2', style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center', 'border': '1px solid white', 'height': '40px', 'vertical-align': 'middle'}),
    html.Tr([html.Td(f"{df_info_anno['min_temp'].iloc[0]} °C, {df_info_anno['min_month'].iloc[0]}", style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}), html.Td(df_info_anno['min_country_state'].iloc[0], style={'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
]

tab_min_temp_head = [html.Thead(row_tab_min_temp[0])]
tab_min_temp_body = [html.Tbody(row_tab_min_temp[1])]

tab_min_temp = dbc.Table(
    tab_min_temp_head+tab_min_temp_body,
    bordered=True,
    hover=True,
    responsive=True,
    striped=True
)

row_exc = [
    html.Th('Escursione termica nel 2013', colSpan='2', style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center', 'border': '1px solid white', 'height': '40px', 'vertical-align': 'middle'}),
    html.Tr([html.Td('Escursione Media Massima', style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}), html.Td(f"{df_info_anno['avg_max_exc_temp'].iloc[0]} °C, {df_info_anno['avg_min_exc_month'][0]}", style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
    html.Tr([html.Td('Escursione Media Minima', style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}), html.Td(f"{df_info_anno['avg_min_exc_temp'].iloc[0]} °C, {df_info_anno['avg_max_exc_month'][0]}", style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
    html.Tr([html.Td('Escursione Massima', style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}), html.Td(f"{df_info_anno['max_exc_temp'].iloc[0]}°C, {df_info_anno['max_exc_month'][0]}", style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
    html.Tr([html.Td('Escursione Minima', style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}), html.Td(f"{df_info_anno['min_exc_temp'].iloc[0]} °C, {df_info_anno['min_exc_month'][0]}", style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
]

tab_exc_head = [html.Thead(row_exc[0])]
tab_exc_body = [html.Tbody([row_exc[1], row_exc[2], row_exc[3], row_exc[4]])]

tab_exc = dbc.Table(
    tab_exc_head + tab_exc_body,
    bordered=True,
    hover=True,
    responsive=True,
    striped=True
)

tabelle_informative = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col([tab_max_temp, html.Br(), tab_min_temp]),
        dbc.Col([tab_exc]),
    ])

])

grafico_mensile = dbc.Row([
    dcc.Graph(id='grafico-mensile-temp')
])

tabella_mensile = dbc.Row(id='tabella-mensile-temp')

