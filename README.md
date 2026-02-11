# Stock Data Pipeline

## Overview
An automated ETL pipeline that extracts daily stock data for AAPL, MSFT, GOOGL, AMZN, and TSLA
using the yfinance API, transforms and loads it into a PostgreSQL database hosted on AWS RDS, and
stores raw CSV files in S3. The pipeline runs serverlessly on AWS Lambda, triggered on a daily
schedule by EventBridge after market close, with CloudWatch monitoring and SNS email alerts for
error handling.

## Architecture
1. **EventBridge** triggers the Lambda function every weekday at 5:00 PM EST (one hour after market close to ensure data accuracy)
2. **Lambda** pulls daily stock data via yfinance, cleans and rounds the data
3. **S3** stores cleaned CSV files and **RDS** stores the data in a PostgreSQL database
4. **CloudWatch** monitors Lambda executions and tracks error metrics
5. **SNS** sends email alerts if the Lambda function fails

## Tech Stack
- Python 3.13
- PostgreSQL 17
- AWS (S3, Lambda, RDS, EventBridge, CloudWatch, SNS, IAM)
- yfinance API
- Docker (for building Lambda deployment packages)
- Claude Code (AI pair programming)

## Project Structure
- `extract.py` — Local extraction script that pulls stock data from yfinance, saves to CSV, and uploads to S3
- `load.py` — Local load script that reads CSV files and inserts data into PostgreSQL
- `lambda_function.py` — Lambda function that combines extract and load steps to run serverlessly in AWS
- `schema.sql` — PostgreSQL table definition for the stock_data table
- `requirements.txt` — Python dependencies for the Lambda deployment package

## AWS Services
| Service | Purpose |
|---------|---------|
| S3 | Stores raw CSV files for each ticker |
| Lambda | Runs the extract and load pipeline serverlessly |
| RDS | Hosts the PostgreSQL database in the cloud |
| EventBridge | Schedules the Lambda to run every weekday after market close |
| CloudWatch | Monitors Lambda logs, metrics, and triggers alarms on errors |
| SNS | Sends email notifications when the CloudWatch alarm fires |
| IAM | Manages permissions for the pipeline user and Lambda execution role |

## Database Schema
```sql
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
```

## Setup
1. Clone the repository
2. Install Python dependencies: `pip install -r requirements.txt`
3. Configure AWS CLI with appropriate IAM credentials
4. Create an S3 bucket for storing CSV files
5. Create an RDS PostgreSQL instance and run `schema.sql` to create the table
6. Build the Lambda deployment package using Docker (linux/arm64)
7. Deploy the Lambda function and set environment variables for database connection (DB_HOST, DB_NAME, DB_USER, DB_PASSWORD)
8. Create an EventBridge rule with a cron schedule to trigger the Lambda function
9. Set up CloudWatch alarms and SNS topic for error notifications

## What I Learned
- IAM permissions and the principle of least privilege
- Cron expressions for scheduling automated workflows
- VPC networking and security groups for database access
- Lambda deployment packaging with Docker
- Connecting cloud services end-to-end (EventBridge → Lambda → S3 + RDS)

## Future Improvements
- Support for configurable ticker lists
- Batch inserts for improved database performance
- Metabase dashboard for data visualization
- Error handling per ticker to prevent single-point failures
- AWS Secrets Manager for credential management
