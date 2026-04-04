import json
import boto3
import uuid

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('UserProfiles')

def lambda_handler(event, context):
    # Handles request: parses input, creates user, stores in DynamoDB, returns response
    try:
        body = json.loads(event.get('body', '{}'))
        
        full_name = body.get('fullName')
        dob = body.get('dob')
        balance = body.get('balance', 0)
        
        user_id = int(uuid.uuid4().int % 1_000_000_000)  # 9 digit-ish int
        
        table.put_item(
            Item={
                'UserId': user_id,
                'FullName': full_name,
                'DOB': dob,
                'Balance': int(balance)
            }
        )
        
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            'body': json.dumps({'message': 'Account Created!', 'id': user_id})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': "Internal Server Error"})
        }