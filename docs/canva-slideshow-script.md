# Capital One AWS Simulator - Canva Slideshow Script

Use this as a direct copy/paste script for Canva slides.

---

## Slide 1 - Title
**Title:** Capital One AWS Micro-Simulator  
**Subtitle:** Event-Driven Banking Workflow with Lambda, SNS, SQS, DynamoDB, Aurora, and EventBridge  
**Presenter:** <Your Name> | CMSC398P

**Visuals to add in Canva**
- Capital One branding colors (navy `#004879`, red `#DB1F26`)
- Existing architecture screenshot as "Before"
- Project screenshot from `frontend/index.html` page

---

## Slide 2 - Project Goal
**Title:** What This Simulator Demonstrates

**Bullets**
- Serverless banking workflow using AWS managed services
- User profile creation and balance lookup
- Transaction processing with asynchronous messaging
- Hybrid data model: DynamoDB + Aurora PostgreSQL
- Event-driven extensions through EventBridge

---

## Slide 3 - Architecture: Before vs After
**Title:** Architecture Evolution

**Before (left side)**
- IAM -> S3 -> Lambda -> DynamoDB/Aurora

**After (right side)**
- IAM -> S3 -> API Gateway -> Lambda (transaction API)
- Lambda publishes transaction events to SNS
- SNS fan-out into SQS queue
- SQS triggers Lambda queue processor
- Queue processor updates DynamoDB and logs transactions
- EventBridge rule invokes Lambda for event orchestration/automation

**Canva layout tip**
- Use two columns with arrows and AWS icons
- Label "Synchronous path" vs "Asynchronous path"

---

## Slide 4 - User-Facing Site
**Title:** Frontend Experience

**Bullets**
- Main portal (`index.html`) supports:
  - Create account
  - Check balance
- Transaction screen (`transactions.html`) supports:
  - Deposit
  - Withdrawal
- Updated UX now states requests are queued asynchronously

**Screenshot checklist**
- Account creation form
- Balance lookup result card
- Transactions page showing "Queued successfully"

---

## Slide 5 - New Feature: SNS + SQS Pipeline
**Title:** Why SNS + SQS Were Added

**Bullets**
- Decouples API request from transaction processing
- Improves reliability and burst handling
- Supports retries and DLQ patterns
- Creates cleaner separation of responsibilities
- Enables future fan-out consumers without changing API Lambda

---

## Slide 6 - Code Snippet: Publish to SNS (Direct AWS Interaction)
**Title:** Lambda Transaction API -> SNS Publish

Use this snippet from `backend/create_transaction.py`:

```python
sns = boto3.client('sns')
TRANSACTION_TOPIC_ARN = os.environ.get('TRANSACTION_TOPIC_ARN')

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
```

**Speaker note**
- This is where the app hands work off to AWS messaging.

---

## Slide 7 - Code Snippet: SQS-triggered Lambda Consumer
**Title:** SQS -> Lambda Queue Processor

Use this snippet from `backend/process_transaction_queue.py`:

```python
def _parse_sns_wrapped_message(record):
    body = json.loads(record['body'])
    message = body.get('Message')
    return json.loads(message) if message else body

for record in event.get('Records', []):
    payload = _parse_sns_wrapped_message(record)
    user_id = int(payload['userId'])
    amount = int(payload['amountTransfered'])
```

**Speaker note**
- SQS receives SNS notifications and triggers Lambda automatically.

---

## Slide 8 - Code Snippet: DynamoDB + Aurora Access
**Title:** Data Layer Integration

Use these snippets from backend:

```python
# DynamoDB tables
dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table('UserProfiles')
trans_table = dynamodb.Table('Transactions')
```

```python
# Aurora connection (create_aurora_transaction.py)
conn = psycopg2.connect(
    host='database-transaction-instance-1.cc7ou4is8y7n.us-east-1.rds.amazonaws.com',
    port=5432,
    database='postgres',
    user='postgres',
    password=auth_token,
    sslmode='require'
)
```

**Speaker note**
- DynamoDB stores low-latency profile/balance state; Aurora stores relational transaction records.

---

## Slide 9 - EventBridge Addition
**Title:** EventBridge for Scheduled or Rule-based Events

**Bullets**
- EventBridge rule captures system/business events
- Rule triggers dedicated Lambda handler
- Handler can publish to SNS or execute other workflows
- Enables automation beyond direct user requests

**Console screenshot checklist**
- EventBridge rule page
- Rule target Lambda configuration
- Recent matched events / invocation history

**Note**
- Add your EventBridge Lambda code snippet here if available in repo or console.

---

## Slide 10 - AWS Console Evidence
**Title:** Console Walkthrough (Proof of Implementation)

Add one screenshot each:
- SNS topic (`TransactionRequests`) and subscriptions
- SQS queue and Lambda trigger mapping
- Lambda env vars (`TRANSACTION_TOPIC_ARN`)
- CloudWatch logs (publish + consumer invocation)
- DynamoDB table items (`UserProfiles`, `Transactions`)
- Aurora table rows (`transactions`)
- EventBridge rule + targets

