#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 15:42:01 2020

@author: sashaqanderson
"""

import pandas as pd
import plotly.graph_objs as go
import dash
import flask
import dash_table
#from dash.dependencies import Output, Input
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc

server = flask.Flask('app')

df = pd.read_csv('data.csv')

df2 = df.copy()

#prepare the data for perceived control v comfort
df2['Discomfort Location: FEET'].fillna(2, inplace = True)
df2['Discomfort Location: FEET'].replace({8: 1}, inplace=True)
df2['Discomfort Location: BACK'].fillna(2, inplace = True)
df2['Discomfort Location: BACK'].replace({3: 1}, inplace=True)
df2['Discomfort Location: FEET']

def grouped_df(title):
    df = df2.groupby([title, 'comfort']).size().unstack(fill_value=0)
    if len(df.columns) > 1:
        df['Total'] = df[0] + df[1]
        df['% Uncomfy'] = round(100 * df[0]/df['Total'],2)
        df['% Comfy'] = round(100 * df[1]/df['Total'], 2)
        df.columns = ['Uncomfy', 'Comfy', 'Total', '% Uncomfy', '% Comfy']
    return df

df_PC = grouped_df('General Satisfaction w/ Perceived Control')
df_PC.reset_index(inplace=True)

df_AS = grouped_df('General Satisfaction w/ Amount of Space')
df_AS.reset_index(inplace=True)

df_DB = grouped_df('Discomfort Location: BACK')
df_DB.reset_index(inplace=True)
df_DB['Discomfort Location: BACK'] = ['Yes', 'No']

df_DF = grouped_df('Discomfort Location: FEET')
df_DF.reset_index(inplace=True)
df_DF['Discomfort Location: FEET'] = ['Yes', 'No']  

def make_piechart(labels, titles, values, texts):
    data = []
    colors = ['#5766c8', '#FF8000']
    for label, value, text_, ttl in zip(labels, values, texts, titles):
        data.append(html.Div([dcc.Graph(figure={'data': [go.Pie(labels=label,
                                                                values=value,
                                                                text = text_,
                                                                hovertemplate= "%{label} <br>n = %{text}",
                                                                marker=dict(colors=colors)
                                                                )],
                                        'layout': go.Layout(
                                                title=go.layout.Title(text=ttl),
                                                height = 400)
                                        })
                              ], className='col-sm-4'))
    return data                                        


def make_piechart2(labels, titles, values, texts):
    data = []
    colors = ['#5766c8', '#FF8000']
    for label, value, text_, ttl in zip(labels, values, texts, titles):
        data.append(html.Div([dcc.Graph(figure={'data': [go.Pie(labels=label,
                                                                values=value,
                                                                text = text_,
                                                                hovertemplate= "%{label} <br>n = %{text}",
                                                                marker=dict(colors=colors)
                                                                )],
                                        'layout': go.Layout(
                                                title=go.layout.Title(text=ttl),
                                                height = 400)
                                        })
                              ], className='col-sm-6'))
    return data  

#Satisfied w/ Perceived Control Pie Charts
labels = 5*[['Comfy', 'Uncomfy']]
titles = list(['1- Very Dissatisfied w/ Perceived Control','2- Dissatisfied w/ Perceived Control', '3- Somewhat Dissatisfied w/ Perceived Control', 
              '4- Satisfied w/ Perceived Control','5- Satisfied w/ Perceived Control'])    
values = list(zip(df_PC['% Comfy'], df_PC['% Uncomfy']))
texts = list(zip(df_PC['Comfy'], df_PC['Uncomfy']))
data = make_piechart(labels, titles, values, texts)

# Satisfied w/ Amt Space Pie Charts
labels2 = 5*[['Comfy', 'Uncomfy']]
titles2 = list(['3- Somewhat Dissatisfied w/ Amt Space', 
              '4- Satisfied w/ Amt Space','5- Somewhat Satisfied w/ Amt Space', '6- Very Satisfied w/ Amt of Space'])    
values2 = list(zip(df_AS['% Comfy'], df_AS['% Uncomfy']))
texts2 = list(zip(df_AS['Comfy'], df_AS['Uncomfy']))
data2 = make_piechart(labels2, titles2, values2, texts2)

#Discomfort in Feet Pie Charts
labels3 = 2*[['Comfy', 'Uncomfy']]
titles3 = list(['Discomfort in Feet', 'No Discomfort in Feet'])    
values3 = list(zip(df_DF['% Comfy'], df_DF['% Uncomfy']))
texts3 = list(zip(df_DF['Comfy'], df_DF['Uncomfy']))
data3 = make_piechart2(labels3, titles3, values3, texts3)
                                  
#Discomfort in Back Pie Charts
labels4 = 2*[['Comfy', 'Uncomfy']]
titles4 = list(['Discomfort in Back', 'No Discomfort in Back'])    
values4 = list(zip(df_DB['% Comfy'], df_DB['% Uncomfy']))
texts4 = list(zip(df_DB['Comfy'], df_DB['Uncomfy']))
data4 = make_piechart2(labels4, titles4, values4, texts4)

#prepare temp data for histograms
df_uncomfy = df2[(df2['comfort']==0)]
df_uncomfy.comfort[(df_uncomfy['comfort']==0)] = 1
df_comfy = df2[(df2['comfort']==1)]
#-------------------------------------------------------------------------

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash('app', external_stylesheets=[dbc.themes.BOOTSTRAP], server = server)

app.layout = html.Div([
        html.Div([
                html.H1(children = 'Thermal Comfort in a Medium Office', style={'text-align':'center'}),
                html.Div(children = '''Data obtained from: Langevin, J., Wen, J., & Gurian, P.L. (2015). Tracking the human-building interaction''', style={'text-align':'center'}),
                html.Br(),
                html.Hr()
                ]),
        dbc.Tabs([
                dbc.Tab(label ='Office Satisfaction',
                        children = [
                                dcc.Dropdown(
                                        id='dropdown1',
                                        options=[
                                                {'label': 'General Satisfaction with Perceived Control', 'value': 'PC'},
                                                {'label': 'General Satisfaction with Amount of Space', 'value': 'AS'}
                                                ],
                                        placeholder ='Select a variable'),
                                html.Div(id='dd-output-container')
                                ]),
                dbc.Tab(label = 'Bodily Discomfort',
                        children = [
                                dcc.Dropdown(
                                        id = 'dropdown2',
                                        options = [
                                                {'label': 'Discomfort in Feet', 'value': 'DF'},
                                                {'label': 'Discomfort in Back', 'value': 'DB'}
                                                ],
                                        placeholder = 'Select a variable'),
                                html.Div(id = 'dd-output-container2')
                                ]
                        ),
                dbc.Tab(label = 'Temperature',
                    children = [
                            dcc.Dropdown(
                                    id = 'dropdown3',
                                    options = [
                                            {'label': 'Thermostat Setpoint', 'value': 'TS'},
                                            {'label': 'Indoor Temperature', 'value': 'IT'},
                                            {'label': 'Outdoor Temperature', 'value': 'OT'}
                                            ],
                                    placeholder = 'Select a variable'),
                            html.Div(id = 'dd-output-container3')
                                ]        
                                    )
                ])
    
    ])
    
@app.callback(
    dash.dependencies.Output('dd-output-container', 'children'),
    [dash.dependencies.Input('dropdown1', 'value')])
def update_output(value):
    if value == 'AS':
        body =  html.Div([
                       html.Center(
                                html.Div(children = [
                                        html.Br(),
                                        html.H3(children = 'Comfort v. Satisfied w/ Amount of Space')
                                        ])
                                ),
                        html.Center(
                                html.Div(
                                        dash_table.DataTable(id = 'table6', 
                                                            columns = [{"name": i, "id": i} for i in df_AS],
                                                            data = df_AS.to_dict('records'),
                                                            style_table={'width': '60%'},
                                                            style_cell={
                                                                    'height': 'auto',
                                                                    'maxWidth': '80px',
                                                                    'whiteSpace': 'normal'}))
                                ),
                        html.Div(dbc.Row(data2))
                                ]
                            )
        
    else:
        body = html.Div([
                html.Center(
                        html.Div(children = [
                            html.Br(),
                            html.H3(children = 'Comfort v. Perceived Control')])
                        
                        ),
                html.Center(
                        html.Div(
                                dash_table.DataTable(id = 'table1',
                                                     columns = [{"name": i, "id": i} for i in df_PC],
                                                     data = df_PC.to_dict('records'),
                                                     style_table={'width': '60%'},
                                                     style_cell={
                                                             'height': 'auto',
                                                             'maxWidth': '80px',
                                                             'whiteSpace': 'normal'}
                                                     ),
                                                     
                                        )),
                html.Div(dbc.Row(data)),                    
                ]
                )
    return body

@app.callback(
    dash.dependencies.Output('dd-output-container2', 'children'),
    [dash.dependencies.Input('dropdown2', 'value')])
def update_output2(value):
    if value == 'DB':
        body = html.Div([
                html.Center(
                        html.Div(children = [html.Br(),
                                             html.H3(children = 'Comfort v. Back Discomfort')
                                             ]
                            )
                        ),
                html.Center(
                    html.Div(                                                   
                            dash_table.DataTable(id = 'table8',
                                                 columns = [{"name": i, "id": i} for i in df_DB],
                                                 data = df_DB.to_dict('records'),
                                                 style_table={'width': '60%'},
                                                 style_cell={
                                                         'height': 'auto',
                                                         'maxWidth': '80px',
                                                         'whiteSpace': 'normal'}
                                                 )
                            )
                        ),
                html.Div(dbc.Row(data4))
                    ]
                    )
    elif value == 'DF':
        body = html.Div([
                html.Center(
                        html.Div([html.Br(),
                                  html.H3(children = 'Comfort v. Foot Discomfort')
                                  ]
                            )
                        ),
                html.Center(  
                    html.Div(
                            dash_table.DataTable(id = 'table7',
                                                 columns = [{"name": i, "id": i} for i in df_DF],
                                                 data = df_DF.to_dict('records'),
                                                 style_table={'width': '60%'},
                                                 style_cell={
                                                         'height': 'auto',
                                                         'maxWidth': '80px',
                                                         'whiteSpace': 'normal'}
                                                 )
                            )
                        ), 
                html.Div(dbc.Row(data3))
                ]
                )
    else:
        body = html.Div([

                ]
                )                        
    return body

@app.callback(
    dash.dependencies.Output('dd-output-container3', 'children'),
    [dash.dependencies.Input('dropdown3', 'value')])
def update_output3(value):
    if value == 'IT':
        body = html.Div([
                html.Center(                    
                        html.Div([html.Br(),
                                  html.H3(children = 'Comfort v. Indoor Temperature')]
                            )
                        ),                                      
                dcc.Graph(id = 'graph2',
                          figure= {'data': [
                                    {'x': df_uncomfy['INDOOR Ambient Temp.'], 'y': df_uncomfy.comfort, 'name': 'uncomfy', 'type': 'histogram', 'histfunc': 'count', 'xbins': dict(size = 0.5), 'marker' : dict(color = 'FF8000')},
                                    {'x': df_comfy['INDOOR Ambient Temp.'], 'y': df_comfy.comfort, 'name': 'comfy', 'type': 'histogram', 'histfunc': 'count', 'marker' : dict(color = '#5766c8')}
                                    ],
                            'layout': {
#                                    'title': 'Comfort v. Indoor Temperature',
                                    'barmode':'stack',
                                    'xaxis': dict(
                                            title= 'Temperature (Celsius)')                                                   
                                    }
                            })                
                ])
    elif value == 'OT':
        body = html.Div([
                html.Center(                    
                        html.Div([html.Br(),
                                  html.H3(children = 'Comfort v. Outdoor Temperature')]
                            )
                        ),                                                                        
                dcc.Graph(id = 'graph3',
                          figure= {'data': [
                                    {'x': df_uncomfy['OUTDOOR Ambient Temp.'], 'y': df_uncomfy.comfort, 'name': 'uncomfy', 'type': 'histogram', 'histfunc': 'count', 'xbins': dict(size = 2.5), 'marker' : dict(color = 'FF8000')},
                                    {'x': df_comfy['OUTDOOR Ambient Temp.'], 'y': df_comfy.comfort, 'name': 'comfy', 'type': 'histogram', 'histfunc': 'count', 'marker' : dict(color = '#5766c8')}
                                    ],
                            'layout': {
#                                    'title': 'Comfort v. Outdoor Temperature',
                                    'barmode':'stack',
                                    'xaxis': dict(
                                            title= 'Temperature (Celsius)')                                                   
                                    }
                            }
                            )                  
                ])
    elif value == 'TS': 
        body = html.Div([
                html.Center(
                        html.Div([html.Br(),
                                  html.H3(children = 'Comfort v. Thermostat Setpoint')]
                            )
                        ),                 
                dcc.Graph(id = 'graph5',
                          figure= {'data': [
                                    {'x': df_uncomfy['Base Thermostat HEATING Setpoint'], 'y': df_uncomfy.comfort, 'name': 'uncomfy', 'type': 'histogram', 'histfunc': 'count', 'xbins': dict(size = 1), 'marker' : dict(color = 'FF8000')},
                                    {'x': df_comfy['Base Thermostat HEATING Setpoint'], 'y': df_comfy.comfort, 'name': 'comfy', 'type': 'histogram', 'histfunc': 'count', 'marker' : dict(color = '#5766c8')}
                                    ],
                            'layout': {
#                                    'title': 'Comfort v. Thermostat Level',
                                    'barmode':'stack',
                                    'xaxis': dict(
                                            title= 'Thermostat Set-Point (Celsius)')                                                   
                                    }
                            }
                            ),                
                ])
    else:
        body = html.Div([ 
                ])
                            
    return body

if __name__ == '__main__':
    app.run_server(debug=True)
