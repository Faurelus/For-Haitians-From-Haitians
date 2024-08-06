import os
import secrets

secret_key = secrets.token_hex(32)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', secret_key)
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost/fhfh_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app/static/profile_pics')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024 
    NEWS_API_URL = 'https://newsdata.io/api/1/news'
    NEWS_API_KEY = os.getenv('NEWS_API_KEY', 'pub_48783e8b4cd706c55eb2ca7ed9a01225c10eb')
    # CASH_APP_API_URL = 'https://sandbox.api.cash.app/customer-request/v1 '
    # CASH_APP_API_KEY = os.getenv('CASH_APP_API_KEY', 'EAAAl0fGbWFJFZO29xIPHE279EFHauwMnJx6KkOq1G3N5vkOQHCDrS2swVmgqvPF')
    # CASH_APP_CLIENT_ID = os.getenv('CASH_APP_CLIENT_ID', 'your_cash_app_client_id_here')
    # SQUARE_API_URL = 'https://connect.squareupsandbox.com/v2/payments'
    # SQUARE_ACCESS_TOKEN = os.getenv('SQUARE_ACCESS_TOKEN', 'EAAAluXUB4nr6OcFC5dwSbvfvspR8rrtkttj_yruSvYH__gtAAXJF0S8gN5rTdPf')
    STRIPE_API_KEY = os.getenv('STRIPE_API_KEY', 'sk_test_51PkoXA1B4Zdx1qPGGlM2ODFw8osvG4tlTh2ZejU5cfvBxIl8XPgh1NeZrztUgLQKL0qX3OmPClgS2rAuhOf3esCY00XTCGaLzP')
    STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_51PkoXA1B4Zdx1qPGysKWB56gUkvzgajx7Of9gQWxx4q2Qg4DIlIOWJYmceOBrQFFYYTEbE6mkEAMlg43G0OHCQCu0002Wtesqv')
    DEBUG = True

