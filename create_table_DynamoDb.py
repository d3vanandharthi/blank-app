# This script created a DynamoDB table using boto3 library.
import boto3
from botocore.exceptions import ClientError
 
REGION= 'us-east-1'
TABLE_NAME = 'UserTable'
 
dynamodb = boto3.client('dynamodb', region_name=REGION)
 
try:
    response = dynamodb.create_table(
        TableName=TABLE_NAME,
        AttributeDefinitions=[
            {
            'AttributeName': 'id',
            'AttributeType': 'S'  # String type for the primary key
            }
        ],
         KeySchema=[
            {
                'AttributeName': 'id',
                'KeyType': 'HASH'  # Partition key
            }
        ],
         BillingMode='PAY_PER_REQUEST'  # On-demand billing mode
    )
    print("Table creation initiated...")
 
    #Wait until table exists
    waiter = dynamodb.get_waiter('table_exists')
    waiter.wait(TableName=TABLE_NAME)
    print("Table created successfully:", response['TableDescription']['TableName'])
 
except dynamodb.exceptions.ResourceInUseException:
    print("Table already exists. Please choose a different name or delete the existing table.")
 
except ClientError as e:
    print("Error creating table:", e.response['Error']['Message'])