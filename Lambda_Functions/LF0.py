import json
import boto3
import random
from time import gmtime, strftime

def lambda_handler(event, context):
    # TODO implement
    client = boto3.client('lexv2-runtime')
    user_text = event['messages'][0]['unstructured']['text']
    lex_response = client.recognize_text(
        botId='CP8TUQXHLD',
        botAliasId='8MOWPVDSMZ',
        localeId = "en_US",
        sessionId = '32131',
        text=user_text
    )
    
    lex_text = lex_response['messages'][0]['content']
    lex_id = str(random.randint(1,1000000))
    response = {
        "messages": [
            {
            "type": "unstructured",
            "unstructured": {
                "id": '311314',
                "text": lex_text,
                "timestamp": strftime("%Y-%m-%d %H:%M:%S", gmtime())
            }
            }
        ]
        }                                
     
    
    
    return response
    
