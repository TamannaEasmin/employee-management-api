from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from models import SessionLocal, Employee

app = FastAPI(title="Employee Management API")

# Pydantic Schema (validation)
class EmployeeCreate(BaseModel):
    full_name: str
    email: str
    designation: str
    salary: float

class EmployeeUpdate(BaseModel):
    salary: float | None = None
    is_active: bool | None = None

# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 1. Create Employee (POST)
@app.post("/employees")
def create_employee(emp: EmployeeCreate, db: Session = Depends(get_db)):
    # Check if the email already exists
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
    return {"message": "Employee added successfully!", "employee": new_emp}

# 2. Get All Employees (GET)
@app.get("/employees")
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()

# 3. Get Single Employee by ID (GET)
@app.get("/employees/{emp_id}")
def get_employee(emp_id: int, db: Session = Depends(get_db)):
    emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

# 4. Update Employee (PUT)
@app.put("/employees/{emp_id}")
def update_employee(emp_id: int, emp_update: EmployeeUpdate, db: Session = Depends(get_db)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Only update fields that are provided in the request
    if emp_update.salary is not None:
        db_emp.salary = emp_update.salary
    if emp_update.is_active is not None:
        db_emp.is_active = emp_update.is_active
        
    db.commit()
    db.refresh(db_emp)
    return {"message": "Employee updated!", "employee": db_emp}

# 5. Delete Employee (DELETE)
@app.delete("/employees/{emp_id}")
def delete_employee(emp_id: int, db: Session = Depends(get_db)):
    db_emp = db.query(Employee).filter(Employee.id == emp_id).first()
    if not db_emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    db.delete(db_emp)
    db.commit()
    return {"message": f"Employee with ID {emp_id} deleted successfully!"}
