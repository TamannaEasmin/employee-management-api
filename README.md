# Employee Management API (with JWT Authentication)

A backend REST API built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**. It covers full CRUD, a one-to-many relationship, and JWT-based authentication.

## 🚀 Features

- **Employee Management (CRUD)** — create, read, update, delete, with pagination and filtering by designation.
- **Users & Orders (One-to-Many)** — create users, place orders linked to a user, and fetch all orders of a user.
- **Secure Authentication (JWT)** — registration with bcrypt hashing, login returns a JWT access token, protected routes require a valid token.
- **Data Validation** — Pydantic prevents invalid data and duplicate emails/usernames.
- **Clean Architecture** — FastAPI `Depends` for database sessions and route protection.

## 🛠️ Technologies Used

- Python 3.10+
- FastAPI
- SQLAlchemy (ORM)
- PostgreSQL
- Pydantic
- Passlib & Bcrypt (password hashing)
- Python-JOSE (JWT)
- Uvicorn

## 🗄️ Database Schema

- **`employees`** — employee details and status.
- **`users_rel`** — user/customer details.
- **`orders_rel`** — orders linked to `users_rel` by foreign key.
- **`users_auth`** — login credentials (hashed passwords) for JWT auth.

## ⚙️ How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone git@github.com:TamannaEasmin/employee-management-api.git
   cd employee-management-api
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
   - Make sure PostgreSQL is installed and running.
   - Create the database:
     ```bash
     sudo -u postgres psql -c "CREATE DATABASE employee_db;"
     ```
   - Update `DATABASE_URL` in `models.py` with your credentials.

5. **Create the tables:**
   ```bash
   python -c "from models import Base, engine; Base.metadata.create_all(bind=engine)"
   ```

6. **Run the server:**
   ```bash
   uvicorn main:app --reload
   ```

7. **Open the API docs:** go to `http://127.0.0.1:8000/docs`.

## 🔐 How to Test Authentication

1. `POST /register` — create a user, e.g. `username: tamanna`, `password: 12345`.
2. `POST /login` — use the same credentials and copy the `access_token` from the response.
3. Click **Authorize** at the top right and enter your **username and password**. This API uses the OAuth2 password flow, so Swagger logs in for you — do not paste the token here.
4. `GET /protected-data` — Execute and you should see a greeting. Click **Logout** and call it again to confirm `401 Unauthorized`.

## 👩‍💻 Author

**Tamanna Easmin**
[GitHub Profile](https://github.com/TamannaEasmin)
