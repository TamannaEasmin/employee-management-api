# Employee Management API

A complete backend REST API built with **FastAPI**, **SQLAlchemy (ORM)**, and **PostgreSQL**. This project features a secure JWT-based authentication system, relational database design, Docker containerization, and CI/CD via GitHub Actions.

![Python Tests](https://github.com/TamannaEasmin/employee-management-api/actions/workflows/test.yml/badge.svg)

## 🚀 Features
- **Employee Management (CRUD):** Create, Read, Update, and Delete employee records with pagination and filtering.
- **User & Order Management (Relational):** Create users and place orders linked to them (One-to-Many Relationship).
- **Secure Authentication (JWT):** User registration, password hashing (bcrypt), and protected routes.
- **Automated Testing:** Full test coverage using `pytest` and `httpx`.
- **CI/CD:** GitHub Actions workflow runs tests automatically on every push.

## 🛠️ Technologies Used
- **Framework:** FastAPI
- **Database:** PostgreSQL, SQLAlchemy (ORM)
- **Authentication:** JWT (python-jose), Passlib (bcrypt)
- **Testing:** pytest, httpx
- **Deployment:** Docker, Docker Hub, Render

## 🗄️ Database Schema
- **`employees`**: Employee details (id, name, email, designation, salary, is_active).
- **`users_rel`**: Customer details for orders.
- **`orders_rel`**: Order details linked to `users_rel` via Foreign Key.
- **`users_auth`**: Login credentials (hashed passwords) for JWT authentication.

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone git@github.com:TamannaEasmin/employee-management-api.git
   cd employee-management-api
Create a virtual environment and install dependencies:

bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
Set up the Database:

Ensure PostgreSQL is running and create a database named employee_db.

Update DATABASE_URL in models.py if necessary.

Run the server:

bash
uvicorn main:app --reload
Open http://127.0.0.1:8000/docs to test the API.

🐳 Running with Docker
Build the Docker image:

bash
docker build -t tamannaeasmin/employee-api:v2 .
Run the container:

bash
docker run -p 8000:8000 tamannaeasmin/employee-api:v2
🧪 Running Tests
To run the automated tests:

bash
pytest -v
(GitHub Actions will automatically run these tests on every push to main).

🌐 Live Demo
The API is deployed and live at:
https://employee-management-api-zscg.onrender.com/docs

👩‍💻 Author
Tamanna Easmin
GitHub Profile