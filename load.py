import psycopg2
import pandas as pd

#PGSQL connection parameters
conn = psycopg2.connect(dbname="stock_data", user="condailey",host="localhost")

# Create a cursor object to interact with the database
cur = conn.cursor()

# List of tickers to load data for
tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']

# Load data from CSV files and insert into the database
for ticker in tickers:
    df = pd.read_csv(f'data/{ticker}_raw_data.csv')
    for index, row in df.iterrows():
        cur.execute("""
            INSERT INTO STOCK_DATA (ticker_name, stock_date, open_price, high_price, low_price, close_price, volume)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (ticker_name, stock_date) DO NOTHING;
        """, (ticker, row['Date'], row['Open'], row['High'], row['Low'], row['Close'], row['Volume']))

# Commit the transaction and close the connection
conn.commit()
cur.close()
conn.close()