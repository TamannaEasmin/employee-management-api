# Employee Management API

A complete REST API built with **FastAPI**, **SQLAlchemy (ORM)**, and **PostgreSQL** to manage employee records. This project demonstrates full CRUD (Create, Read, Update, Delete) operations and follows the 5-step design framework (Question, Remove, Simplify, Speed, Automate).

## 🚀 Features
- **Create Employee:** Add a new employee with name, email, designation, and salary.
- **Read Employees:** Get a list of all employees or a specific employee by ID.
- **Update Employee:** Update salary or active status of an employee.
- **Delete Employee:** Remove an employee from the database.
- **Data Validation:** Uses Pydantic to ensure no duplicate emails and valid data formats.
- **Clean Architecture:** Uses FastAPI `Depends` for database session management.

## 🛠️ Technologies Used
- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Pydantic
- Uvicorn

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone git@github.com:TamannaEasmin/employee-management-api.git
   cd employee-management-api
