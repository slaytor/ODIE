import dash_core_components as dcc
import dash_html_components as html

header = html.Div(
   className='header',
   children=html.Div(
       className='container-width',
       style={'height': '100%'},
       children=[
           html.Div(className='title', children=[
               html.H4('ODIE - Occupational Data Interactive Explorer'),
           ], style={'float': 'left'}),
           html.Div(className='links', children=[
               #dcc.Link(html.A('Home', className='link'), href='/', style={'padding-right':20}),
               dcc.Link(html.A('Jobs', className='link'), href='/apps/jobs_app', style={'padding-right':20}),
               dcc.Link(html.A('Industries', className='link'), href='/apps/ind_app', style={'padding-right':20}),
               dcc.Link(html.A('Heatmap', className='link'), href='/apps/heatmap_app', style={'padding-right':20}),
           ], style={'float': 'right'})
       ]
   )
)

footer = html.Div([
    html.Div([
    ], style={'background-color': '#001f3f', 'color': '#FFFFFF', 'height': 20}
    ),
    html.Div([
        html.P('For questions contact: '),
        html.P('Sam Taylor'),
        html.P('sataylor@wiley.com')
    ], style={"font-size": 14, 'textAlign': 'center', 'background-color': '#008080',
                'color': '#FFFFFF'})
])
