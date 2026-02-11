/*
   Date: 02/10/2026
   Author: Connor Dailey

   schema.sql - PostgreSQL table definition for stock market data.

   Composite primary key (ticker_name, stock_date) ensures
   one record per ticker per trading day and prevents duplicates.
*/

CREATE TABLE stock_data (
    ticker_name VARCHAR,
    stock_date DATE,
    open_price DECIMAL(10, 3),
    high_price DECIMAL(10, 3),
    low_price DECIMAL(10, 3),
    close_price DECIMAL(10, 3),
    volume BIGINT,
    PRIMARY KEY (ticker_name, stock_date)
);
