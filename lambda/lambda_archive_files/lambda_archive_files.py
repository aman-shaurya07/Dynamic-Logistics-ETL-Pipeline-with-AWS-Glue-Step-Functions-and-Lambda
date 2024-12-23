import boto3
import json

def lambda_handler(event, context):
    s3_client = boto3.client('s3')
    for record in event['Records']:
        source_bucket = record['s3']['bucket']['name']
        source_key = record['s3']['object']['key']
        destination_bucket = 'logistics-archive'

        # Move file to archive bucket
        copy_source = {'Bucket': source_bucket, 'Key': source_key}
        destination_key = f"archived_data/{source_key.split('/')[-1]}"

        s3_client.copy_object(CopySource=copy_source, Bucket=destination_bucket, Key=destination_key)
        s3_client.delete_object(Bucket=source_bucket, Key=source_key)

        print(f"Moved {source_key} to {destination_bucket}/{destination_key}")
