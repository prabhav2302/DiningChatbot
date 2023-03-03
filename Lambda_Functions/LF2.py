import boto3
import json
import requests
import random

def lambda_handler(event, context):
    sqs = boto3.client('sqs')
    queue_url = 'https://sqs.us-east-1.amazonaws.com/231662283369/reccomendation-queue'
    response = sqs.receive_message(
        QueueUrl=queue_url,
        MaxNumberOfMessages=1
    )
    
    if 'Messages' not in response:
        print('Queue is empty')
        return
    
    sqs_message = response['Messages'][0]['Body']
    user_info = sqs_message.split(",")
    user_location = user_info[0]
    user_cuisine = user_info[1].capitalize()
    user_party_size = user_info[2]
    user_date = user_info[3]
    user_time = user_info[4]
    user_email = user_info[5]

    receipt_handle = response['Messages'][0]['ReceiptHandle']
    sqs.delete_message(
        QueueUrl=queue_url,
        ReceiptHandle=receipt_handle
    )
    
    

    
    
    es_query = "https://search-chatbot-3hmncvgjz736jl2knemmga6jfu.us-east-1.es.amazonaws.com/_search?q={cuisine}".format(cuisine=user_cuisine)
    esResponse = requests.get(es_query,auth=('pa1363', 'Pr@bhav123'))
    hits = json.loads(esResponse.text)['hits']['hits']
    options = []
    for i in hits:
        options.append(i['_source']['RestaurantID'])
    
    

    
    dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('restaurant-info')
    
    reccomendation_string = ""
    visited_indexes = set()
    counter = 0
    while(counter<3):
        restaurant_id = options[random.randint(0,len(options)-1)]
        print(restaurant_id)
        if(restaurant_id in visited_indexes):
            continue
        visited_indexes.add(restaurant_id)
        response = table.get_item(
            Key={
            'id': restaurant_id
            }
        )
        reccomendation_string = reccomendation_string + str(counter+1) + "." + response['Item']['name'] + " located at " + response['Item']['location']['address1'] + " , "
        counter+=1
    
    print(reccomendation_string)
    
    
    recipient = "waves.outreach@gmail.com"
    ses = boto3.client('ses')
    email_send = "Hello! Here are my "+user_cuisine+" restaurant suggestions for " + user_party_size + " people for today at " + user_time + ". " + reccomendation_string
    
    
    # Create the message
    message = {
        "Subject": {
            "Data": "Restaurant Reccomendation"
        },
        "Body": {
            "Text": {
                "Data": email_send
            }
        }
    }

    # Send the email
    response = ses.send_email(
        Source="officialprabhav@gmail.com",
        Destination={
            "ToAddresses": [recipient]
        },
        Message=message
    )

    
    
