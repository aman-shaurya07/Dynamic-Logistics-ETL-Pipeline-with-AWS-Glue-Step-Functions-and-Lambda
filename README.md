# Dynamic Logistics ETL Pipeline with AWS Glue, Step Functions, and Lambda

## Overview
This project processes logistics data automatically:
1. Files uploaded to the `logistics-raw` S3 bucket trigger the Step Functions workflow.
2. Glue crawlers validate and infer the schema of new files.
3. Glue jobs process the data, transform it, and store the output.
4. Processed files are archived using a Lambda function.

## Architecture
- **S3**: Stores raw files and triggers the workflow.
- **Lambda (Trigger Step Functions)**: Starts Step Functions when a file is uploaded.
- **Step Functions**: Orchestrates the Glue Crawler, Glue Job, and Lambda Archiver.
- **Glue**: Performs the ETL (Extract, Transform, Load) processing.


## Prerequisites
1. **AWS Services**:
   - S3, Lambda, Glue, Step Functions.
2. **IAM Roles**:
   - Refer to `iam/required_roles.txt`.



## Steps to Deploy

***Step 1. Create S3 buckets:***
```bash
aws s3 mb s3://logistics-raw
aws s3 mb s3://logistics-archive
aws s3 mb s3://logistics-helper
```

***Step 2. Copy lambda functions zip files(lambda_trigger_step_functions.zip, lambda_archive_files.zip) to logistics-helper bucket:***
```bash
aws s3 cp lambda_trigger_step_functions.zip s3://logistics-helper/
aws s3 cp lambda_archive_files.zip s3://logistics-helper/
```


***Step 3: Deploy Lambda Functions***

1. Trigger Step Functions:
```bash
aws lambda create-function \
    --function-name step-functions-trigger \
    --runtime python3.9 \
    --role <LAMBDA_EXECUTION_ROLE_ARN> \
    --handler lambda_trigger_step_functions.lambda_handler \
    --code S3Bucket=logistics-helper,S3Key=lambda_trigger_step_functions.zip \
    --timeout 30
```

2. Archive Files:
```bash
aws lambda create-function \
    --function-name logistics-archive-files \
    --runtime python3.9 \
    --role <LAMBDA_EXECUTION_ROLE_ARN> \
    --handler lambda_archive_files.lambda_handler \
    --code S3Bucket=logistics-helper,S3Key=lambda_archive_files.zip \
    --timeout 30
```

***Step 4: Configure S3 Event Notifications***
```bash
aws s3api put-bucket-notification-configuration \
    --bucket logistics-raw \
    --notification-configuration file://s3/s3_event_notification_config.json
```


***Step 5: Set Up Glue:***

****Create a Glue Crawler:****

In glue_crawler_config.json file, replace the <GLUE_SERVICE_ROLE> with the ARN of the IAM role with Glue permissions.
```bash 
aws glue create-crawler --cli-input-json file://glue/glue_crawler_config.json
```

Create a Glue Job:
```bash
aws glue create-job --name logistics-etl-job --role <GLUE_SERVICE_ROLE> --command '{"Name": "glueetl", "ScriptLocation": "s3://path-to-glue-job-script.py"}'
```

***Step 6: Set Up Step Functions:***
```bash
bash step_functions/create_state_machine.sh
```

***Step 6: Testing: Upload a file to logistics-raw/input_data/ and monitor the pipeline.***

