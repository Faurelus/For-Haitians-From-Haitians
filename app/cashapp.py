import requests
import secrets
from flask import current_app

def create_payment(amount, currency='USD'):
    url = f"{current_app.config['https://api.cash.app']}/v1/payments"
    headers = {
        'Authorization': f"Bearer {current_app.config['CASH_APP_API_KEY']}",
        'Content-Type': 'application/json'
    }
    payload = {
        'amount_money': {
            'amount': amount * 100,  # Convert to cents
            'currency': currency
        },
        'source_id': 'CASH_APP',  # Assuming you are using Cash App as a source
        'idempotency_key': secrets.token_hex(16)
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()