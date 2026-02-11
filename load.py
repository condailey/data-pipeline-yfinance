"""
Date: 02/10/2026
Author: Connor Dailey

load.py - Local load script for stock market data.

Reads cleaned CSV files from the data/ directory and inserts
them into a local PostgreSQL database. Uses a composite primary
key (ticker_name, stock_date) to prevent duplicate entries.
"""

import psycopg2
import pandas as pd

# Connect to local PostgreSQL
conn = psycopg2.connect(dbname="stock_data", user="condailey", host="localhost")
cur = conn.cursor()

tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Load each ticker's CSV and insert into the database
for ticker in tickers:
    df = pd.read_csv(f'data/{ticker}_raw_data.csv')
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO STOCK_DATA (ticker_name, stock_date, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ticker_name, stock_date) DO NOTHING;
        """, (ticker, row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))

# Commit all inserts and close the connection
conn.commit()
cur.close()
conn.close()
