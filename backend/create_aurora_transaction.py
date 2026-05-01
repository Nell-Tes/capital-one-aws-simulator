import json
import psycopg2
import boto3
import time
from decimal import Decimal

dynamodb = boto3.resource('dynamodb')
userTable = dynamodb.Table('UserProfiles')

auth_token = "database-transaction-instance-1.cc7ou4is8y7n.us-east-1.rds.amazonaws.com:5432/?Action=connect&DBUser=postgres&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=ASIA6JYRHTYNHIMJO2GA%2F20260430%2Fus-east-1%2Frds-db%2Faws4_request&X-Amz-Date=20260430T203153Z&X-Amz-Expires=900&X-Amz-Security-Token=IQoJb3JpZ2luX2VjEE0aCXVzLWVhc3QtMSJGMEQCIHHlNv60wn%2FwE0Q3%2FC7Fh35pNkrFjhs6hFEQWUmu3tdfAiBeBjlSPQwdGor3%2F3IhcdVV%2BQ277YZmLbMxalagI7BN2yrvAggWEAAaDDk4MzA0Njc5MDY4MiIMznzEjBk315o3AsocKswCKUQD9aagrB5UG7G%2BzCyxlxADIFfOAXdFKrfrJP6piqpzLM4pcJOcVzRKmab0VBqTfa7t0n9poF6lUhW5ZqnP7i72HfoDe72xooxI92Zi6hIlcAS%2BsHyBDsy3mtmFWIRL%2Bx99cndCFFeb00IzJukol5T2GNdp%2FNeW1yVx%2F9YYDgCFj9BblRqiER97wTUVyMfabOAQHQhJcpq4tfPsG7TqJCtJev3AGBnDGmulgy11SWCXpguEF18MBwiPqWlFDuMZk2achRx4MpZRO93JkJbQK9pXB0Au3Bire5DLyjSz77wCnPC%2FLvb3VNC7BTCgOcqsM%2BIy5Rl0M3I3k4MqUBgNZs3WCkgKLnNYCB8gxqGOJXa1AoAm6nZ%2FmHCntfV24LVpH0IqhZidYyJ%2BpCAqoMYO5a2KVIoPBks%2FeWx2AVR%2Bm2Wn14FyNVN7MmJGc%2BEwlt7OzwY6rgIIEwZZSHiC5p7ApERQ%2BH3wskwQnfJntPfQJLC1mHzSJh5PyrE%2FxxbNmwMfsb3a0u6Db4OLRkjQEjeLzFo0R1vIEeOg52zITpp3g3O4see%2B5wYoJoSWagTnZoh2mXpwyBi0oUqajzutHZQTTibtUqEJyGQibypY8B%2Bcdrr23RGgS%2BHHlvUuXiZj0OkG5hHVu1xTZAPD1IwZuRefTPdrVeFRZfe8QJ%2FH2g3pdQQsy7%2FrZfbGbQL61f9TJyA8l%2FsSwAROfNeLm1WLPW%2FMN6LGWcSV%2BAUaq4PBx5XJqcGjEdSJDd2DLdwU7pnwpOV%2BJng4A3qln%2B1y6LLEjSZYDJmlffL%2F%2B3i0OIz4dD1UfzVdSiD%2FQTY%2BeT4j38Y4HHiCl3HpZoKVfPnkfKyu%2F8NXLTrAHA%3D%3D&X-Amz-Signature=a29f95b0d94f96c54008f5af2a471769dd4e04b102f928ce955daccb1a904a5a&X-Amz-SignedHeaders=host"

conn = None
def tryConnection():
    try:
        conn = psycopg2.connect(
            host='database-transaction-instance-1.cc7ou4is8y7n.us-east-1.rds.amazonaws.com',
            port=5432,
            database='postgres',
            user='postgres',
            password=auth_token,
            sslmode='require'
        )
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute('SELECT version();')
        print(cur.fetchone()[0])
        cur.close()
    except Exception as e:
        print(f"Database error: {e}")
        raise

def closeConnection():
    if conn:
        conn.close()

def addTransaction(transactionNumber, userID, type, amount):
    if conn:
        cur = conn.cursor()
        sql = "INSERT INTO transactions (transactionnumber, userid, type, amount) VALUES (%s, %s, %s)"
        cur.execute(sql, (userID, type, amount))

def lambda_handler(event, context):
    cors_headers = {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Headers": "Content-Type",
        "Access-Control-Allow-Methods": "OPTIONS,POST"
    }
    try:
        tryConnection()
        body = json.loads(event.get('body', '{}'))
        
        user_id = int(body.get('userId'))
        amount_transfered = Decimal(str(body.get('amountTransfered', 0)))
        type = body.get('type')

        # 1. Check if user exists and get current balance
        response = userTable.get_item( Key={'UserId': user_id} )
        if 'Item' not in response:
            print(f"Error: erm.......")
            return {
                'statusCode': 404,
                'headers': cors_headers,
                'body': json.dumps({'error': 'User does not exist'})
            }
        
        current_balance = response['Item'].get('Balance', 0)

        # 2. Logic for Withdrawal (check funds)
        if type == "Withdrawal" and current_balance < amount_transfered:
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps({'error': 'Insufficient balance'})
            }
        
        # 3. Log the Transaction history
        addTransaction(int(time.time() * 1000), user_id, type, amount_transfered)

        # 4. Update the Balance in UserProfiles
        operator = "+" if type == "Deposit" else "-"
        
        userTable.update_item(
            Key={'UserId': user_id},
            UpdateExpression=f"SET Balance = Balance {operator} :amt",
            ExpressionAttributeValues={':amt': amount_transfered}
        )

        closeConnection()


        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': "{type} Done!", 'id': user_id})
        }


    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps({'error': str(e)})
        }

