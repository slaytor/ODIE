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

from app import app

css = [
    'https://cdn.rawgit.com/plotly/dash-app-stylesheets/8485c028c19c393e9ab85e1a4fafd78c489609c2/dash-docs-base.css',
    'https://dl.dropboxusercontent.com/s/t8d6kluyt7y1sls/custom.css?dl=0',
    'https://fonts.googleapis.com/css?family=Dosis',
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css'
]
js = ['https://cdn.rawgit.com/slaytor/Projects/master/GA-1']

layout = html.Div([
    html.H3('Home App'),
    ])


app.css.append_css({'external_url': css})
app.scripts.append_script({'external_url': js})
