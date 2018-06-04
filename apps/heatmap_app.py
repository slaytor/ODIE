import dash
import dash_auth
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt
import pandas as pd
import numpy as np
import plotly
import plotly.figure_factory as ff
import os

from app import app, df, ind_df, IA_df, display_columns, ind_display_columns

level_one_jobs = df[df.Level == 1].copy()
level_one_jobs['Job Title'] = level_one_jobs['Job Title'].str.replace(' occupations', '')
level_one_jobs_titles = level_one_jobs['Job Title'].tolist()

level_two_industries = ind_df[(ind_df.Level == 2) &
                                (ind_df.occ_code.str.contains('-0000'))]

colorscale=[[1.0, 'rgb(165,0,38)'], [0.0, 'rgb(49,54,149)']]

font_colors = ['#efecee', '#3c3636', '#efecee']


layout = html.Div([
    html.Div([
        html.H3('Heatmap App'),
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
    - Use the heatmap to find high or low growth occupation and industry areas.
    - Click on any cell in the heatmap to expand further occupations in that category.
    - *More functionality forthcoming*
            '''),
            ],
            id='heatmap_instructions',
            style={'margin-left': '50', 'margin-right': '50', 'padding-bottom':'20'}
        ),
        html.Div([
            dcc.Dropdown(
                id='changes',
                options=[
                    {'label': i, 'value': i} for i in ['Change (%)', 'Change (#)']
                ],
                value='Change (%)',
                multi=False,
                clearable=False
            ),
        ], style={'width':'30%'}),
        html.Div([
            dcc.Graph(
                id='heatmap',
                config={'displayModeBar': False}
            ),
        ]),
        html.Div([
            dcc.Tabs(
                tabs=[
                    {'label': i, 'value': i} for i in ['Heatmap - One Level Lower', 'Occupations', 'Industries']
                ],
                value='Occupations',
                id='tabs',
                vertical=False,
                style={
                    'borderBottom': 'thin lightgrey solid',
                    'textAlign': 'center',
                    'paddingTop': '5px',
                    'paddingRight': '250',
                    'paddingLeft': '250'
                }
            ),
            html.Div([
                html.Div(
                    id='heatmap-selection',
                ),
            ], id='SELECTION',),
            html.Div([
                dcc.Graph(
                    id='heatmap_2',
                    config={'displayModeBar': False}
                ),
            ], id='HEATMAP_HEATMAP'),
            html.Div([
                dt.DataTable(
                    rows=[{}],

                    #optional - sets the order of columns
                    columns=ind_display_columns,

                    row_selectable=False,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    editable=False,
                    min_height=280,
                    column_widths=[50, 250, 120, 120, 140, 120, 120, 130, 80, 80],
                    row_height=25,
                    header_row_height=35,
                    id='HEATMAP_industry_datatable'
                ),
                html.Div(id='ind_selected-indexes', style={'padding-bottom': 20}),
            ], id='HEATMAP_INDUSTRIES'
            ),
            html.Div([
                dt.DataTable(
                    rows=[{}],

                    #optional - sets the order of columns
                    columns=display_columns,

                    row_selectable=False,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    editable=False,
                    min_height=280,
                    column_widths=[50, 275, 120, 120, 65, 65, 85, 85, 75, 90, 70],
                    row_height=25,
                    header_row_height=35,
                    id='HEATMAP_job_datatable'
                ),
                html.Div(id='selected-indexes', style={'padding-bottom': 20}),
            ], id='HEATMAP_OCCUPATIONS'
            ),
        ],
        style={'width': '100%', 'font-size': 12, 'padding-bottom': 20, 'padding-top': 20}),

        html.Div(id='output')

    ],style={'textAlign': 'left', 'margin-left': '30', 'margin-right': '30'}),

])



@app.callback(
    Output('heatmap_instructions', 'style'),
    [Input('toggle', 'value')])
def toggle_container(toggle_value):
    if toggle_value == 'Show Instructions':
        return {'display': 'block', 'borderBottom': 'thin lightgrey solid',
                'borderTop': 'thin lightgrey solid', 'font-size': 15}
    else:
        return {'display': 'none'}


@app.callback(
    Output('HEATMAP_INDUSTRIES', 'style'),
    [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Industries':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('HEATMAP_OCCUPATIONS', 'style'),
    [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Occupations':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('HEATMAP_HEATMAP', 'style'),
    [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Heatmap - One Level Lower':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(
    Output('SELECTION', 'style'),
    [Input('heatmap', 'clickData')])
def toggle_container(clickData):
    if clickData:
        return {'display': 'block',
                'font-size': 18, 'textAlign': 'left', 'padding-top': 25}
    else:
        return {'display': 'none'}


@app.callback(
    Output('heatmap', 'figure'),
    [Input('changes', 'value')])
def update_selected_row_indices(value):

    heatmap = pd.pivot_table(level_two_industries, index='Title', columns='occ_code',
                            values=value)

    heatmap.drop('00-0000', axis=1, inplace=True)
    heatmap.columns = level_one_jobs_titles

    z = heatmap.values.tolist()
    x = heatmap.columns.tolist()
    y = heatmap.index.tolist()
    z_text = []
    max_val = heatmap.max().max()
    for i in z:
        line = [str(j) for j in i]
        z_text.append(line)

    fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text,
                                colorscale=colorscale, font_colors=font_colors)
    fig.data.update({'zmin': -max_val, 'zmax': max_val})
    fig.layout.update({'margin': {'l':300, 'r':0, 't':200, 'b':0}})
    fig.layout.update({'autosize': True, 'height': 500})
    fig.layout.xaxis.update({'title': 'Occupation'})
    fig.layout.yaxis.update({'title': 'Industry'})
    for i in range(len(fig.layout.annotations)):
        fig.layout.annotations[i].font.size = 8

    return fig


@app.callback(
    Output('HEATMAP_job_datatable', 'rows'),
    [Input('heatmap', 'clickData')])
def update_selected_row_indices(clickData):
    if clickData:
        for point in clickData['points']:
            code = df[df['Job Title'] == point['x'] + ' occupations']['code'].values[0]
            code = code.replace('0000', '')
            rows = df[(df.code.str.contains(code)) & (df.Level > 1)]
    return rows[display_columns].to_dict('records')


@app.callback(
    Output('HEATMAP_industry_datatable', 'rows'),
    [Input('heatmap', 'clickData')])
def update_selected_row_indices(clickData):
    if clickData:
        for point in clickData['points']:
            code = IA_df[IA_df['Title'] == point['y']]['Code'].values[0]
            code = code[:2]
            rows = IA_df[(IA_df['Code'].str.startswith(code)) & (IA_df.Level > 2)]
    return rows[ind_display_columns].to_dict('records')


@app.callback(
    Output('heatmap-selection', 'children'),
    [Input('heatmap', 'clickData')])
def update_selected_row_indices(clickData):
    if clickData:
        for point in clickData['points']:
            selected_job = point['x']
            selected_industry = point['y']

    return html.Div([
        html.Div([html.P("Selected Industry: {}".format(selected_industry))],
            className="six columns", style={'textAlign': 'center'}
        ),
        html.Div([html.P("Selected Job: {}".format(selected_job))],
            className="six columns", style={'textAlign': 'center'}
        )
    ],
    className="row", style={'borderBottom': 'thin lightgrey solid',
                                'padding-bottom': 10})

@app.callback(
    Output('heatmap_2', 'figure'),
    [Input('heatmap', 'clickData')],
    [State('changes', 'value')])
def update_selected_row_indices(clickData, value):
    if clickData:
        for point in clickData['points']:
            job_code = df[df['Job Title'] == point['x'] + ' occupations']['code'].values[0]
            job_code = job_code.replace('0000', '')

            ind_code = ind_df[ind_df['Title'] == point['y']]['Code'].values[0]
            ind_code = ind_code[:2]

        sub_jobs = df[(df.code.str.contains(job_code)) & (df.Level == 3)]
        sub_jobs_list = sub_jobs['code'].tolist()
        sub_jobs_columns = sub_jobs['Job Title'].tolist()

        level_three_industries = ind_df[(ind_df.Level == 3) &
                                        (ind_df['occ_code'].isin(sub_jobs_list)) &
                                        (ind_df['Code'].str.startswith(ind_code))]
        heatmap_2 = pd.pivot_table(level_three_industries, index='Title',
                                    columns='occ_code', values=value)
        columns = df[df.code.isin(heatmap_2.columns.tolist())]
        columns = columns['Job Title'].tolist()
        heatmap_2.columns = columns

        z = heatmap_2.values.tolist()
        x = heatmap_2.columns.tolist()
        y = heatmap_2.index.tolist()
        z_text = []
        max_val = heatmap_2.max().max()
        for i in z:
            line = [str(j) for j in i]
            z_text.append(line)

        fig = ff.create_annotated_heatmap(z, x=x, y=y, annotation_text=z_text,
                                            colorscale=colorscale, font_colors=font_colors)
        fig.layout.update({'margin': {'l':500, 'r':0, 't':200, 'b':0}})
        fig.data.update({'zmin': -max_val, 'zmax': max_val})
        fig.layout.update({'autosize': True})
        fig.layout.xaxis.update({'title': 'Occupations'})
        fig.layout.yaxis.update({'title': 'Industries'})
        for i in range(len(fig.layout.annotations)):
            fig.layout.annotations[i].font.size = 8

        return fig

    return None

app.scripts.append_script({'external_url': 'https://cdn.rawgit.com/slaytor/Projects/ba3e394f/gtag.js'})
