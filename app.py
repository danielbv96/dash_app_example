
# coding: utf-8

# In[102]:


import json
from textwrap import dedent as d
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})
colors = {
    'background': '#e6f2ff',
    'text': '#7FDBFF'}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

df = pd.read_csv('nama_10_gdp_1_Data.csv')

title1 = 'Correlation between indicators'

title2 = 'Evolution of indicators'

available_indicators = df['NA_ITEM'].unique()
available_countries = df['GEO'].unique()
available_units = df['UNIT'].unique()

app.layout = html.Div([
    html.Div([
        html.Div([
            dcc.Markdown('''*Daniel Bermejo Vidal*
# Cloud Computing - Final Project
            '''),
            dcc.Markdown('''## First exercise:
            '''),

            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Gross domestic product at market prices'
                ),
                dcc.RadioItems(
                    id='units',
                    options=[{'label': i, 'value': i} for i in available_units],
                    value='Current prices, million euro',
                    labelStyle={'display': 'inline-block'}
                ),
            
            ],
            style={'width': '48%', 'display': 'inline-block','margin-bottom' : '35px'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Value added, gross'
                ),
            ],style={'width': '48%', 'float': 'right', 'display': 'inline-block','margin-bottom' : '35px'})
        ]),

        dcc.Graph(id='indicator-graphic',
                  clickData={'points': [{'text': 'Belgium'}]}
                  ),
        
        
        

        dcc.Slider(
            id='year--slider',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=df['TIME'].max(),
            step=None,
            marks={str(year): str(year) for year in df['TIME'].unique()},

        ),
        
        dcc.Markdown('''## Second exercise:
#### To select the country, click on the points in the first graph.
        '''),
        html.Div(id='country',style = {'color':'blue'})
    ],style = {'display': 'inline-block','width': '98%','margin-left': '20px'}),
    html.Div([
       # html.Div([
       #     dcc.Dropdown(
        #        id='dropdown-geo',
         #       options=[{'label': i, 'value': i} for i in available_countries],
          #      value='Belgium'
           # ),
       # ],style={'width': '0%', 'display': 'inline-block','margin-bottom' : '35px'}),
        
        html.Div([
            dcc.Dropdown(
                id='dropdown-indi',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            ),
        ],style={'width': '100%', 'float': 'initial', 'display': 'inline-block','margin-bottom' : '35px'}),
        html.Div([dcc.RadioItems(
                    id='units_countries',
                    options=[{'label': i, 'value': i} for i in available_units],
                    value='Current prices, million euro',
                    labelStyle={'display': 'inline-block'})]),
                
        dcc.Graph(id='country-graphic')
        
    ],style = {'display': 'inline-block','width': '98%','margin-left': '20px','margin-bottom':'20px'})
        

    
],style = {'display': 'inline-block', 'width': '100%','margin-left' : '0px','margin-right': '0px','background-color': 'lightgray'})


@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('units','value'),
     dash.dependencies.Input('year--slider', 'value')])

def update_graph(xaxis_column_name, yaxis_column_name,
                 units_type,
                 year_value):
    dfff = df[df['UNIT']== units_type]
    dff = dfff[dfff['TIME'] == year_value]
    
    
    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            name='Country',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'red'},
                'color' : 'rgb(0,201,87)',
            }
          
            
            
        )],
        'layout': go.Layout(
            title=title1,
            plot_bgcolor = colors['background'],
            paper_bgcolor = colors['background'],
            margin={'l': 70, 'b': 50, 't': 50, 'r': 30},
            hovermode='closest',
            showlegend=True
        )
        
    }

@app.callback(
    dash.dependencies.Output('country','children'),
    [dash.dependencies.Input('indicator-graphic','clickData')])

def update_output_div(clickData):
    country_name_text = clickData['points'][0]['text']
    return 'You have selected "{}"'.format(country_name_text)

@app.callback(
    dash.dependencies.Output('country-graphic','figure'),
    [dash.dependencies.Input('indicator-graphic','clickData'),
    # dash.dependencies.Input('dropdown-geo','value'),
     dash.dependencies.Input('units_countries','value'),
     dash.dependencies.Input('dropdown-indi','value')])

def update_graph2(clickData,
                  #dropdown_geo_name,
                  units_countries_name,
                  dropdown_indi_name):
    country_name = clickData['points'][0]['text']
    dff1 = df[df['UNIT']==units_countries_name]
    dff2 = dff1[dff1['GEO'] == country_name]
    return {
        'data': [go.Scatter(
            x=dff2['TIME'].unique(),
            y=dff2[dff2['NA_ITEM'] == dropdown_indi_name]['Value'],
            text=dff2[dff2['NA_ITEM'] == dropdown_indi_name]['TIME'],
            mode='lines',
        )],
        'layout': go.Layout(
            title=title2,
            autosize=True,
            xaxis={
                'title': 'Year'
            },
            yaxis={
                'title': dropdown_indi_name,
            },
            margin={'l': 70, 'b': 50, 't': 50, 'r': 30, 'autoexpand':True},
            plot_bgcolor = colors['background'],
            paper_bgcolor = colors['background'],
            hovermode='closest'
        )
        
    }

if __name__ == '__main__':
    app.run_server()

