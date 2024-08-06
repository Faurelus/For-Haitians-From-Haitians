from app import create_app, db
from app.models import User, Profile, Fundraiser, Donation, News
from datetime import datetime
from faker import Faker

app = create_app()
faker = Faker()

with app.app_context():
    # Create the database and the database table
    db.create_all()

    # Insert user data
    users = []
    for _ in range(10):
        user = User(username=faker.user_name(), email=faker.email(), password_hash=faker.password())
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Insert profile data
    for user in users:
        profile = Profile(user_id=user.id, bio=faker.text(), avatar=faker.image_url())
        db.session.add(profile)
    db.session.commit()

    # Insert fundraiser data
    for _ in range(5):
        fundraiser = Fundraiser(
            user_id=faker.random_element(users).id,
            title=faker.sentence(),
            description=faker.text(),
            goal_amount=faker.random_int(min=500, max=10000),
            current_amount=faker.random_int(min=0, max=5000),
            created_at=datetime.now()
        )
        db.session.add(fundraiser)
    db.session.commit()

    # Insert donation data
    fundraisers = Fundraiser.query.all()
    for _ in range(20):
        donation = Donation(
            user_id=faker.random_element(users).id,
            fundraiser_id=faker.random_element(fundraisers).id,
            amount=faker.random_int(min=10, max=500),
            created_at=datetime.now()
        )
        db.session.add(donation)
    db.session.commit()

    # Insert news data
    for _ in range(5):
        news = News(
            title=faker.sentence(),
            content=faker.text(),
            created_at=datetime.now()
        )
        db.session.add(news)
    db.session.commit()

    print("Database seeded with fake data!")
