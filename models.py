from sqlalchemy import create_engine, Column, Integer, String, Numeric, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker,relationship

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


#user model
class User(Base):
    __tablename__ ="users_rel"

    id = Column(Integer,primary_key=True)
    name =Column(String(100),nullable = False)
    email=Column(String(150),unique=True,nullable=False)

    #one-to-many Relationship(User- order)
    orders = relationship("Order", back_populates="user")

#order model
class Order(Base):
    __tablename__ = "orders_rel"
    id=Column(Integer,primary_key=True)
    user_id =Column(Integer,ForeignKey("users_rel.id"),nullable=False)
    product_name= Column(String(100),nullable=False)
    amount = Column(Numeric(10,4),nullable =False)

    #many to one relationship (Order-User)
    user = relationship("User", back_populates="orders")




SessionLocal = sessionmaker(bind=engine)

Base.metadata.create_all(bind=engine)
