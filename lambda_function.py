import boto3                                                                                                                                                                                                                 
import yfinance as yf                                                                                                                                                                                                        
import pandas as pd                                                                                                                                                                                                          
                                                                                                                                                                                                                               
def lambda_handler(event, context):                   
    tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA']
    s3 = boto3.client('s3')

    for ticker in tickers:
        stock = yf.Ticker(ticker)
        data = stock.history(period="10y", interval="1d", auto_adjust=False)
        cleaned_data = data[['Open', 'High', 'Low', 'Close', 'Volume']]
        rounded_data = cleaned_data.round(3) 
        csv_buffer = rounded_data.to_csv(index=True)
        s3.put_object(Bucket='condailey-stock-data', Key=f'{ticker}_raw_data.csv', Body=csv_buffer)