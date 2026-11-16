import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Ensure the database URL is set for tests
DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://postgres:12345@localhost:5432/employee_db")

@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    # Create tables in the database before running tests
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield
    # Clean up: Drop all tables after tests
    Base.metadata.drop_all(bind=engine)
