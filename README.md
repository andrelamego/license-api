# 🔑 License Key API

A clean and modern REST API built with **FastAPI + SQLAlchemy**, designed to manage software **license keys** with full CRUD operations, expiration validation, and renewal logic.

---

## Features

- **Single-table design** – just licenses, no user management
- **Automatic expiration** – each license expires after a given number of days
- **Unique license keys** – generated using `UUID4`
- **Status system** – `active`, `inactive`, or `expired`
- **Renewal endpoint** – easily extend license duration
- **SQLite by default**, easily switchable to PostgreSQL
- **Clean structure**, ready for Docker, Render, Railway, etc.

---

## Project Structure

license_api/
│
├── main.py # FastAPI entry point  
├── models.py # SQLAlchemy ORM models  
├── schemas.py # Pydantic schemas for request/response  
├── database.py # Database connection (SQLite/PostgreSQL)  
├── utils.py # Helper functions (key generator, expiration)  
├── requirements.txt # Project dependencies  
├── README.md # Documentation  
└── LICENSE # License file  

---

## Installation

### Requirements

- Python **3.10+**
- pip
- (optional) PostgreSQL or any SQL-compatible database

### Setup

```bash
git clone https://github.com/andrelamego/license-api.git
cd license-api

pip install -r requirements.txt
```

---

### Endpoints Overview

| Method   | Endpoint                   | Description                                   |
| -------- | -------------------------- | --------------------------------------------- |
| **POST** | `/license/create`          | Create a new license key                      |
| **POST** | `/license/verify`          | Verify if a license is valid/expired/inactive |
| **GET**  | `/licenses`                | List all licenses                             |
| **PUT**  | `/license/deactivate/{id}` | Deactivate a license                          |
| **PUT**  | `/license/renew/{id}`      | Renew license for +30 days                    |

---

### Usage Examples

#### Create License

POST /license/create

```json
{
  "plan": "monthly",
  "duration_days": 30
}
```

✅ Response:

```json
{
  "id": 1,
  "key": "cb2c03b1-6375-4f84-a3a9-3f0df0a421e2",
  "plan": "monthly",
  "expires_at": "2025-12-09T22:15:30.000Z",
  "is_active": true,
  "created_at": "2025-11-09T22:15:30.000Z"
}
```

#### Verify License

POST /license/verify

```json
{
  "key": "cb2c03b1-6375-4f84-a3a9-3f0df0a421e2"
}
```


✅ Valid response:

```json
{
  "valid": true,
  "license": {
    "id": 1,
    "key": "cb2c03b1-6375-4f84-a3a9-3f0df0a421e2",
    "plan": "monthly",
    "expires_at": "2025-12-09T22:15:30.000Z",
    "is_active": true,
    "created_at": "2025-11-09T22:15:30.000Z"
  }
}
```



❌ Expired response:

```
{
  "valid": false,
  "reason": "expired"
}
```

#### Renew License

PUT /license/renew/1

✅ Response:

```json
{
  "id": 1,
  "key": "cb2c03b1-6375-4f84-a3a9-3f0df0a421e2",
  "plan": "monthly",
  "expires_at": "2026-01-08T22:15:30.000Z",
  "is_active": true,
  "created_at": "2025-11-09T22:15:30.000Z"
}
```

#### Deactivate License

PUT /license/deactivate/1

✅ Response:

```json
{
  "id": 1,
  "key": "cb2c03b1-6375-4f84-a3a9-3f0df0a421e2",
  "plan": "monthly",
  "expires_at": "2025-12-09T22:15:30.000Z",
  "is_active": false,
  "created_at": "2025-11-09T22:15:30.000Z"
}
```

---

## 👨‍💻 Author

André Lamego
💼 Fullstack Developer
📧 Contact: andreolamego@gmail.com

🌐 GitHub: @andrelamego