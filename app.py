import dash
import dash_auth
import os
import pandas as pd

############ JOBS APP VARS ############
df = pd.read_csv('data/job_data.csv')
ind_df = pd.read_csv('data/industries_database.csv')
ind_df = ind_df[ind_df.Level > 0]
certs_df = pd.read_csv('data/certs_data.csv')
skills = pd.read_csv('data/skills.csv')
tat = pd.read_csv('data/tat.csv')
tools = tat[tat['T2 Type'] == 'Tools']
tech = tat[tat['T2 Type'] == 'Technloogy']

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

############ INDUSTRY APP VARS ############
IA_df = pd.read_csv('data/industries_data.csv')
IA_df = IA_df.drop_duplicates(subset='Title').sort_values('Level')
IA_df = IA_df[IA_df.Level > 1]
job_df = pd.read_csv('data/industries_database_2.csv')
job_df = job_df[job_df.Level > 0]

levels = [2,3,4,5,6]

IA_display_columns = ['Level', 'Title', '2016 Employment', '2016 % of Industry', '2016 % of Occupation',
                        '2026 Employment', '2026 % of Industry', '2026 % of Occupation', 'Change (%)',
                        'Change (#)', 'Code']

IA_job_display_columns = ['Level', 'Title', '2016 Employment', '2016 % of Industry',
                        '2016 % of Occupation', '2026 Employment', '2026 % of Industry',
                        '2026 % of Occupation', 'Change (#)', 'Change (%)']



# Keep this out of source code repository - save in a file or a database
#USER = os.environ.get("JOBS_APP_USER")
#PASSWORD = os.environ.get("JOBS_APP_PASS")
#VALID_USERNAME_PASSWORD_PAIRS = [
#    [USER, PASSWORD]
#]

app = dash.Dash()
app.title = 'ODIE'
server = app.server

#auth = dash_auth.BasicAuth(
#    app,
#    VALID_USERNAME_PASSWORD_PAIRS
#)

app.config.suppress_callback_exceptions = True
