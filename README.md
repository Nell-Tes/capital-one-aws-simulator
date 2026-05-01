# capital-one-aws-simulator
A micro-level simulation of Capital One's cloud architecture using AWS Lambda, S3, DynamoDB, Aurora, SNS, and SQS.

## Event-driven transaction flow

Transaction requests now use asynchronous messaging:

1. `create_transaction.py` validates input and publishes the transaction request to an SNS topic.
2. SNS fan-outs the request to an SQS queue subscription.
3. `process_transaction_queue.py` consumes queue messages, writes to `Transactions`, and updates `UserProfiles` balance.

### Required Lambda environment variables

- `TRANSACTION_TOPIC_ARN` on the API-facing transaction Lambda (`create_transaction.py`)
  - Expected format: `arn:aws:sns:us-east-1:<account-id>:<topic-name>`
  - If you accidentally paste a subscription ARN, the Lambda now normalizes it to the topic ARN.
