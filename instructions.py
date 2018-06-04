import dash_core_components as dcc
import dash_html_components as html

app.config.suppress_callback_exceptions = True

job_instructions = html.Div([
    # Enter instructions
    dcc.Markdown('''
##### Filter Occupational data from the Bureau of Labor Statistics and other sources.

- How it works:
- The data table at the top of the page contains Occupation data. All numerical data is in 1,000's (excluding %'s)
- Use the dropdown filters at the top of the page to slice the data by major categoreis or features.
- You can also click on the 'Filter Rows' button on the right and then filter any row in the data set.
- Try using '>' or '<' to filter by size (ex. '>500')
- Or filter Job Titles by text search (ex. 'computer')
- As you filter the data, the chart below will update to display only the filtered subset
- Clicking on any single row in the table, or the chart, will then bring up further industry-level data below.
- This data can also be filtered by dropdown or using the 'Filter Rows' button

    '''),
    ],
    id='instructions'
),
