import json
import boto3
import time

dynamodb = boto3.resource('dynamodb')
transTable = dynamodb.Table('Transactions')
userTable = dynamodb.Table('UserProfiles')

def lambda_handler(event, context):
    # Handles request: parses input, creates user, stores in DynamoDB, returns response
    try:
        body = json.loads(event.get('body', '{}'))

        count = int(time.time() * 1000)
        
        user_id = body.get('userId', 0)
        responses = userTable.get_item(
            Key={'UserId': int(user_id)}
        )
        if 'Item' not in responses:
            print(f"Error: erm.......")
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'User does not exist'})
            }
        type = body.get('type')
        amount_transfered = body.get('amountTransfered', 0)
        
        transTable.put_item(
            Item={
                'TransactionNumber': int(count) + 1,
                'UserId': int(user_id),
                'Type': type,
                'AmountTransfered': int(amount_transfered)
            }
        )
        return {
            'statusCode': 200,
            'headers': {
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Headers": "Content-Type",
                "Access-Control-Allow-Methods": "OPTIONS,POST"
            },
            'body': json.dumps({'message': "{type} Done!", 'id': user_id})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps({'error': "Internal Server Error"})
        }