import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Force tests to use an in-memory SQLite database
os.environ["DATABASE_URL"] = "sqlite:///./test.db"

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Create tables in the test database
    engine = create_engine("sqlite:///./test.db", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up after tests
    Base.metadata.drop_all(bind=engine)
