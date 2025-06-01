

```markdown
# 🌐 High Availability and Disaster Recovery with AWS Serverless Architecture

This project demonstrates how to build a **highly available**, **resilient**, and **serverless** application using AWS managed services such as **DynamoDB Global Tables**, **Lambda**, **API Gateway**, **Route 53**, and a frontend website.

---

## 📌 Features

- **Multi-region active-passive setup**
- **Automatic failover using Route 53 Health Checks**
- **Global DynamoDB replication**
- **Fully serverless backend using AWS Lambda**
- **REST APIs exposed via API Gateway**
- **Responsive frontend using HTML, Bootstrap, and JavaScript**

---

## ⚙️ Step-by-Step Setup

### 1. **Create DynamoDB Global Table**
- **Table Name**: `HighAvailabilityTable`
- **Partition Key**: `ItemId` (String)
- Add a replica region (e.g., `us-west-2`) via the **Global Tables** tab.

---

### 2. **Create IAM Role**
- **Role Name**: `LambdaDynamoDBRole`
- Attach Policies:
  - `AmazonDynamoDBFullAccess`
  - `AWSLambdaBasicExecutionRole`

---

### 3. **Deploy Lambda Functions in Both Regions**

1. **Read Function** (`read_function.py`):
```python
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('HighAvailabilityTable')

def lambda_handler(event, context):
    try:
        response = table.scan()
        items = response['Items']
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Enable CORS
            },
            'body': json.dumps(items)  # Return the items array
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',  # Enable CORS
            },
            'body': json.dumps({'error': str(e)})
        }
```

2. **Write Function** (`write_function.py`):
```python
import json
import boto3

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('HighAvailabilityTable')

def lambda_handler(event, context):
    try:
        body = json.loads(event['body'])
        item_id = body['ItemId']
        data = body['Data']

        table.put_item(Item={'ItemId': item_id, 'Data': data})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'Item saved successfully'})
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

* Runtime: Python 3.9
* Use the `LambdaDynamoDBRole`
* Deploy same functions in both primary and secondary regions

---

### 4. **Create REST APIs via API Gateway**

* **Resources**:

  * `/read` → GET → `ReadFunction`
  * `/write` → POST → `WriteFunction`
* Enable **CORS**
* Use **proxy integration**
* Deploy to stage: `prod`
* Repeat in the second region

---

### 5. **Set Up ACM Certificates & Custom Domain**

* Domain: `api.<your-domain>.com`
* Use **DNS validation** via ACM
* Configure **Custom domain names** in API Gateway
* Map APIs to the domain for both regions

---

### 6. **Route 53 DNS & Health Checks**

1. **Create Health Checks** for `/read` endpoints in both regions.
2. **Failover Routing Policy**:

   * Primary: API Gateway (us-east-1)
   * Secondary: API Gateway (us-west-2)

---

### 7. **Frontend Website (HTML + Bootstrap + JS)**

#### `index.html`

* Form to write data
* Dynamic list to read items
* Interacts with `api.<your-domain>.com`

Host via:

* S3 Static Website Hosting
* Or integrate with API Gateway

---

### 8. **Failover Testing**

* Simulate failure by deleting/disabling the primary API
* Route 53 will redirect traffic to the secondary API
* Frontend continues working via the DNS-based failover

---

## 🛡️ Best Practices

* Replace `AmazonDynamoDBFullAccess` with least-privilege policies in production.
* Set lower TTLs for DNS records if faster failover is required.
* Use CloudWatch Alarms with Route 53 Health Checks for better monitoring.

---

## 🚀 Tech Stack

| Service         | Purpose                       |
| --------------- | ----------------------------- |
| **AWS Lambda**  | Serverless compute backend    |
| **DynamoDB**    | Multi-region persistent store |
| **API Gateway** | Expose REST APIs              |
| **Route 53**    | DNS and failover control      |
| **ACM**         | SSL/TLS certificates          |
| **S3**          | (Optional) Frontend hosting   |

---

## 📁 Repository Structure

```
.
├── lambdas/
│   ├── read_function.py
│   └── write_function.py
├── frontend/
│   └── index.html
└── README.md
```


---

> ✅ Built for educational and demo purposes using AWS best practices for HA and DR in a serverless context.

```
