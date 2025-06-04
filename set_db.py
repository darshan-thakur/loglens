import os
from sqlalchemy import text, create_engine
from dotenv import load_dotenv
from models import DBEngine, Base


# Create loglens database

load_dotenv()
engine = create_engine(os.getenv('DEFAULT_DATABASE_URL'))

with engine.connect() as conn:
    conn.execute(text("COMMIT"))
    result = conn.execute(text("SELECT datname FROM pg_database WHERE datistemplate = false;"))
    databases = [row[0] for row in result.fetchall()]
    if 'loglens' not in databases:
        conn.execute(text("CREATE DATABASE loglens"))
        print("Database creation successful")
    else:
        print("loglens database already exists. Skipping DB creation")

#Create tables

Base.metadata.create_all(DBEngine().engine)

print("Table creation successful")



