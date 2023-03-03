import boto3
import json

# Set the region and credentials for the OpenSearch domain
region = 'us-east-1'  # Replace with your OpenSearch domain region
access_key = ''
secret_key = ''

# Create an OpenSearch client using boto3
opensearch_client = boto3.client('es', region_name=region, aws_access_key_id=access_key, aws_secret_access_key=secret_key)

# Specify the OpenSearch domain endpoint
endpoint = 'https://search-chatbot-3hmncvgjz736jl2knemmga6jfu.us-east-1.es.amazonaws.com'


# Load the JSON data from the file
with open('output.json') as f:
    data = json.load(f)

# Put the JSON data in the OpenSearch domain
for item in data['businesses']:
	doc = {'id': item['id'],'cuisine': 'Chinese'}
	opensearch_client.put_document(
        DomainName='chatbot',
        Document={
            'id': item['id'],
            'cuisine': 'Chinese'
        }
    )
