import boto3
import json

def lambda_handler(event, context):
    stepfunctions_client = boto3.client('stepfunctions')
    for record in event['Records']:
        # Extract file details from the S3 event
        bucket_name = record['s3']['bucket']['name']
        file_key = record['s3']['object']['key']

        # Trigger Step Functions workflow
        response = stepfunctions_client.start_execution(
            stateMachineArn="<STEP_FUNCTIONS_ARN>",  # Replace with your Step Functions ARN
            input=json.dumps({
                "bucket_name": bucket_name,
                "file_key": file_key
            })
        )

        print(f"Triggered Step Functions: {response['executionArn']}")
    return {
        'statusCode': 200,
        'body': json.dumps('Step Functions started successfully.')
    }


# Note: You can get STEP_FUNCTIONS_ARN from output of Step function state machine creation