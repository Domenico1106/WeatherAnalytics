from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

''' ------------------------------------------------- Funzioni -------------------------------------------------'''

def layout():
    return html.Div([
        html.Div(children='Previsione Temperature negli Stati Uniti nel 2014',
                 style={'textAlign': 'center', 'fontSize': '20px', 'margin-top': '25px',
                        'color': 'white', 'fontFamily': 'Verdana, sans-serif',
                        'textShadow': '0 0 8px #4c8a9e, 0 0 15px #4c8a9e, 0 0 20px #4c8a9e, 0 0 25px #4c8a9e'}),
        html.Br(),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=grafico_mensile)),
            dbc.Col(dcc.Graph(figure = grafico_annuale))

        ]),
        html.Br(),
        tabella_mensile,

    ])

''' ------------------------------------------------- Variabili -------------------------------------------------'''

# path_regressione = '..\\..\\backend\\risultati_regressione'
# path_regressione_annuale = '..\\..\\backend\\dataset\\RegressioneLineare\\TemperatureUSA.csv'

path_regressione = 'pathTo\\yourBackendResultRegression'
path_regressione_annuale = 'pathTo\\dataset\\RegressioneLineare\\TemperatureUSA.csv'
df_regressione = pd.read_csv(f"{path_regressione}\\2014_Previsione.csv", delimiter = "; ", engine = 'python')
df_regressione_annuale = pd.read_csv(path_regressione_annuale, delimiter=', ', engine='python', names= ['anno', 'valore'])
df_regressione_annuale['valore'] = ((df_regressione_annuale['valore'] - 32) / 1.8).round(2)

''' ------------------------------------------------- Componenti -------------------------------------------------'''

row_monthly = [
    html.Th("Temperatura Media Annuale", colSpan='2', style={'backgroundColor': '#1a0933', 'width': '250px', 'text-align': 'center', 'border': '1px solid white', 'height': '40px', 'vertical-align': 'middle'}),
    html.Tr([html.Td(f"Previsione: {df_regressione['previsioneAnnuale'].iloc[0]} °C", style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'}),
             html.Td(f"Valore Reale: {df_regressione['valoreAnnualeReali'].iloc[0]} °C", style={'width': '330px', 'text-align': 'center', 'border': '1px solid white', 'backgroundColor': '#1a0933ad'})]),
]
head_monthly = [[html.Thead(row_monthly[0])]]
body_monthly = [[html.Tbody(row_monthly[1])]]

tabella_mensile = dbc.Table(
    head_monthly[0] + body_monthly[0],
    bordered=True,
    hover=True,
    responsive=True,
    striped=True,

)

grafico_mensile = px.histogram(data_frame=df_regressione, x='mese', y=['previsione', 'valoriReali'], barmode='group',
                               title='Temperature Mensili del 2014',
                               labels={'variable': 'Temperature'}, opacity=0.8,
                               color_discrete_sequence=['#EB89B5', '#330C73'], nbins=50)
grafico_mensile.update_layout(xaxis_title="Mesi", yaxis_title="Medie Temperature °C")


nuovi_nomi = {'previsione': 'Previste', 'valoriReali': 'Reali'}
grafico_mensile.for_each_trace(lambda t: t.update(name=nuovi_nomi[t.name],
                                                  legendgroup=nuovi_nomi[t.name],
                                                  hovertemplate=t.hovertemplate.replace(t.name, nuovi_nomi[t.name]))
                               )

grafico_annuale = px.scatter(df_regressione_annuale, x="anno", y="valore", labels={'valore': 'Temperatura °C', 'anno': 'Anni'}, trendline="ols", trendline_color_override="red", title='Regressione Lineare tra Anno e Temperatura negli anni precedenti il 2014')