---

## Slide 11 - End-to-End Flow Demo
**Title:** Transaction Lifecycle Demo

**Step flow for narration**
1. User submits deposit/withdrawal on transactions page
2. API Lambda validates and publishes to SNS
3. SNS forwards to SQS subscription
4. SQS triggers queue processor Lambda
5. Lambda updates DynamoDB balance + transaction history store
6. Logs/metrics observable in CloudWatch

---

## Slide 12 - Key Outcomes & Next Steps
**Title:** Outcomes and Future Work

**Outcomes**
- Implemented event-driven transaction processing
- Improved reliability and scalability with SNS/SQS
- Maintained user-facing banking simulation UI
- Integrated multiple AWS data and messaging services

**Next steps**
- Add DLQ and alarms
- Add idempotency key handling
- Add EventBridge-driven scheduled reconciliation
- Add CI/CD deployment pipeline

---

## Canva Build Instructions (Fast)
1. Open Canva -> Presentation (16:9).
2. Use a dark blue + white theme with red accents.
3. Create 12 slides using this script.
4. Use AWS architecture icons for service blocks.
5. Paste code snippets in monospace boxes with dark background.
6. Export as PDF + PPTX.

---

## Architecture Diagram Blueprint (Exact Canva Layout)

Use this for the "Architecture: Before vs After" slide, or duplicate into a standalone architecture slide.

### Canvas setup
- Slide size: `1920 x 1080` (Canva 16:9)
- Background: light gray `#F2F3F5`
- Font:
  - Titles: `Poppins Semibold`
  - Labels: `Poppins Medium`
  - Sub-labels: `Poppins Regular`

### Color palette
- Capital One navy: `#004879`
- Capital One red: `#DB1F26`
- Arrow black: `#1E1E1E`
- Caption gray: `#3C3C3C`

### Grid and spacing
- Top margin: `70 px`
- Left/right margin: `90 px`
- Service icon tile size: `120 x 120`
- Horizontal node gap: `85 px`
- Vertical lane gap: `190 px`

### Element placement (x, y, w, h)
Coordinates below are top-left anchored on a `1920x1080` slide.

1) Capital One logo/title
- Position: `(780, 40, 360, 90)`
- Text: `Capital One AWS Simulator`
- Subtitle under title: `Event-Driven Banking Architecture`

2) IAM tile (start)
- Tile: `(120, 460, 120, 120)`
- Label box: `(95, 595, 170, 95)`
- Label text:
  - `Identity`
  - `Access`
  - `Management`

3) S3 static web tile
- Tile: `(325, 460, 120, 120)`
- Label box: `(305, 595, 165, 65)`
- Label text:
  - `S3`
  - `Web Interface`

4) API Gateway tile
- Tile: `(530, 460, 120, 120)`
- Label box: `(500, 595, 190, 65)`
- Label text:
  - `API Gateway`

5) Lambda Transaction API tile
- Tile: `(740, 380, 120, 120)`
- Label box: `(700, 505, 210, 95)`
- Label text:
  - `Lambda`
  - `Transaction API`

6) SNS topic tile
- Tile: `(950, 380, 120, 120)`
- Label box: `(920, 505, 190, 70)`
- Label text:
  - `SNS Topic`
  - `TransactionRequests`

7) SQS queue tile
- Tile: `(1160, 380, 120, 120)`
- Label box: `(1135, 505, 180, 70)`
- Label text:
  - `SQS Queue`

8) Lambda Queue Processor tile
- Tile: `(1370, 380, 120, 120)`
- Label box: `(1325, 505, 230, 95)`
- Label text:
  - `Lambda`
  - `Queue Processor`

9) DynamoDB tile (lower right)
- Tile: `(1570, 560, 120, 120)`
- Label box: `(1490, 690, 290, 85)`
- Label text:
  - `DynamoDB`
  - `UserProfiles + Balances`

10) Aurora tile (upper right)
- Tile: `(1570, 250, 120, 120)`
- Label box: `(1488, 375, 290, 95)`
- Label text:
  - `Aurora PostgreSQL`
  - `Transaction History`

11) Lambda Profile API branch
- Tile: `(740, 620, 120, 120)`
- Label box: `(695, 745, 230, 95)`
- Label text:
  - `Lambda`
  - `Profile API`

12) EventBridge tile (lower middle)
- Tile: `(950, 700, 120, 120)`
- Label box: `(920, 825, 210, 70)`
- Label text:
  - `EventBridge`
  - `Rule`

13) Lambda Event Handler tile
- Tile: `(1160, 700, 120, 120)`
- Label box: `(1120, 825, 220, 70)`
- Label text:
  - `Lambda Event`
  - `Handler`

