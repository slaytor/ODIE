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

from app import app, df, ind_df, certs_df, skills, tools, tech, display_columns, ind_display_columns, eds, exps


layout = html.Div([
    html.Div([
        html.H3('Jobs App'),
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
##### Filter Occupational data from the Bureau of Labor Statistics and other sources.

- How it works:
    - The data table at the top of the page contains Occupation data. All numerical data is in 1,000's (excluding %'s)
    - Use the dropdown filters at the top of the page to slice the data by major categories or features.
    - You can also click on the 'Filter Rows' button on the right and then filter any row in the data set.
        - Try using '>' or '<' to filter by size (ex. '>500')
        - Or filter Job Titles by text search (ex. 'computer')
    - As you filter the data, the chart below will update to display only the filtered subset
    - Clicking on any single row in the table, or the chart, will then bring up further industry-level data below.
        - This data can also be filtered by dropdown or using the 'Filter Rows' button

            '''),
            ],
            id='job_instructions',
            style={'margin-left': '100', 'margin-right': '100'}
        ),
        html.Div([

            html.Div([
                html.P('Type Filter'),
                dcc.Dropdown(
                    id='types',
                    options=[
                        {'label': i, 'value': i} for i in df.type.unique().tolist()
                    ],
                    value=[],
                    multi=True,
                    clearable=False
                ),
            ],
            className="three columns"),

            html.Div([
                html.P('Category Level Filter'),
                dcc.Dropdown(
                    id='level',
                    options=[
                        {'label': i, 'value': i} for i in df.Level.unique().tolist()
                    ],
                    value=[],
                    multi=True
                ),
            ],
            className="three columns"),
            html.Div([
                html.P('Education Filter'),
                dcc.Dropdown(
                    id='educations',
                    options=[
                        {'label': i, 'value': i} for i in eds
                    ],
                    value=[],
                    multi=True
                ),
            ],
            className="three columns"),
            html.Div([
                html.P('Experience Filter'),
                dcc.Dropdown(
                    id='experience',
                    options=[
                        {'label': i, 'value': i} for i in df.Experience.unique().tolist()
                    ],
                    value=[],
                    multi=True
                ),
            ],
            className="three columns"),

        ],
        className="row",
        style={'padding-top': 15, 'font-size': 12}),

    ],style={'textAlign': 'left', 'margin-left': '30', 'margin-right': '30'}),

    html.Div([
        html.Div([
            dt.DataTable(
                rows=df[display_columns].to_dict('records'),

                # optional - sets the order of columns
                columns=display_columns,

                row_selectable=True,
                filterable=True,
                sortable=True,
                selected_row_indices=[],
                editable=False,
                min_height=280,
                column_widths=[50, 275, 120, 120, 65, 65, 85, 85, 75, 90, 70],
                row_height=25,
                header_row_height=35,
                id='JA_datatable'
            ),
            html.Div(id='selected-indexes', style={'padding-bottom': 20}),
            dcc.RadioItems(
                id='radio-buttons',
                options=[{'label': j, 'value': j} for j in
                        ['2016 Employment', '2026 Employment', '2016 %', '2026 %',
                        'Change (#)', 'Change (%)', 'Openings', 'Median Wage']],
                value='Change (%)',
                labelStyle={'display': 'inline-block'},
                style={'textAlign': 'center', 'font-size': 14, 'margin-right': 5}
            ),
            html.Div([
                dcc.Graph(
                    id='JA_graph',
                    config={'displayModeBar': False}
                ),
            ]),
        ],
        style={'width': '100%', 'margin-right': 'auto','font-size': 12, 'textAlign': 'left'}),

        html.Div([
            dcc.Tabs(
                tabs=[
                    {'label': i, 'value': i} for i in ['Industries', 'Skills', 'Tools', 'Technology', 'Certifications']
                ],
                value='Industries',
                id='tabs',
                vertical=False,
                style={
                    'borderBottom': 'thin lightgrey solid',
                    'textAlign': 'center',
                    'paddingTop': '5px',
                    'paddingRight': '200',
                    'paddingLeft': '200'
                }
            ),
            html.Div([
                html.Div([
                    html.P('Filter by Industry Level'),
                    dcc.Dropdown(
                        id='ind-level',
                        options=[
                            {'label': i, 'value': i} for i in ind_df.Level.unique().tolist()
                        ],
                        value=[],
                        multi=True
                    ),
                ], style={'width': '20%', 'float': 'left', 'padding-right': 25, 'font-size': 12}),
                dt.DataTable(
                    rows=[{}],

                    #optional - sets the order of columns
                    columns=ind_display_columns,

                    row_selectable=True,
                    filterable=True,
                    sortable=True,
                    selected_row_indices=[],
                    editable=False,
                    min_height=280,
                    column_widths=[50, 250, 120, 120, 140, 120, 120, 130, 80, 80],
                    row_height=25,
                    header_row_height=35,
                    id='JA_industry_datatable'
                ),
                html.Div(id='ind_selected-indexes', style={'padding-bottom': 20}),
            ], id='INDUSTRIES'),
            html.Div([
                dcc.RadioItems(
                    id='ind-radio-buttons',
                    options=[{'label': j, 'value': j} for j in
                            ['2016 Employment', '2016 % of Industry', '2016 % of Occupation',
                            '2026 Employment', '2026 % of Industry', '2026 % of Occupation',
                            'Change (%)', 'Change (#)']],
                    value='Change (%)',
                    labelStyle={'display': 'inline-block'},
                    style={'textAlign': 'center', 'font-size': 14, 'margin-right': 5}
                ),
                dcc.Graph(
                    id='JA_ind_graph',
                    config={'displayModeBar': False}
                ),
            ], id='IND_GRAPH'),
            html.Div([
                html.Div(id='certs-table-container')
                ],
                id='CERTS',
                style={'paddingRight': '300', 'paddingLeft': '300'}
            ),
            html.Div([
                html.Div(id='skills-table-container')
                ],
                id='SKILLS',
                style={'paddingRight': '300', 'paddingLeft': '300'}
            ),
            html.Div([
                html.Div(id='tools-table-container')
                ],
                id='TOOLS',
                style={'paddingRight': '300', 'paddingLeft': '300'}
            ),
            html.Div([
                html.Div(id='tech-table-container')
                ],
                id='TECH',
                style={'paddingRight': '300', 'paddingLeft': '300'}
            ),
        ],
        style={'width': '100%', 'font-size': 12, 'padding-bottom': 20}),

    ],
    style={'textAlign': 'left', 'margin-left': '30', 'margin-right': '30'}),


])



@app.callback(Output('job_instructions', 'style'), [Input('toggle', 'value')])
def toggle_container(toggle_value):
    if toggle_value == 'Show Instructions':
        return {'display': 'block', 'borderBottom': 'thin lightgrey solid',
                'borderTop': 'thin lightgrey solid', 'font-size': 15}
    else:
        return {'display': 'none'}


@app.callback(Output('INDUSTRIES', 'style'),
              [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Industries':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('IND_GRAPH', 'style'),
              [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Industries':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('CERTS', 'style'),
              [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Certifications':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('SKILLS', 'style'),
              [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Skills':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('TOOLS', 'style'),
              [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Tools':
        return {'display': 'block'}
    else:
        return {'display': 'none'}

@app.callback(Output('TECH', 'style'),
              [Input('tabs', 'value')])
def toggle_container(tab_value):
    if tab_value == 'Technology':
        return {'display': 'block'}
    else:
        return {'display': 'none'}


# Filtering Logic with multiple filters
@app.callback(Output('JA_datatable', 'rows'),
              [Input('educations', 'value'),
               Input('types', 'value'),
               Input('experience', 'value'),
               Input('level', 'value')])
def update_rows(ed_, type_, exp_, lev_):
    # First, always filter by selected type
    dff = df[df.type.isin(type_)]
    if len(type_) == 0:
        dff = df.copy()
    # Set logic to list of True/False
    logic = [len(ed_) == 0, len(exp_) == 0, len(lev_) == 0]

    ##### No Filters
    if logic == [1,1,1]:
        return dff[display_columns].to_dict('records')

    ##### One Filter
    elif logic == [0,1,1]:
        dff = dff[dff.ed_needed.isin(ed_)]
        return dff[display_columns].to_dict('records')
    elif logic == [1,0,1]:
        dff = dff[dff.Experience.isin(exp_)]
        return dff[display_columns].to_dict('records')
    elif logic == [1,1,0]:
        dff = dff[dff.Level.isin(lev_)]
        return dff[display_columns].to_dict('records')

    ##### Two Filters
    elif logic == [0,0,1]:
        dff = dff[(dff.ed_needed.isin(ed_)) & (dff.Experience.isin(exp_))]
        return dff[display_columns].to_dict('records')
    elif logic == [0,1,0]:
        dff = dff[(dff.ed_needed.isin(ed_)) & (dff.Level.isin(lev_))]
        return dff[display_columns].to_dict('records')
    elif logic == [1,0,0]:
        dff = dff[(dff.Experience.isin(exp_)) & (dff.Level.isin(lev_))]
        return dff[display_columns].to_dict('records')

    ##### All Filters
    elif logic == [0,0,0]:
        dff = dff[(dff.ed_needed.isin(ed_)) & (dff.Experience.isin(exp_))
                    & (dff.Level.isin(lev_))]
        return dff[display_columns].to_dict('records')



# Disable the education dropdown if the type is job categories
@app.callback(
    Output('educations', 'value'),
    [Input('types', 'value')])
def disable_dropdown(value):
    if value == ['Job Categories']:
        return ['—']
    if value != ['Job Categories']:
        return []

@app.callback(
    Output('educations', 'disabled'),
    [Input('types', 'value')])
def disable_dropdown(value):
    if value == ['Job Categories']:
        return True
    if value != ['Job Categories']:
        return False

# Disable the experience dropdown if the type is job categories
@app.callback(
    Output('experience', 'value'),
    [Input('types', 'value')])
def disable_dropdown(value):
    if value == ['Job Categories']:
        return ['—']
    if value != ['Job Categories']:
        return []

@app.callback(
    Output('experience', 'disabled'),
    [Input('types', 'value')])
def disable_dropdown(value):
    if value == ['Job Categories']:
        return True
    if value != ['Job Categories']:
        return False


@app.callback(
    Output('JA_datatable', 'selected_row_indices'),
    [Input('JA_graph', 'clickData')],
    [State('JA_datatable', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('JA_graph', 'figure'),
    [Input('JA_datatable', 'rows'),
     Input('JA_datatable', 'selected_row_indices'),
     Input('radio-buttons', 'value')])
def update_figure(rows, selected_row_indices, radio_value):
    dff2 = pd.DataFrame(rows)[['Job Title', radio_value]]
    fig = plotly.tools.make_subplots(
        rows=1, cols=1,
        shared_xaxes=True)

    marker = {'color': ['teal']*len(dff2)}
    for i in (selected_row_indices or []):
        marker['color'][i] = '#FF851B'
    fig.append_trace({
        'x': dff2['Job Title'],
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
    Output('certs-table-container', 'children'),
    [Input('JA_datatable', 'rows'),
     Input('JA_datatable', 'selected_row_indices')])
def display_table(rows, selected_row_indices):
    if len(selected_row_indices) == 1:
        code = pd.DataFrame(rows).iloc[selected_row_indices[0]]['code']
        cert_codes = [x for x in certs_df['code'].unique().tolist()]
        if code in cert_codes:
            dff5 = certs_df[certs_df['code'] == code].sort_values('Job Postings',
                    ascending=False).drop('code', axis=1).to_dict('records')

            return dt.DataTable(
                rows=dff5,

                #optional - sets the order of columns
                #columns=ind_display_columns,

                row_selectable=False,
                filterable=True,
                sortable=True,
                selected_row_indices=[],
                editable=False,
                min_height=280,
                column_widths=[550, 225, 225, 200],
                row_height=25,
                header_row_height=35,
                id='certs_datatable'
            ),


@app.callback(
    Output('skills-table-container', 'children'),
    [Input('JA_datatable', 'rows'),
     Input('JA_datatable', 'selected_row_indices')])
def display_table(rows, selected_row_indices):
    if len(selected_row_indices) == 1:
        code = pd.DataFrame(rows).iloc[selected_row_indices[0]]['code']
        dff6 = skills[skills['O*NET-SOC Code'] == code][['Element Name', 'Data Value']]
        dff6 = dff6.groupby('Element Name').mean().sort_values('Data Value',
                                            ascending=False).reset_index()
        dff6.columns = ['Skill', 'Importance Value']

        return dt.DataTable(
            rows=dff6.to_dict('records'),

            #optional - sets the order of columns
            #columns=ind_display_columns,

            row_selectable=False,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            editable=False,
            min_height=280,
            column_widths=[400, 400],
            row_height=25,
            header_row_height=35,
            id='skills_datatable'
        ),


@app.callback(
    Output('tools-table-container', 'children'),
    [Input('JA_datatable', 'rows'),
     Input('JA_datatable', 'selected_row_indices')])
def display_table(rows, selected_row_indices):
    if len(selected_row_indices) == 1:
        code = pd.DataFrame(rows).iloc[selected_row_indices[0]]['code']
        ranks = tools[tools['O*NET-SOC Code'] == code][['T2 Example', 'T2 Type']]
        ranks = ranks.groupby('T2 Example').count().sort_values('T2 Type',
                                                    ascending=False).reset_index()
        ranks.columns = ['Tool', 'Importance']
        ranks['Importance'] = ranks['Importance'] / 10 * 10

        return dt.DataTable(
            rows=ranks.to_dict('records'),

            #optional - sets the order of columns
            #columns=ind_display_columns,

            row_selectable=False,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            editable=False,
            min_height=280,
            column_widths=[400, 400],
            row_height=25,
            header_row_height=35,
            id='tools_datatable'
        ),



@app.callback(
    Output('tech-table-container', 'children'),
    [Input('JA_datatable', 'rows'),
     Input('JA_datatable', 'selected_row_indices')])
def display_table(rows, selected_row_indices):
    if len(selected_row_indices) == 1:
        code = pd.DataFrame(rows).iloc[selected_row_indices[0]]['code']
        ranks = tech[tech['O*NET-SOC Code'] == code][['T2 Example', 'T2 Type']]
        ranks = ranks.groupby('T2 Example').count().sort_values('T2 Type',
                                                    ascending=False).reset_index()
        ranks.columns = ['Technology', 'Importance']
        ranks['Importance'] = ranks['Importance'] / 10 * 10

        return dt.DataTable(
            rows=ranks.to_dict('records'),

            #optional - sets the order of columns
            #columns=ind_display_columns,

            row_selectable=False,
            filterable=True,
            sortable=True,
            selected_row_indices=[],
            editable=False,
            min_height=280,
            column_widths=[400, 400],
            row_height=25,
            header_row_height=35,
            id='tech_datatable'
        ),



@app.callback(
    Output('JA_industry_datatable', 'rows'),
    [Input('JA_datatable', 'rows'),
     Input('JA_datatable', 'selected_row_indices'),
     Input('ind-level', 'value')])
def update_ind_rows(rows, selected_row_indices, level):
    if len(selected_row_indices) == 0 or len(selected_row_indices) > 1:
        return [{}]
    title = pd.DataFrame(rows).ix[selected_row_indices]['code'].tolist()
    dff3 = ind_df[ind_df['occ_code'] == title[0]]
    dff3.drop_duplicates(inplace=True, subset='Title')
    if len(level) > 0:
        dff3 = dff3[dff3.Level.isin(level)]
    return dff3[ind_display_columns].sort_values('2016 Employment', ascending=False).to_dict('records')



@app.callback(
    Output('JA_ind_graph', 'figure'),
    [Input('JA_industry_datatable', 'rows'),
     Input('JA_industry_datatable', 'selected_row_indices'),
     Input('ind-radio-buttons', 'value')])
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
    Output('JA_industry_datatable', 'selected_row_indices'),
    [Input('JA_ind_graph', 'clickData')],
    [State('JA_industry_datatable', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


app.scripts.append_script({'external_url': 'https://cdn.rawgit.com/slaytor/Projects/ba3e394f/gtag.js'})
