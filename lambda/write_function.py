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
