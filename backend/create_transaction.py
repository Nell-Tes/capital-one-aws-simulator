import json
import boto3
import time
import os

dynamodb = boto3.resource('dynamodb')
transTable = dynamodb.Table('Transactions')
userTable = dynamodb.Table('UserProfiles')
sns = boto3.client('sns')

DEFAULT_TRANSACTION_TOPIC_ARN = "arn:aws:sns:us-east-1:983046790682:TransactionRequests:ff28ce36-89b3-4f21-94e9-8bb7064a3806"
TRANSACTION_TOPIC_ARN = os.environ.get('TRANSACTION_TOPIC_ARN', DEFAULT_TRANSACTION_TOPIC_ARN)


def normalize_sns_topic_arn(arn_value):
    if not arn_value:
        return arn_value
    parts = arn_value.split(":")
    # Topic ARN: arn:aws:sns:<region>:<account>:<topic-name>
    # Subscription ARN adds one more segment with the subscription id.
    if len(parts) == 7 and parts[2] == "sns":
        return ":".join(parts[:6])
    return arn_value

def lambda_handler(event, context):
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': 'CORS preflight OK'})
        }

    try:
        body = json.loads(event.get('body', '{}'))

        count = int(time.time() * 1000)

        user_id = int(body.get('userId', 0))
        response = userTable.get_item(
            Key={'UserId': user_id}
        )
        if 'Item' not in response:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({'error': 'User does not exist'})
            }

        transaction_type = body.get('type')
        amount_transfered = int(body.get('amountTransfered', 0))
        if transaction_type not in {"Deposit", "Withdrawal"}:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({'error': 'type must be Deposit or Withdrawal'})
            }
        if amount_transfered <= 0:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({'error': 'amountTransfered must be greater than 0'})
            }
        topic_arn = normalize_sns_topic_arn(TRANSACTION_TOPIC_ARN)
        if not topic_arn:
            return {
                'statusCode': 500,
                'headers': cors_headers,
                'body': json.dumps({'error': 'TRANSACTION_TOPIC_ARN is not configured'})
            }

        transaction_number = count + 1
        payload = {
            'transactionNumber': transaction_number,
            'userId': user_id,
            'type': transaction_type,
            'amountTransfered': amount_transfered
        }
        sns_response = sns.publish(
            TopicArn=topic_arn,
            Subject='BankTransactionRequested',
            Message=json.dumps(payload)
        )

        return {
            'statusCode': 202,
            'headers': cors_headers,
            'body': json.dumps({
                'message': f'{transaction_type} queued for processing',
                'id': user_id,
                'transactionNumber': transaction_number,
                'snsMessageId': sns_response.get('MessageId')
            })
        }

    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': "Internal Server Error"})
        }