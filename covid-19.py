import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import requests

# Initialize Dash app
app = dash.Dash(__name__)

# Fetch COVID-19 Data
def get_covid_data():
    url = 'https://disease.sh/v3/covid-19/historical/all?lastdays=all'
    response = requests.get(url).json()
    
    # Extract time series data
    dates = list(response['cases'].keys())
    cases = list(response['cases'].values())
    deaths = list(response['deaths'].values())
    recovered = list(response['recovered'].values())
    
    # Create DataFrame
    df = pd.DataFrame({'Date': dates, 'Cases': cases, 'Deaths': deaths, 'Recovered': recovered})
    df['Date'] = pd.to_datetime(df['Date'])
    return df

# Layout
app.layout = html.Div([
    html.H1("Interactive COVID-19 Dashboard", style={'textAlign': 'center'}),
    
    # COVID-19 Graphs
    html.H3("COVID-19 Cases Over Time"),
    dcc.Graph(id='covid-cases-graph'),
    
    html.H3("COVID-19 Deaths Over Time"),
    dcc.Graph(id='covid-deaths-graph'),
    
    html.H3("COVID-19 Recovered Cases Over Time"),
    dcc.Graph(id='covid-recovered-graph'),
])

# Callbacks
@app.callback(
    Output('covid-cases-graph', 'figure'),
    [Input('covid-cases-graph', 'id')]
)
def update_covid_cases_chart(_):
    df = get_covid_data()
    fig = px.line(df, x='Date', y='Cases', title='COVID-19 Cases Over Time')
    return fig

@app.callback(
    Output('covid-deaths-graph', 'figure'),
    [Input('covid-deaths-graph', 'id')]
)
def update_covid_deaths_chart(_):
    df = get_covid_data()
    fig = px.line(df, x='Date', y='Deaths', title='COVID-19 Deaths Over Time')
    return fig

@app.callback(
    Output('covid-recovered-graph', 'figure'),
    [Input('covid-recovered-graph', 'id')]
)
def update_covid_recovered_chart(_):
    df = get_covid_data()
    fig = px.line(df, x='Date', y='Recovered', title='COVID-19 Recovered Cases Over Time')
    return fig

# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
