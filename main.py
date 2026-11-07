from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from decimal import Decimal

from models import SessionLocal, Employee, User, Order, UserAuth

app = FastAPI(title="Employee & Order Management API")

# --------------------------
# JWT Config (Change SECRET_KEY in production!)
# --------------------------
SECRET_KEY = "your-super-secret-key-change-this-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# --------------------------
# Auth Helper Functions
# --------------------------
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(lambda: next(get_db()))):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = db.query(UserAuth).filter(UserAuth.username == username).first()
    if user is None:
        raise credentials_exception
    return user

# ==========================================
# Pydantic Schemas
# ==========================================
class EmployeeCreate(BaseModel):
    full_name: str
    email: str
    designation: str
    salary: Decimal

class EmployeeUpdate(BaseModel):
    salary: Decimal | None = None
    is_active: bool | None = None

class UserCreate(BaseModel):
    name: str
    email: str

class OrderCreate(BaseModel):
    user_id: int
    product_name: str
    amount: Decimal

# ==========================================
# DB Dependency
# ==========================================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==========================================
# Employee CRUD Routes
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
    designation: str | None = None,
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
# User & Order Routes
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
    
    return {"user_name": user.name, "orders": user.orders}

# ==========================================
# Auth Routes
# ==========================================
@app.post("/register")
def register(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    existing_user = db.query(UserAuth).filter(UserAuth.username == form_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    safe_password = form_data.password[:72]
    
    hashed_pw = get_password_hash(safe_password) 
    new_user = UserAuth(username=form_data.username, hashed_password=hashed_pw)
    db.add(new_user)
    db.commit()
    return {"message": "User registered successfully!"}

    


@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(UserAuth).filter(UserAuth.username == form_data.username).first()
    
    
    safe_password = form_data.password[:72]
    
    if not user or not verify_password(safe_password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Incorrect username or password")
        
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/protected-data")
def protected_route(current_user: UserAuth = Depends(get_current_user)):
    return {"message": f"Hello {current_user.username}, you are seeing protected data!", "username": current_user.username, "is_admin": current_user.is_admin}
