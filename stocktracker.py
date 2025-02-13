import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import yfinance as yf

# Initialize Dash app
app = dash.Dash(__name__)

# List of Top 20 Stocks by Market Cap (as of recent data)
top_20_stocks = [
    'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'NVDA', 'BRK-B', 'META', 'V', 'JNJ',
    'WMT', 'JPM', 'PG', 'UNH', 'HD', 'DIS', 'PYPL', 'VZ', 'NFLX', 'KO'
]

# Fetch Stock Data
def get_stock_data(ticker='AAPL'):
    stock = yf.Ticker(ticker)
    hist = stock.history(period='6mo')
    hist.reset_index(inplace=True)
    
    # Calculate Bollinger Bands
    hist['MA20'] = hist['Close'].rolling(window=20).mean()
    hist['Upper'] = hist['MA20'] + (hist['Close'].rolling(window=20).std() * 2)
    hist['Lower'] = hist['MA20'] - (hist['Close'].rolling(window=20).std() * 2)
    return hist

# Layout
app.layout = html.Div([
    html.H1("Interactive Stock Tracker", style={'textAlign': 'center'}),
    
    # Stock Selection
    html.H3("Select Stock"),
    dcc.Dropdown(
        id='stock-dropdown',
        options=[{'label': ticker, 'value': ticker} for ticker in top_20_stocks],
        value='AAPL',
        clearable=False
    ),
    
    # Stock Graph
    dcc.Graph(id='stock-graph'),
])

# Callback for updating stock graph
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('stock-dropdown', 'value')]
)
def update_stock_chart(selected_stock):
    df = get_stock_data(selected_stock)
    fig = px.line(df, x='Date', y=['Close', 'Upper', 'Lower'], title=f'{selected_stock} Stock Prices with Bollinger Bands')
    return fig

# Run App
if __name__ == '__main__':
    app.run_server(debug=True)
