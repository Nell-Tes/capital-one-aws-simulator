import psycopg2
import boto3

auth_token = boto3.client('rds', region_name='us-east-1').generate_db_auth_token(DBHostname='database-transaction.cluster-cc7ou4is8y7n.us-east-1.rds.amazonaws.com', Port=5432, DBUsername='postgres', Region='us-east-1')

conn = None
def tryConnection():
    try:
        conn = psycopg2.connect(
            host='database-transaction.cluster-cc7ou4is8y7n.us-east-1.rds.amazonaws.com',
            port=5432,
            database='postgres',
            user='postgres',
            password=auth_token,
            sslmode='require'
        )
        cur = conn.cursor()
        cur.execute('SELECT version();')
        print(cur.fetchone()[0])
    except Exception as e:
        print(f"Database error: {e}")
        raise

def closeConnection():
    if conn:
        conn.close()


def addTransaction(userID, type, amount):
    if conn:
        cur = conn.cursor()
        sql = "INSERT INTO transactions (userid, type, amount) VALUES (%s, %s, %s)"
        cur.execute(sql, (userID, type, amount))