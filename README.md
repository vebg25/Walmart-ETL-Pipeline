# Walmart ETL Pipeline

## Architectural Diagram of Walmart ETL pipeline
![](https://github.com/vebg25/Walmart-ETL-Pipeline/blob/main/Walmart%20ETL%20pipeline.png)

## Key Points explaining the architecture of the ETL pipeline

### 1.    _**Amazon CloudWatch**_-   It triggers an AWS Lambda function to initiate data extraction.

### 2.    _**AWS Lambda (Extract Phase)**_-   AWS CloudWatch triggers this function and it extracts raw data from the Walmart API based on a given query.

### 3.    _**Amazon S3 (Storage for Raw Data)**_-  It stores the raw data extracted by the Lambda function.

### 4.    _**AWS Lambda (Transform Phase)**_-   This function transforms raw data into a more organized CSV format.

### 5.    _**Amazon S3 (Storage for Transformed Data)**_-   It stores the transformed data in CSV format extracted by the Lambda function.

### 6.    _**Snowpipe (Load Phase)**_-   This is used to load the transformed CSV data from S3 into Snowflake DB.

### 7.    _**Snowflake DB**_-   It stores the final processed data for analytics and querying using SQL.
