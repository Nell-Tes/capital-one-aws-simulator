## Database: DynamoDB
* **Table Name:** UserProfiles
* **Primary Key:** UserID (String)
* **Attributes:** FullName, DOB, Balance (Defined at runtime by Lambda)

## Database: AuroraDB
* **Table Name:** Transactions
* **Primary Key:** UserID (String)
* **Attributes:** TypeTransaction (String), AmountTransfered (Float)

## Messaging: SNS
* **Topic Name:** TransactionRequests
* **Purpose:** Accept transaction events from API Lambda and fan out to worker subscribers.

## Messaging: SQS
* **Queue Name:** TransactionRequestsQueue
* **Purpose:** Buffer transaction requests for reliable asynchronous processing.
* **Subscription:** Subscribed to SNS `TransactionRequests` topic.