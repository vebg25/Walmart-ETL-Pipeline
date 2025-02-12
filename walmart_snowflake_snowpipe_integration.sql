CREATE DATABASE snowflake_database;
use snowflake_database;

CREATE OR REPLACE storage integration s3_init
    TYPE=EXTERNAL_STAGE
    STORAGE_PROVIDER=S3
    ENABLED=TRUE
    STORAGE_AWS_ROLE_ARN='arn:aws:iam::703671895332:role/walmart-manager-role'
    STORAGE_ALLOWED_LOCATIONS=('s3://walmart-aws-1-bucket/transformed_data/walmart_data/')

CREATE OR REPLACE TABLE product_searched(
    title STRING,
    image STRING,
    currentPrice STRING,
    rawPrice STRING,
    reviewsCount INTEGER,
    ratings DECIMAL,
    shippingMessage STRING,
    isBestSeller BOOLEAN,
    outOfStock BOOLEAN    
);

CREATE OR REPLACE FILE FORMAT csv_file_format
TYPE = CSV
FIELD_OPTIONALLY_ENCLOSED_BY = '"'
SKIP_HEADER = 1
ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE
NULL_IF = ('', 'NULL');

CREATE OR REPLACE STAGE loading_data
    URL='s3://walmart-aws-1-bucket/transformed_data/walmart_data/'
    STORAGE_INTEGRATION=s3_init
    FILE_FORMAT = csv_file_format

LIST @loading_data;


CREATE OR REPLACE PIPE product_pipe
auto_ingest=True
AS
COPY INTO snowflake_database.PUBLIC.product_searched
FROM @snowflake_database.PUBLIC.loading_data
FILE_FORMAT=(FORMAT_NAME=csv_file_format,ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE);

DESC pipe product_pipe;
SELECT SYSTEM$PIPE_STATUS('product_pipe');

SELECT * FROM product_searched;


