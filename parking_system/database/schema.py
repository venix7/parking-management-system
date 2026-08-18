from parking_system.database.connection import get_connection
from parking_system.models import VehicleType


def create_tables():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS parking_slots (
                    slot_id INTEGER PRIMARY KEY,
                    slot_type VARCHAR(20) NOT NULL,
                    occupied BOOLEAN NOT NULL DEFAULT FALSE
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vehicles (
                    id SERIAL PRIMARY KEY,
                    registration_number VARCHAR(20) UNIQUE NOT NULL,
                    vehicle_type VARCHAR(20) NOT NULL
                );
            """)

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS parking_records (
                    id SERIAL PRIMARY KEY,
                    vehicle_id INTEGER NOT NULL
                        REFERENCES vehicles(id),
                    slot_id INTEGER NOT NULL
                        REFERENCES parking_slots(slot_id),
                    entry_time TIMESTAMP NOT NULL,
                    exit_time TIMESTAMP,
                    fee DECIMAL(10, 2)
                );
            """)

        connection.commit()


def create_default_slots():
    with get_connection() as connection:
        with connection.cursor() as cursor:

            slot_id = 1

            # 20 Bike slots
            for _ in range(20):
                cursor.execute(
                    """
                    INSERT INTO parking_slots
                        (slot_id, slot_type)
                    VALUES (%s, %s)
                    ON CONFLICT (slot_id) DO NOTHING;
                    """,
                    (slot_id, VehicleType.BIKE.value),
                )
                slot_id += 1

            # 70 Car slots
            for _ in range(70):
                cursor.execute(
                    """
                    INSERT INTO parking_slots
                        (slot_id, slot_type)
                    VALUES (%s, %s)
                    ON CONFLICT (slot_id) DO NOTHING;
                    """,
                    (slot_id, VehicleType.CAR.value),
                )
                slot_id += 1

            # 10 Truck slots
            for _ in range(10):
                cursor.execute(
                    """
                    INSERT INTO parking_slots
                        (slot_id, slot_type)
                    VALUES (%s, %s)
                    ON CONFLICT (slot_id) DO NOTHING;
                    """,
                    (slot_id, VehicleType.TRUCK.value),
                )
                slot_id += 1

        connection.commit()