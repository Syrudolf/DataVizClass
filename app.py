import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd

data = pd.read_csv("OxCGRT_latest.csv",dtype={'CountryCode':'string', 'RegionName':'string', 'RegionCode':'string','Date':'string'})
data.loc[:,'Date'] = pd.to_datetime(data.Date, format='%Y-%m-%d')
print(data.Date.max())

app = dash.Dash(
    __name__,  
    external_stylesheets=[dbc.themes.LITERA], 
    meta_tags=[
        {'name':'viewport',
        'content':'width=device-width, initial-scale=1.0'}
    ]
    )

app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("The Dashboard", className="text-center text-primary, mb-4"),
                width=12)
    ]),
    
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(id='dropdown1', multi=False, value='Latvia',
                         options=[{'label':x, 'value':x}
                                  for x in sorted(data.CountryName.unique())
                                  ]
                         ),
            
            dcc.Graph(id='totalCases', figure={})
        ], width={'size':5, 'offset':0, 'order':1}),
        
        
        dbc.Col([
            dcc.Dropdown(id='dropdown2', multi=True, value=['Latvia','Portugal'],
                         options=[{'label':x, 'value':x}
                                  for x in sorted(data.CountryName.unique())]
                         ),
            dcc.Graph(id='totalCases2', figure={})
        ], width={'size':5, 'offset':0, 'order':2})
        
    ], no_gutters=False, justify='center'),
    
        #button
    dbc.Row([
        dbc.ButtonGroup(
    [dbc.Button("Calculated daily cases"), dbc.Button("7-day-average"), dbc.Button("14-day-average")]
)
    ], justify='center'),
    
    
], fluid=True)

# 1
@app.callback(
    Output('totalCases', 'figure'),
    Input('dropdown1', 'value')
)

def update_graph(selection):
    dataS = data[data.CountryName == selection]
    figure = px.line(dataS, x='Date', y='ConfirmedCases')
    return figure

# 2
@app.callback(
    Output('totalCases2', 'figure'),
    Input('dropdown2', 'value')
)

def update_graph(selection):
    dataS = data[data.CountryName.isin(selection)]
    figure = px.line(dataS, x='Date', y='ConfirmedCases', color='CountryName')
    return figure

# # 3
# @app.callback(
#     Output('plot', 'figure'),
#     Input('checklist', 'value')
# )

# def update_graph(selection):
#     dataS = data[data.CountryName.isin(selection)]
#     dataS = dataS[dataS.Date == '2021-01-01']
#     figure = px.bar(dataS, x='CountryName', y='ConfirmedCases')
#     return figure

if __name__=='__main__':
    app.run_server(debug=True, port=3000)