### Arrow map (start -> end)
Use straight black arrows, thickness `3 px`, arrowhead size medium.

Main request path:
- IAM -> S3
- S3 -> API Gateway
- API Gateway -> Lambda Transaction API
- Lambda Transaction API -> SNS Topic
- SNS Topic -> SQS Queue
- SQS Queue -> Lambda Queue Processor

Data write path:
- Lambda Queue Processor -> Aurora
- Lambda Queue Processor -> DynamoDB

Profile branch:
- API Gateway -> Lambda Profile API
- Lambda Profile API -> DynamoDB

Event branch:
- EventBridge Rule -> Lambda Event Handler
- Lambda Event Handler -> SNS Topic

### Label style
- Service labels: `26-30 px` depending on length
- Subtext: `22-24 px`
- Text color: `#2E2E2E`
- Align center under each icon

### Visual polish
- Add soft shadow to each icon tile:
  - Blur: `8`
  - Offset Y: `3`
  - Opacity: `20%`
- Keep all labels baseline-aligned per lane for cleaner look.
- Ensure no arrow crosses text blocks; route arrows around label boxes.

### AWS icon search terms in Canva
- `AWS IAM`
- `AWS S3`
- `AWS API Gateway`
- `AWS Lambda`
- `AWS SNS`
- `AWS SQS`
- `AWS DynamoDB`
- `AWS Aurora`
- `AWS EventBridge`

---

## Deep-Dive Slide Blueprint (Async Transaction Flow Only)

Use this as a dedicated technical slide after the full architecture.

### Purpose
Show exactly how one transaction request moves through SNS/SQS and updates storage.

### Canvas setup
- Slide size: `1920 x 1080`
- Background: white `#FFFFFF`
- Header bar: navy rectangle `#004879`, size `(0, 0, 1920, 120)`
- Header text: `Async Transaction Pipeline (Deposit/Withdrawal)`

### Node layout (x, y, w, h)
All service tiles are `130 x 130`.

1) API Gateway
- Tile: `(120, 420, 130, 130)`
- Label: `(85, 565, 200, 60)` -> `API Gateway`

2) Lambda Transaction API
- Tile: `(360, 420, 130, 130)`
- Label: `(300, 565, 250, 85)` -> `Lambda` / `create_transaction`

3) SNS Topic
- Tile: `(620, 420, 130, 130)`
- Label: `(575, 565, 220, 85)` -> `SNS Topic` / `TransactionRequests`

4) SQS Queue
- Tile: `(880, 420, 130, 130)`
- Label: `(845, 565, 200, 60)` -> `SQS Queue`

5) Lambda Queue Processor
- Tile: `(1140, 420, 130, 130)`
- Label: `(1065, 565, 280, 85)` -> `Lambda` / `process_transaction_queue`

6) DynamoDB
- Tile: `(1420, 320, 130, 130)`
- Label: `(1360, 465, 250, 85)` -> `DynamoDB` / `UserProfiles`

7) Aurora PostgreSQL
- Tile: `(1420, 560, 130, 130)`
- Label: `(1335, 705, 320, 90)` -> `Aurora PostgreSQL` / `Transactions history`

### Arrow map
Use `3 px` black arrows with medium arrowheads.

- API Gateway -> Lambda Transaction API
- Lambda Transaction API -> SNS Topic
- SNS Topic -> SQS Queue
- SQS Queue -> Lambda Queue Processor
- Lambda Queue Processor -> DynamoDB
- Lambda Queue Processor -> Aurora PostgreSQL

### Numbered flow badges (add circles)
Place small red circles (`#DB1F26`) with white numbers near each arrow:
- `1` User submits transaction
- `2` Lambda validates + builds payload
- `3` Publish to SNS
- `4` SNS fan-out to SQS
- `5` SQS triggers consumer Lambda
- `6` Update balance + transaction log

### Side callout boxes (right side)
Add two rounded callout boxes:

1) Reliability callout `(1580, 250, 300, 170)`
- Title: `Why SQS?`
- Bullets:
  - Buffers traffic spikes
  - Enables retries
  - Supports DLQ patterns

2) Data consistency callout `(1580, 460, 300, 190)`
- Title: `Storage outcomes`
- Bullets:
  - DynamoDB: current profile/balance
  - Aurora: transaction audit history
  - Both updated by queue processor

### Code snippet strip (bottom)
At bottom, add a dark strip `(70, 850, 1780, 180)` with two mini snippets:

Left snippet title: `SNS publish`
```python
sns.publish(TopicArn=topic_arn, Message=json.dumps(payload))
```

Right snippet title: `SQS consumer`
```python
for record in event["Records"]:
    payload = _parse_sns_wrapped_message(record)
```

### Animation order (if using Canva Present mode)
1. API -> Lambda
2. Lambda -> SNS
3. SNS -> SQS
4. SQS -> Queue Lambda
5. Queue Lambda -> DynamoDB + Aurora
6. Show side callout boxes
