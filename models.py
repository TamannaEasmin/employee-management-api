from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

# NEW DATABASE  employee_db
DATABASE_URL = "postgresql://postgres:12345@localhost:5432/employee_db"
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class Employee(Base):
    __tablename__ = "employees"
    
    id = Column(Integer, primary_key=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)
    designation = Column(String(100), nullable=False)
    salary = Column(Numeric(10, 2), nullable=False)
    is_active = Column(Boolean, default=True)

SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)
