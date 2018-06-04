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

from header_footer import header, footer

css = [
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/8485c028c19c393e9ab85e1a4fafd78c489609c2/dash-docs-base.css',
    'https://dl.dropboxusercontent.com/s/t8d6kluyt7y1sls/custom.css?dl=0',
    'https://fonts.googleapis.com/css?family=Dosis',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
]
js = ['https://cdn.rawgit.com/slaytor/Projects/master/GA-1']

margins = {'l':40, 'r':40, 't':10, 'b':25}

df = pd.read_csv('data/job_data.csv')
ind_df = pd.read_csv('data/industries_database.csv')
ind_df = ind_df[ind_df.Level > 0]
certs_df = pd.read_csv('data/certs_data.csv')

display_columns = ['Level', 'Job Title', '2016 Employment', '2026 Employment',
                    '2016 %', '2026 %', 'Change (#)', 'Change (%)',
                    'Openings', 'Median Wage', 'code']

ind_display_columns = ['Level', 'Title', '2016 Employment', '2016 % of Industry', '2016 % of Occupation',
                        '2026 Employment', '2026 % of Industry', '2026 % of Occupation', 'Change (%)',
                        'Change (#)']

eds = ['—', 'No formal educational credential', 'High school diploma or equivalent',
        'Some college, no degree', "Associate's degree", "Bachelor's degree",
        "Master's degree", 'Postsecondary nondegree award',
        'Doctoral or professional degree']

exps = ['—', '5 years or more', 'Less than 5 years', 'None']

# Keep this out of source code repository - save in a file or a database
USER = os.environ.get("JOBS_APP_USER")
PASSWORD = os.environ.get("JOBS_APP_PASS")
VALID_USERNAME_PASSWORD_PAIRS = [
    [USER, PASSWORD]
]

app = dash.Dash('auth')
app.title = 'ODIE'
server = app.server
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

app.config.suppress_callback_exceptions = True
#app.scripts.config.serve_locally=True

app.layout = html.Div([
    header,
    html.Div([

        dcc.RadioItems(
            id='toggle',
            options=[{'label': i, 'value': i} for i in ['Show Instructions', 'Hide']],
            value='Hide',
            labelStyle={'display': 'inline-block'},
        ),
    ], style={'background-color': '#008080', 'color': '#FFFFFF',
                'margin-left': '30', 'margin-right': '30'}),
    html.Div([
        html.Div([
            # Enter instructions
            dcc.Markdown('''
        Welcome to the Occupational Trend Explorer!

        This tool allows you to filter data from the Bureau of Labor Statistics and other sources to identify job trends.

        How it works:
            - The data table at the top of the page contains Occupation data. All numerical data is in 1,000's (excluding %'s)
            - Use the dropdown filters at the top of the page to slice the data by major categoreis or features.
            - You can also click on the 'Filter Rows' button on the right and then filter any row in the data set.
                - Try using > or < to filter by size (ex. '>500')
                - Or filter Job Titles by text search (ex. 'computer')
            - As you filter the data, the chart below will update to display only the filtered subset
            - Clicking on any single row in the table, or the chart, will then bring up further industry-level data below.
                - This data can also be filtered by dropdown or using the 'Filter Rows' button

            '''),
            ],
            id='instructions'
        ),
        html.Div([

            html.Div([
                html.P('Filter by Job Categories or Individual Jobs'),
                dcc.Dropdown(
                    id='types',
                    options=[
                        {'label': i, 'value': i} for i in df.type.unique().tolist()
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
                        {'label': i, 'value': i} for i in df.Level.unique().tolist()
                    ],
                    value=[],
                    multi=True
                ),
            ],style={'width': '45%', 'float': 'right', 'padding-right': 25, 'font-size': 12}),

        ],style={'width': '50%', 'float': 'left', 'textAlign': 'left', 'padding-top': 15}),

        html.Div([

            html.Div([
                html.P('Filter by Education Required'),
                dcc.Dropdown(
                    id='educations',
                    options=[
                        {'label': i, 'value': i} for i in eds
                    ],
                    value=[],
                    multi=True
                ),
            ],style={'width': '45%', 'float': 'right', 'padding-right': 25, 'font-size': 12}),

            html.Div([
                html.P('Filter by Experience Required'),
                dcc.Dropdown(
                    id='experience',
                    options=[
                        {'label': i, 'value': i} for i in df.Experience.unique().tolist()
                    ],
                    value=[],
                    multi=True
                ),
            ],style={'width': '45%', 'float': 'left', 'padding-right': 25, 'font-size': 12}),

        ], style={'width': '50%', 'float': 'right', 'textAlign': 'left', 'padding-top': 15}),

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
                id='datatable'
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
                    id='graph',
                    config={'displayModeBar': False}
                ),
            ]),
        ],
        style={'width': '100%', 'margin-right': 'auto','font-size': 12, 'textAlign': 'left'}),

        html.Div([
            dcc.Tabs(
                tabs=[
                    {'label': i, 'value': i} for i in ['Industries', 'Certifications', 'Other']
                ],
                value='Industry',
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
                html.Div(id='table-container')
                ],
                id='CERTS',
                style={'paddingRight': '300', 'paddingLeft': '300'}
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
                    id='industry_datatable'
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
                    id='ind-graph',
                    config={'displayModeBar': False}
                ),
            ], id='IND_GRAPH')
        ],
        style={'width': '100%', 'font-size': 12, 'padding-bottom': 20}),

    footer

    ],
    style={'textAlign': 'left', 'margin-left': '30', 'margin-right': '30'})

], style={
    'fontFamily': 'Sans-Serif'
})



