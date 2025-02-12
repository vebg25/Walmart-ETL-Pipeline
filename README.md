# Walmart ETL Pipeline

## Architectural Diagram of Walmart ETL pipeline
![](https://github.com/vebg25/Walmart-ETL-Pipeline/blob/main/Walmart%20ETL%20pipeline.png)

## Key Points explaining the architecture of the ETL pipeline

## 1. ### Amazon CloudWatch:- It triggers an AWS Lambda function to initiate data extraction.
## 2. ### AWS Lambda (Extract Phase):- AWS CloudWatch triggers this function and it extracts raw data from the Walmart API based on a given query.
## 3. ### Amazon S3 (Storage for Raw Data):- It stores the raw data extracted by the Lambda function.
## 4. ### AWS Lambda (Transform Phase):- This function transforms raw data into a more organized CSV format.
## 5. ### Amazon S3 (Storage for Transformed Data):- It stores the transformed data in CSV format extracted by the Lambda function.
## 6. ### Snowpipe (Load Phase):- This is used to load the transformed CSV data from S3 into Snowflake DB.
## 7. ### Snowflake DB:- It stores the final processed data for analytics and querying using SQL.
