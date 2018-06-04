import dash
import dash_auth
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import numpy as np
import plotly
import os

from app import app, IA_df, job_df, levels, IA_display_columns, IA_job_display_columns, eds, exps



layout = html.Div([
    html.Div([
        html.H3('Industries App'),
        dcc.RadioItems(
            id='toggle',
            options=[{'label': i, 'value': i} for i in ['Show Instructions', 'Hide']],
            value='Hide',
            labelStyle={'display': 'inline-block'},
        ),
    ], style={'margin-left': '30', 'margin-right': '30'}),
    html.Div([
        html.Div([
            # Enter instructions
            dcc.Markdown('''
##### Filter Industry data from the Bureau of Labor Statistics and other sources.

- How it works:
    - The data table at the top of the page contains Industry data. All numerical data is in 1,000's (excluding %'s)
    - Use the dropdown filters at the top of the page to slice the data by major categories or features.
    - You can also click on the 'Filter Rows' button on the right and then filter any row in the data set.
        - Try using '>' or '<' to filter by size (ex. '>500')
        - Or filter Industry Titles by text search (ex. 'agriculture')
    - As you filter the data, the chart below will update to display only the filtered subset
    - Clicking on any single row in the table, or the chart, will then bring up further occupation-level data below.
        - This data can also be filtered by dropdown or using the 'Filter Rows' button

            '''),
            ],
            id='ind_instructions',
            style={'margin-left': '50', 'margin-right': '50'}
        ),
        html.Div([

            html.Div([
                html.P('Filter by Industry Categories or Individual Industries'),
                dcc.Dropdown(
                    id='types',
                    options=[
                        {'label': i, 'value': i} for i in IA_df.Type.unique().tolist()
                    ],
                    value=[],
                    multi=True,
                    clearable=False
                ),
            ],style={'width': '45%', 'float': 'left', 'padding-right': 25, 'font-size': 12}),

            html.Div([
                html.P('Filter by Category Level'),
                dcc.Dropdown(
                    id='level',
                    options=[
                        {'label': i, 'value': i} for i in levels
                    ],
                    value=[],
                    multi=True
                ),
            ],style={'width': '45%', 'float': 'right', 'padding-right': 25, 'font-size': 12}),

        ],style={'width': '100%', 'float': 'left', 'textAlign': 'left', 'padding-top': 15}),

    ],style={'textAlign': 'left', 'margin-left': '30', 'margin-right': '30'}),

    html.Div([
        html.Div([
            dt.DataTable(
                rows=IA_df[IA_display_columns].to_dict('records'),

                # optional - sets the order of columns
                columns=IA_display_columns,

                row_selectable=True,
                filterable=True,
                sortable=True,
                selected_row_indices=[],
                editable=False,
                min_height=280,
                column_widths=[50, 250, 120, 120, 140, 120, 120, 130, 80, 80, 60],
                row_height=25,
                header_row_height=35,
                id='IA_datatable'
            ),
            html.Div(id='selected-indexes', style={'padding-bottom': 20}),
            dcc.RadioItems(
                id='radio-buttons',
                options=[{'label': j, 'value': j} for j in
                        ['2026 Employment', '2026 % of Industry',
                        '2026 % of Occupation', 'Change (%)', 'Change (#)']],
                value='Change (%)',
                labelStyle={'display': 'inline-block'},
                style={'textAlign': 'center', 'font-size': 14, 'margin-right': 5}
            ),
            html.Div([
                dcc.Graph(
                    id='IA_graph',
                    config={'displayModeBar': False}
                ),
            ]),
        ],
        style={'width': '100%', 'margin-right': 'auto','font-size': 12, 'textAlign': 'left'}),

        html.Div([
            dcc.Tabs(
                tabs=[
                    {'label': i, 'value': i} for i in ['Occupations', 'Other']
                ],
                value='Occupations',
                id='tabs',
                vertical=False,
                style={
                    'borderBottom': 'thin lightgrey solid',
                    'textAlign': 'center',
                    'paddingTop': '5px',
                    'paddingRight': '300',
                    'paddingLeft': '300'
                }
            ),
            html.Div([
                html.Div([
                    html.P('Filter by Job Level'),
                    dcc.Dropdown(
                        id='job-level',
                        options=[
                            {'label': i, 'value': i} for i in job_df.Level.unique().tolist()
                        ],
                        value=[],
                        multi=True
                    ),
                ], style={'width': '20%', 'float': 'left', 'padding-right': 25, 'font-size': 12}),
                dt.DataTable(
                    rows=[{}],

                    #optional - sets the order of columns
                    columns=IA_job_display_columns,

                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    editable=False,
                    min_height=280,
                    column_widths=[50, 250, 120, 120, 140, 120, 120, 130, 80, 80],
                    row_height=25,
                    header_row_height=35,
                    id='IA_job_datatable'
                ),
                html.Div(id='ind_selected-indexes', style={'padding-bottom': 20}),
            ], id='OCCUPATIONS'),
            html.Div([
                dcc.RadioItems(
                    id='job-radio-buttons',
                    options=[{'label': j, 'value': j} for j in
                            ['2026 Employment', '2026 % of Industry',
                             '2026 % of Occupation', 'Change (#)', 'Change (%)']],
                    value='Change (%)',
                    labelStyle={'display': 'inline-block'},
                    style={'textAlign': 'center', 'font-size': 14, 'margin-right': 5}
                ),
                dcc.Graph(
                    id='IA_job_graph',
                    config={'displayModeBar': False}
                ),
            ], id='JOB_GRAPH')
        ],
        style={'width': '100%', 'font-size': 12, 'padding-bottom': 20}),

    ],
    style={'textAlign': 'left', 'margin-left': '30', 'margin-right': '30'}),

])