@app.callback(Output('instructions', 'style'), [Input('toggle', 'value')])
def toggle_container(toggle_value):
    if toggle_value == 'Show Instructions':
        return {'display': 'block', 'background-color': '#008080', 'color': '#FFFFFF',
                'font-size': 15}
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


# Filtering Logic with multiple filters
@app.callback(Output('datatable', 'rows'),
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
    Output('datatable', 'selected_row_indices'),
    [Input('graph', 'clickData')],
    [State('datatable', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices


@app.callback(
    Output('graph', 'figure'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices'),
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

    fig.layout.update({'margin': {'l':200, 'r':200, 't':0, 'b':30}})
    fig.layout.update({'autosize': True, 'height': 225})
    #fig.layout.yaxis.update({'tickprefix': '%', 'hoverformat': '.1f'})
    fig.layout.xaxis.update({'showticklabels': False})

    return fig


@app.callback(
    Output('table-container', 'children'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices')])
def display_table(rows, selected_row_indices):
    if len(selected_row_indices) == 1:
        code = pd.DataFrame(rows).iloc[selected_row_indices[0]]['code']
        job = pd.DataFrame(rows).iloc[selected_row_indices[0]]['Job Title']
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
    Output('industry_datatable', 'rows'),
    [Input('datatable', 'rows'),
     Input('datatable', 'selected_row_indices'),
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
    Output('ind-graph', 'figure'),
    [Input('industry_datatable', 'rows'),
     Input('industry_datatable', 'selected_row_indices'),
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

        fig.layout.update({'margin': {'l':125, 'r':125, 't':0, 'b':30}})
        fig.layout.update({'autosize': True, 'width':1200, 'height': 225})
        fig.layout.xaxis.update({'showticklabels': False})

    else:
        fig.layout.update({'autosize': True, 'width':1200, 'height': 10})
        fig.layout.yaxis.update({'showticklabels': False})

    return fig



@app.callback(
    Output('industry_datatable', 'selected_row_indices'),
    [Input('ind-graph', 'clickData')],
    [State('industry_datatable', 'selected_row_indices')])
def update_selected_row_indices(clickData, selected_row_indices):
    if clickData:
        for point in clickData['points']:
            if point['pointNumber'] in selected_row_indices:
                selected_row_indices.remove(point['pointNumber'])
            else:
                selected_row_indices.append(point['pointNumber'])
    return selected_row_indices



app.css.append_css({'external_url': css})
app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=True)
