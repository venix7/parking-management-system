# Smart Parking Management System — Steps 1 & 2

This is the first stage of the planned Smart Parking Management System.

## Current scope

### Step 1 — Python parking system

The original C++ CLI project's core functionality has been recreated in Python:

- Register/park a vehicle
- Assign a matching parking slot
- Prevent duplicate active vehicles
- Remove/exit a vehicle
- Calculate parking fees
- Display active vehicles
- Display available slots
- Maintain in-memory parking history
- Show basic occupancy and revenue information

### Step 2 — Clean Python architecture

The parking logic has been separated from the command-line interface.

The important design rule is:

> `ParkingService` contains business logic and does not use `input()` or `print()`.

This makes the same service reusable later by FastAPI and other interfaces.

## Project structure

```text
smart_parking_step1_step2/
├── main.py
├── parking_system/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── enums.py
│   │   ├── vehicle.py
│   │   ├── parking_slot.py
│   │   └── parking_record.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── parking_service.py
│   └── utils/
│       ├── __init__.py
│       └── formatting.py
├── tests/
│   └── test_parking_service.py
└── README.md
```

## Requirements

- Python 3.10 or newer
- No external packages are required for the application itself.

## Run the application

From the project root:

```bash
python main.py
```

## Run tests

If `pytest` is installed:

```bash
pytest
```

## Important note

Data is currently stored only in memory. Closing the application loses active vehicles and parking history.

That is intentional.

PostgreSQL will be introduced in the next stage, and FastAPI will be introduced after the core application logic is ready.
