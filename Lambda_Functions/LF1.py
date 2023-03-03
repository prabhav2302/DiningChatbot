import json
from datetime import datetime, timedelta
import re
import boto3

def validate(slots):

    valid_areas = ['bronx', 'brooklyn', 'manhattan', 'queens', 'staten island']
    valid_cuisines = ['chinese','mexican','indian','italian','korean']
    today = datetime.now().date()
    
    
    if not slots['location']:
        return {
        'isValid': False,
        'violatedSlot': 'location'
        }        
        
    if slots['location']['value']['originalValue'].lower() not in  valid_areas:
        return {
        'isValid': False,
        'violatedSlot': 'location',
        'message': 'We currently  support only {} as a valid destination.?'.format(", ".join(valid_areas))
        }
        
    if not slots['cuisine']:
        return {
        'isValid': False,
        'violatedSlot': 'cuisine',
    }
    
    if slots['cuisine']['value']['originalValue'].lower() not in  valid_cuisines:
        return {
        'isValid': False,
        'violatedSlot': 'cuisine',
        'message': 'We currently  support only {} as a valid cuisine.?'.format(", ".join(valid_cuisines))
        }
            
        
    if not slots['Party_Number']:
        return {
        'isValid': False,
        'violatedSlot': 'Party_Number'
    }
        
    if not slots['Date']:
        return {
        'isValid': False,
        'violatedSlot': 'Date'
    }
    
    date_str = slots['Date']['value']['interpretedValue'] #need to fix this as well
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    if date < today:
        return {
        'isValid': False,
        'violatedSlot': 'Date',
        'message': 'Your booking date can at earliest be today'
        }
        
    
    if not slots['Time']:

        return {
        'isValid': False,
        'violatedSlot': 'Time'
    }    
   
    
    if not slots['email']:
        return {
        'isValid': False,
        'violatedSlot': 'email'
    }    

    return {'isValid': True}
    
def lambda_handler(event, context):
    slots = event['sessionState']['intent']['slots']
    intent = event['sessionState']['intent']['name']
    validation_result = validate(slots)
    
    
    if event['invocationSource'] == 'DialogCodeHook':
        if not validation_result['isValid']:
            
            if 'message' in validation_result:
            
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                },
                "messages": [
                    {
                        "contentType": "PlainText",
                        "content": validation_result['message']
                    }
                ]
               } 
            else:
                response = {
                "sessionState": {
                    "dialogAction": {
                        'slotToElicit':validation_result['violatedSlot'],
                        "type": "ElicitSlot"
                    },
                    "intent": {
                        'name':intent,
                        'slots': slots
                        
                        }
                }
               } 
    
            
        
        else:
            response = {
            "sessionState": {
                "dialogAction": {
                    "type": "Delegate"
                },
                "intent": {
                    'name':intent,
                    'slots': slots
                    
                    }
        
            }
        }
        
        return response
    
    if event['invocationSource'] == 'FulfillmentCodeHook':
        # Add order in Database
        sqs = boto3.client('sqs')
        print(slots)
        message = slots['location']['value']['resolvedValues'][0] +","+slots['cuisine']['value']['resolvedValues'][0] +","+slots['Party_Number']['value']['resolvedValues'][0] + ",:"+slots['Date']['value']['resolvedValues'][0] + ","+slots['Time']['value']['resolvedValues'][0] + ","+slots['email']['value']['resolvedValues'][0]                                     
        print(message)
        sqs_response = sqs.send_message(
            QueueUrl="https://sqs.us-east-1.amazonaws.com/231662283369/reccomendation-queue",
            MessageBody=message
        )
        response = {
        "sessionState": {
            "dialogAction": {
                "type": "Close"
            },
            "intent": {
                'name':intent,
                'slots': slots,
                'state':'Fulfilled'
                
                }
    
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "You’re all set. Expect my suggestions shortly! Have a great day. "
            }
        ]
    }
        return response
           
        