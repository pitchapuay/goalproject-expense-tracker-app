import json

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    amount = body.get("amount", "")
    
    # Here you could add code to save the expense (e.g., to DynamoDB)
    
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"message": f"Expense {amount} saved!"})
    }