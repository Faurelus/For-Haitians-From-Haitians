import requests
from flask import current_app

def fetch_news():
    url = f"{current_app.config['NEWS_API_URL']}?apikey={current_app.config['NEWS_API_KEY']}&q=haiti&country=ht"
    response = requests.get(url)
    return response.json()
