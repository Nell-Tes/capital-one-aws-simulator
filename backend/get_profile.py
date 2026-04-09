import json
import boto3
from botocore.exceptions import ClientError
from decimal import Decimal

# Helper to handle DynamoDB numbers (Decimals) in JSON
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return super(DecimalEncoder, self).default(obj)

dynamodb = boto3.resource('dynamodb')

def lambda_handler(event, context):
    table = dynamodb.Table('Users') 
    
    query_params = event.get('queryStringParameters')
    user_id_str = query_params.get('id') if query_params else None

    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'OPTIONS,GET'
    }

    if not user_id_str:
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps({'error': 'Missing user id parameter'})
        }

    try:
        # THE FIX: Convert the string from the URL to an Integer
        user_id_int = int(user_id_str)
        
        response = table.get_item(Key={'id': user_id_int})
        item = response.get('Item')

        if not item:
            return {
                'statusCode': 404,
                'headers': cors_headers,
                'body': json.dumps({'error': 'User not found'})
            }

        return {
            'statusCode': 200,
            'headers': cors_headers,
            # Use DecimalEncoder to handle the balance/number fields
            'body': json.dumps(item, cls=DecimalEncoder)
        }

    except ValueError:
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps({'error': 'ID must be a number'})
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': str(e)})
        }