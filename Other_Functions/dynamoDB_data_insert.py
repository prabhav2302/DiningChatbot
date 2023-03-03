import boto3
import json
from decimal import Decimal
from datetime import datetime

session = boto3.Session(
    aws_access_key_id='',
    aws_secret_access_key=''
)

# Use the session to connect to DynamoDB
dynamodb = session.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('restaurant-info')


# Read the JSON file and convert it into a Python dictionary
with open('korean.json', 'r') as f:
    data = json.load(f,  parse_float=Decimal)


# Loop through each item in the JSON file and insert it into the table
for item in data['businesses']:
	item['cuisine'] = 'Korean'
	item['insertedAtTimestamp'] = str(datetime.now())
	table.put_item(Item=item)


