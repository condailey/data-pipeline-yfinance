/* SQL schema for stock data */

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