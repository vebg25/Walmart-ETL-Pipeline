import json
import boto3
from datetime import datetime
import os
import requests

def lambda_handler(event, context):
    rapid_api_key=os.environ.get('rapid_api_key')
    url = "https://walmart-data.p.rapidapi.com/walmart-serp.php"
    querystring = {"url":"https://www.walmart.com/search?q=one+plus+phones"}
    headers = {"x-rapidapi-key": rapid_api_key,"x-rapidapi-host": "walmart-data.p.rapidapi.com"}
    response = requests.get(url, headers=headers, params=querystring)
    # BOTO3 to put in S3
    filename = 'walmart_raw_' + str(datetime.now()) + '.json'
    client= boto3.client('s3')
    client.put_object(Body=json.dumps(response.json()),Bucket='walmart-aws-1-bucket',Key=f'raw_data/to_processed/{filename}')