from sqlalchemy import create_engine, text

# Database connection details
db_uri = 'postgresql://postgres:your_password@localhost/fhfh_db'

# Create an engine
engine = create_engine(db_uri)

# Connect to the database
with engine.connect() as connection:
    result = connection.execute(text("SELECT current_database();"))
    current_db = result.fetchone()[0]
    print(f"Connected to database: {current_db}")
