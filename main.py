from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import SessionLocal, Employee, User, Order

app = FastAPI(title="Employee & Order Management API")

# ==========================================
# Pydantic Schemas (Data Validation)
# ==========================================
class EmployeeCreate(BaseModel):
    full_name: str
    email: str
    designation: str
    salary: float

class EmployeeUpdate(BaseModel):
    salary: float = None
    is_active: bool = None

class UserCreate(BaseModel):
    name: str
    email: str

class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    amount: float

# ==========================================
# Database Dependency
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# Employee Routes (CRUD)
# ==========================================
@app.post("/employees")
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    existing_emp = db.query(Employee).filter(Employee.email == emp.email).first()
    if existing_emp:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_emp = Employee(
        full_name=emp.full_name,
        email=emp.email,
        designation=emp.designation,
        salary=emp.salary
    )
    db.add(new_emp)
    db.commit()
    db.refresh(new_emp)
    return {"message": "Employee added!", "employee": new_emp}

@app.get("/employees")
def get_employees(
    skip: int = 0, 
    limit: int = 10, 
    designation: str = None, 
    db: Session = Depends(get_db)
):
    query = db.query(Employee)
    if designation:
        query = query.filter(Employee.designation == designation)
    return query.offset(skip).limit(limit).all()

@app.get("/employees/{emp_id}")
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp_update: EmployeeUpdate, db: Session = Depends(get_db)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if emp_update.salary is not None:
        db_emp.salary = emp_update.salary
    if emp_update.is_active is not None:
        db_emp.is_active = emp_update.is_active
        
    db.commit()
    db.refresh(db_emp)
    return {"message": "Employee updated!", "employee": db_emp}

@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_emp)
    db.commit()
    return {"message": f"Employee with ID {emp_id} deleted!"}

# ==========================================
# User & Order Routes (Relational)
# ==========================================
@app.post("/users")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
        
    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"message": "User created!", "user": new_user}

@app.post("/orders")
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    # Check if user exists
    user_exists = db.query(User).filter(User.id == order.user_id).first()
    if not user_exists:
        raise HTTPException(status_code=404, detail="User not found")
        
    new_order = Order(
        user_id=order.user_id,
        product_name=order.product_name,
        amount=order.amount
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return {"message": "Order placed!", "order": new_order}

@app.get("/users/{user_id}/orders")
def get_user_orders(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Relationship gives us direct access to all orders of this user
    return {"user": user.name, "orders": user.orders}