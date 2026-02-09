import yfinance as yf
import pandas as pd

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Fetch historical data for each ticker
for ticker in tickers:
    stock = yf.Ticker(ticker)
    data = stock.history(period="10y", interval="1d", auto_adjust=False)
    cleaned_data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    rounded_data = cleaned_data.round(3) 
    rounded_data.to_csv(f'data/{ticker}_raw_data.csv')
