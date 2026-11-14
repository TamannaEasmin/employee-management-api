import os
from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker, relationship




# Priority: Environment variable from Render
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    # Fallback for local development
    DATABASE_URL = "postgresql://postgres:12345@localhost:5432/employee_db"

print(f"Connecting to database: {DATABASE_URL[:30]}...")  # To verify it's not localhost


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


class UserAuth(Base):
    __tablename__ = "users_auth"

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    is_admin = Column(Boolean, default=False)


class User(Base):
    __tablename__ = "users_rel"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(150), unique=True, nullable=False)

    orders = relationship("Order", back_populates="user")


class Order(Base):
    __tablename__ = "orders_rel"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users_rel.id"), nullable=False)
    product_name = Column(String(100), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)

    user = relationship("User", back_populates="orders")


# Best practice sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)
print("Tables created successfully!")
