import json
import boto3
import os
from io import StringIO
import pandas as pd
from datetime import datetime
def transform_data(response):
    output_data_formatted = []
    products = response.get('body', {}).get('products', [])
    for product in products:
        temp_list = [
            product.get('title'),
            product.get('image'),
            product.get('price', {}).get('currentPrice'),
            product.get('price', {}).get('rawPrice'),
            product.get('reviewsCount'),
            product.get('ratings'),
            product.get('shippingMessage'),
            product.get('isBestSeller'),
            product.get('outOfStock')
        ]
        output_data_formatted.append(temp_list)
    return output_data_formatted

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket = 'walmart-aws-1-bucket'
    key = 'raw_data/to_processed/'  # Directory in S3

    walmart_data = []
    walmart_keys = []
    
    # List objects in the S3 bucket under the given prefix
    response = s3.list_objects_v2(Bucket=bucket, Prefix=key)
    
    # Check if any objects exist
    if 'Contents' not in response:
        return {'statusCode': 404, 'message': 'No JSON files found in the specified S3 path.'}

    for file in response['Contents']:
        file_key = file['Key']
        
        # Process only JSON files
        if file_key.endswith('.json'):
            obj = s3.get_object(Bucket=bucket, Key=file_key)
            content = obj['Body'].read().decode('utf-8')  # Decode S3 object content
            json_object = json.loads(content)  # Parse JSON
            walmart_data.append(json_object)
            walmart_keys.append(file_key)
    
    for data in walmart_data:
        walmart_transformed_data = transform_data(data)
        
        walmart_df = pd.DataFrame(walmart_transformed_data, columns=[
            'title', 'image', 'currentPrice', 'rawPrice', 'reviewsCount', 
            'ratings', 'shippingMessage', 'isBestSeller', 'outOfStock'
        ])

        # Save transformed data back to S3
        walmart_key = f"transformed_data/walmart_data/walmart_transformed_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        walmart_buffer = StringIO()
        walmart_df.to_csv(walmart_buffer, index=False)
        
        s3.put_object(Bucket=bucket, Key=walmart_key, Body=walmart_buffer.getvalue())

   
    s3_resource = boto3.resource('s3')
    for key in walmart_keys:
        copy_source = {
            'Bucket': bucket,
            'Key': key
        }
        s3_resource.meta.client.copy(copy_source, bucket, 'raw_data/processed/' + key.split("/")[-1])    
        s3_resource.Object(bucket, key).delete()
    
    return {
        'statusCode': 200,
        'message': 'Data transformation completed successfully and uploaded to S3.'
    }
