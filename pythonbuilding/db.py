# pythonbuilding/db.py
import os
from sqlalchemy import create_engine
from sqlmodel import Session

# Read DB credentials from environment variables
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "mysql-service")  # default if not set
DB_PORT = os.environ.get("DB_PORT", "3306")        # default if not set
DB_NAME = os.environ.get("DB_NAME")

# Create the SQLAlchemy URL
DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine and session
engine = create_engine(DATABASE_URL, echo=True, future=True)

# Dependency for FastAPI routes
def get_session():
    with Session(engine) as session:
        yield session
