import json
import boto3

dynamodb = boto3.resource('dynamodb')
trans_table = dynamodb.Table('Transactions')
user_table = dynamodb.Table('UserProfiles')


def _parse_sns_wrapped_message(record):
    body = json.loads(record['body'])
    message = body.get('Message')
    return json.loads(message) if message else body


def lambda_handler(event, context):
    for record in event.get('Records', []):
        payload = _parse_sns_wrapped_message(record)
        user_id = int(payload['userId'])
        amount = int(payload['amountTransfered'])
        transaction_type = payload['type']
        transaction_number = int(payload['transactionNumber'])

        user_response = user_table.get_item(Key={'UserId': user_id})
        if 'Item' not in user_response:
            raise ValueError(f'User {user_id} not found')

        current_balance = int(user_response['Item'].get('Balance', 0))
        if transaction_type == 'Withdrawal' and current_balance < amount:
            raise ValueError(f'Insufficient balance for user {user_id}')

        trans_table.put_item(
            Item={
                'TransactionNumber': transaction_number,
                'UserId': user_id,
                'Type': transaction_type,
                'AmountTransfered': amount
            }
        )

        if transaction_type == 'Withdrawal':
            expression = "SET Balance = Balance - :amt"
        else:
            expression = "SET Balance = Balance + :amt"

        user_table.update_item(
            Key={'UserId': user_id},
            UpdateExpression=expression,
            ExpressionAttributeValues={':amt': amount},
            ReturnValues='UPDATED_NEW'
        )

    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'SQS batch processed'})
    }