@app.callback(Output('ind_instructions', 'style'), [Input('toggle', 'value')])
def toggle_container(toggle_value):
    if toggle_value == 'Show Instructions':
        return {'display': 'block', 'borderBottom': 'thin lightgrey solid',
                'borderTop': 'thin lightgrey solid', 'font-size': 15}
    else:
        return {'display': 'none'}


@app.callback(Output('OCCUPATIONS', 'style'),
              [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Occupations':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('JOB_GRAPH', 'style'),
              [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Occupations':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# Filtering Logic with multiple filters
@app.callback(Output('IA_datatable', 'rows'),
              [Input('types', 'value'),
               Input('level', 'value')])
def update_rows(type_, lev_):
    # First, always filter by selected type
    dff = IA_df[IA_df.Type.isin(type_)]
    if len(type_) == 0:
        dff = IA_df.copy()
    # Set logic to list of True/False
    logic = [len(lev_) == 0]

    ##### No Filters
    if logic == [1]:
        return dff[IA_display_columns].to_dict('records')

    ##### One Filter
    elif logic == [0]:
        dff = dff[dff.Level.isin(lev_)]
        return dff[IA_display_columns].to_dict('records')


@app.callback(
    Output('IA_datatable', 'selected_row_indices'),
    [Input('IA_graph', 'clickData')],
    [State('IA_datatable', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('IA_graph', 'figure'),
    [Input('IA_datatable', 'rows'),
     Input('IA_datatable', 'selected_row_indices'),
     Input('radio-buttons', 'value')])
def update_figure(rows, selected_row_indices, radio_value):
    dff2 = pd.DataFrame(rows)[['Title', radio_value]]
    fig = plotly.tools.make_subplots(
        rows=1, cols=1,
        shared_xaxes=True)

    marker = {'color': ['teal']*len(dff2)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff2['Title'],
        'y': dff2[radio_value],
        'type': 'bar',
        'marker': marker
    }, 1, 1)

    fig.layout.update({'margin': {'l':100, 'r':100, 't':0, 'b':30}})
    fig.layout.update({'autosize': True, 'height': 225})
    #fig.layout.yaxis.update({'tickprefix': '%', 'hoverformat': '.1f'})
    fig.layout.xaxis.update({'showticklabels': False})

    return fig



@app.callback(
    Output('IA_job_datatable', 'rows'),
    [Input('IA_datatable', 'rows'),
     Input('IA_datatable', 'selected_row_indices'),
     Input('job-level', 'value')])
def update_ind_rows(rows, selected_row_indices, level):
    if len(selected_row_indices) == 0 or len(selected_row_indices) > 1:
        return [{}]
    title = pd.DataFrame(rows).ix[selected_row_indices]['Code'].tolist()
    dff3 = job_df[job_df['ind_code'] == title[0]]
    dff3.drop_duplicates(inplace=True, subset='Title')
    if len(level) > 0:
        dff3 = dff3[dff3.Level.isin(level)]
    return dff3[IA_job_display_columns].sort_values('2016 Employment', ascending=False).to_dict('records')



@app.callback(
    Output('IA_job_graph', 'figure'),
    [Input('IA_job_datatable', 'rows'),
     Input('IA_job_datatable', 'selected_row_indices'),
     Input('job-radio-buttons', 'value')])
def update_figure(rows, selected_row_indices, radio_value):

    fig = plotly.tools.make_subplots(
        rows=1, cols=1,
        shared_xaxes=True)

    if len(rows) != 1:
        dff4 = pd.DataFrame(rows)[['Title', radio_value]]

        marker = {'color': ['teal']*len(dff4)}
        for i in (selected_row_indices or []):
            marker['color'][i] = '#FF851B'

        fig.append_trace({
            'x': dff4['Title'],
            'y': dff4[radio_value],
            'type': 'bar',
            'marker': marker
        }, 1, 1)

        fig.layout.update({'margin': {'l':150, 'r':160, 't':0, 'b':30}})
        fig.layout.update({'autosize': True, 'width':1200, 'height': 225})
        fig.layout.xaxis.update({'showticklabels': False})

    else:
        fig.layout.update({'autosize': True, 'width':1200, 'height': 10})
        fig.layout.yaxis.update({'showticklabels': False})

    return fig



@app.callback(
    Output('IA_job_datatable', 'selected_row_indices'),
    [Input('IA_job_graph', 'clickData')],
    [State('IA_job_datatable', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


app.scripts.append_script({'external_url': 'https://cdn.rawgit.com/slaytor/Projects/ba3e394f/gtag.js'})
