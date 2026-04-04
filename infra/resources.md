## Database: DynamoDB
* **Table Name:** UserProfiles
* **Primary Key:** UserID (String)
* **Attributes:** FullName, DOB, Balance (Defined at runtime by Lambda)

## Database: AuroraDB
* **Table Name:** Transactions
* **Primary Key:** UserID (String)
* **Attributes:** TypeTransaction (String), AmountTransfered (Float)