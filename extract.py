"""
Date: 02/10/2026
Author: Connor Dailey

extract.py - Local extraction script for stock market data.

Pulls 10 years of daily historical stock data from yfinance,
cleans and rounds the data, saves to local CSV files, and
uploads to S3 for cloud storage.
"""

import yfinance as yf
import boto3

# Tickers to extract data for
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

s3 = boto3.client('s3')

for ticker in tickers:
    # Pull 10 years of daily stock data with unadjusted prices
    stock = yf.Ticker(ticker)
    data = stock.history(period="10y", interval="1d", auto_adjust=False)

    # Keep only relevant price and volume columns
    cleaned_data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
    rounded_data = cleaned_data.round(3)

    # Save locally and upload to S3
    rounded_data.to_csv(f'data/{ticker}_raw_data.csv')
    s3.upload_file(f'data/{ticker}_raw_data.csv', 'condailey-stock-data', f'{ticker}_raw_data.csv')
