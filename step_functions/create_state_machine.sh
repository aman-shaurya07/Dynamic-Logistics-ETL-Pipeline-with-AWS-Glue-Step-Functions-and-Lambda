#!/bin/bash

# Define the state machine name
STATE_MACHINE_NAME="logistics-etl-pipeline"

# Define the role ARN for Step Functions (replace with your role ARN)
EXECUTION_ROLE_ARN="<STEP_FUNCTIONS_EXECUTION_ROLE_ARN>"

# Define the state machine definition file
STATE_MACHINE_DEFINITION="step_functions_definition.json"

# Validate required parameters
if [[ -z "$EXECUTION_ROLE_ARN" ]]; then
    echo "Error: EXECUTION_ROLE_ARN is not set. Please update the script with the correct role ARN."
    exit 1
fi

# Create the state machine
aws stepfunctions create-state-machine \
    --name $STATE_MACHINE_NAME \
    --definition file://$STATE_MACHINE_DEFINITION \
    --role-arn $EXECUTION_ROLE_ARN

# Output success message
if [[ $? -eq 0 ]]; then
    echo "Step Functions state machine '$STATE_MACHINE_NAME' created successfully."
else
    echo "Error: Failed to create Step Functions state machine."
fi
