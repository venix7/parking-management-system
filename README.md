# Smart Parking Management System

A full-stack parking management system built with **Python, Streamlit, FastAPI, and PostgreSQL**. The application manages vehicle entry and exit, automatically assigns suitable parking slots, calculates parking fees, stores parking history, and provides dashboard analytics.

## Live Deployment

| Component | Deployment |
|---|---|
| **Streamlit Frontend** | https://parking-lot-management-system-tew8dadq6fzrrkczs6fb2o.streamlit.app/ |
| **FastAPI Backend** | https://parking-management-system-7sni.onrender.com |
| **API Documentation** | https://parking-management-system-7sni.onrender.com/docs |

The deployed application uses the following architecture:

```text
Streamlit Community Cloud
        ↓
FastAPI Backend on Render
        ↓
Neon PostgreSQL
```

**Neon PostgreSQL** is used as the hosted PostgreSQL database for persistent parking data. The database connection is handled by the FastAPI backend, so no public database URL is exposed in the project README.

> **Note:** The FastAPI backend may take a short time to respond after periods of inactivity because it is hosted on Render.

## Features

- Register and park vehicles
- Automatic parking slot allocation
- Support for bikes, cars, and trucks
- Track currently parked vehicles
- Track vehicle entry and exit times
- Calculate parking fees
- Release parking slots when vehicles exit
- View available parking slots
- Maintain parking history
- Dashboard with:
  - Total parking slots
  - Occupied slots
  - Available slots
  - Occupancy rate
  - Total revenue
- Revenue-over-time analytics
- Streamlit web dashboard
- FastAPI REST API with Swagger documentation
- PostgreSQL database for persistent storage
- Automated tests with Pytest

## Architecture

```text
                  ┌─────────────────────┐
                  │   Streamlit UI      │
                  │   Web Dashboard     │
                  └──────────┬──────────┘
                             │ HTTP Requests
                             ▼
                  ┌─────────────────────┐
                  │    FastAPI API      │
                  │  Backend / Logic    │
                  └──────────┬──────────┘
                             │
                             ▼
                  ┌─────────────────────┐
                  │ PostgreSQL Database │
                  │   Persistent Data   │
                  └─────────────────────┘
```

## Tech Stack

- **Python**
- **Streamlit** — frontend/dashboard
- **FastAPI** — backend REST API
- **PostgreSQL** — database
- **Psycopg** — PostgreSQL connection
- **Pandas** — analytics and data processing
- **Pytest** — testing
- **Uvicorn** — ASGI server
- **Render** — FastAPI deployment
- **Streamlit Community Cloud** — frontend deployment
- **Neon PostgreSQL** — hosted PostgreSQL database

## Project Structure

```text
smart-parking/
│
├── parking_system/
│   ├── api/
│   │   ├── __init__.py
│   │   ├── routes.py
│   │   └── schemas.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── connection.py
│   │   └── schema.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   ├── parking_record.py
│   │   ├── parking_slot.py
│   │   └── vehicle.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   └── parking_service.py
│   │
│   └── utils/
│       ├── __init__.py
│       └── formatting.py
│
├── tests/
│   └── test_parking_service.py
│
├── api.py
├── main.py
├── setup_database.py
├── streamlit_app.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/venix7/parking-management-system.git
cd parking-management-system
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure PostgreSQL

The application expects PostgreSQL connection details through environment variables.

For local PostgreSQL:

```text
DB_HOST=localhost
DB_PORT=5432
DB_NAME=smart_parking
DB_USER=postgres
DB_PASSWORD=your_password
```

For a hosted PostgreSQL database such as Neon:

```text
DATABASE_URL=your_database_connection_string
```

Do not commit database credentials or `.env` files to GitHub.

### 5. Initialize the database

```powershell
python setup_database.py
```

This creates the required database tables and parking slots.

### 6. Start the FastAPI backend

```powershell
uvicorn api:app --reload --port 8000
```

The API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

### 7. Start the Streamlit frontend

Open another terminal, activate the virtual environment, and run:

```powershell
streamlit run streamlit_app.py
```

## Environment Variables

For local development, use environment variables or a local `.env` file.

Example:

```text
DATABASE_URL=your_database_url
```

For the deployed Streamlit application, configure the backend URL through Streamlit Secrets:

```toml
API_URL = "https://parking-management-system-7sni.onrender.com"
```

Do not commit the secrets file to GitHub.

## API

The FastAPI backend provides endpoints for the main parking operations, including:

- Dashboard information
- Parking a vehicle
- Vehicle exit
- Currently parked vehicles
- Available parking slots
- Parking history

Interactive API documentation is available at:

https://parking-management-system-7sni.onrender.com/docs

## Testing

Make sure the virtual environment is activated and Pytest is installed:

```powershell
pip install pytest
```

Run the test suite from the project root:

```powershell
python -m pytest
```


## Security Notes

- Do not commit `.env` files.
- Do not commit Streamlit secrets.
- Do not expose PostgreSQL passwords or connection strings in source code.
- Use environment variables or platform-provided secret management for deployment credentials.

## License

This project is intended as a personal/academic software project.
