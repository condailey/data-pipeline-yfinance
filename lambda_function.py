"""
Date: 02/10/2026
Author: Connor Dailey

lambda_function.py - AWS Lambda handler for the stock data pipeline.

Extracts daily stock data from yfinance, uploads CSV files to S3,
and loads the data into a PostgreSQL database on RDS.
Triggered daily by EventBridge after market close.
"""

import boto3
import yfinance as yf
import psycopg2
import os


def lambda_handler(event, context):
    """Main Lambda entry point. Extracts stock data, uploads to S3, and loads into RDS."""

    # Connect to RDS PostgreSQL using environment variables
    conn = psycopg2.connect(
        host=os.environ["DB_HOST"],
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ["DB_NAME"],
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"]
    )

    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    s3 = boto3.client('s3')

    for ticker in tickers:
        # Pull 10 years of daily stock data with unadjusted prices
        stock = yf.Ticker(ticker)
        data = stock.history(period="10y", interval="1d", auto_adjust=False)

        # Keep only relevant price and volume columns
        cleaned_data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        rounded_data = cleaned_data.round(3)

        # Upload CSV to S3
        csv_buffer = rounded_data.to_csv(index=True)
        s3.put_object(Bucket='condailey-stock-data', Key=f'{ticker}_raw_data.csv', Body=csv_buffer)

        # Insert each row into RDS, skipping duplicates via composite primary key
        for index, row in rounded_data.iterrows():
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO STOCK_DATA (ticker_name, stock_date, open_price, high_price, low_price, close_price, volume)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (ticker_name, stock_date) DO NOTHING;
                """, (ticker, index, float(row['Open']), float(row['High']), float(row['Low']), float(row['Close']), int(row['Volume'])))

    # Commit all inserts and close the connection
    conn.commit()
    conn.close()
