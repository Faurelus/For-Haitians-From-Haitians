from app import create_app, db
from app.models import User, Profile, News, Donation, Fundraiser

app = create_app()

with app.app_context():
    print("App context setup successfully")
    if db:
        print("Database initialized successfully")
    print("Tables detected in the database:", db.Model.metadata.tables.keys())
