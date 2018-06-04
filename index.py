from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import dash_table_experiments as dt


from app import app, server
from apps import home, jobs_app, ind_app, heatmap_app
from header_footer import header, footer

css = [
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/8485c028c19c393e9ab85e1a4fafd78c489609c2/dash-docs-base.css',
    'https://dl.dropboxusercontent.com/s/t8d6kluyt7y1sls/custom.css?dl=0',
    'https://fonts.googleapis.com/css?family=Dosis',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
]
js = ['https://cdn.rawgit.com/slaytor/Projects/ba3e394f/gtag.js']

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(dt.DataTable(rows=[{}]), style={'display': 'none'}),
    header,
    html.Div([
        html.Div(id='page-content'),
    ],
    className='content-container',
    style={'margin-left': '30', 'margin-right': '30'}),
    footer,
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
         return jobs_app.layout
    if pathname == '/apps/jobs_app':
         return jobs_app.layout
    elif pathname == '/apps/ind_app':
         return ind_app.layout
    elif pathname == '/apps/heatmap_app':
         return heatmap_app.layout
    else:
        return '404'

app.scripts.config.serve_locally = False
app.css.append_css({'external_url': css})
app.scripts.append_script({'external_url': js})


if __name__ == '__main__':
    app.run_server(debug=True)
