# Employee & Order Management API

A complete REST API built with **FastAPI**, **SQLAlchemy (ORM)**, and **PostgreSQL**. This project demonstrates full CRUD operations along with **One-to-Many Relational Database** implementation.

## 🚀 Features
- **Employee Management (CRUD):**
  - Create, Read, Update, and Delete employee records.
  - Pagination and filtering by designation.
- **User & Order Management (Relational):**
  - Create users.
  - Place orders linked to specific users (Foreign Key).
  - Fetch all orders belonging to a specific user (One-to-Many Relationship).
- **Data Validation:** Uses Pydantic to ensure valid data and prevent duplicate emails.
- **Clean Architecture:** Uses FastAPI `Depends` for database session management.

## 🛠️ Technologies Used
- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Pydantic
- Uvicorn

## 🗄️ Database Schema
- **`employees`**: Stores employee details (id, name, email, designation, salary, is_active).
- **`users_rel`**: Stores user details (id, name, email).
- **`orders_rel`**: Stores order details (id, user_id [FK], product_name, amount).

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone git@github.com:TamannaEasmin/employee-management-api.git
   cd employee-management-api
2. **Create and activate a virtual environment:**
python3 -m venv .venv
source .venv/bin/activate

3.**Install dependencies:**

pip install -r requirements.txt

4.**Set up the Database:**

Ensure PostgreSQL is installed and running.

Create a database named employee_db:

sudo -u postgres psql -c "CREATE DATABASE employee_db;"
Update DATABASE_URL in models.py with your credentials.

5.**Create Database Tables:**

bash
python -c "from models import Base, engine; Base.metadata.create_all(bind=engine)"
Run the server:

bash
uvicorn main:app --reload
Test the API:
Open the browser and go to http://127.0.0.1:8000/docs to view the Swagger UI.

👩‍💻 Author
Tamanna Easmin
GitHub Profile