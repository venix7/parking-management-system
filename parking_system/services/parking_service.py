from datetime import datetime
from typing import List, Optional, Tuple

from parking_system.database.connection import get_connection
from parking_system.models import (
    ParkingRecord,
    ParkingSlot,
    Vehicle,
    VehicleType,
)


class ParkingService:
    """
    Contains the core parking-management logic.

    This class deliberately does not use input(), print(), Streamlit,
    FastAPI, or database code. That keeps the business logic reusable
    by a CLI, API, or GUI later.
    """

    def __init__(self) -> None:
        pass


    def find_available_slot(
        self,
        vehicle_type: VehicleType,
    ) -> Optional[ParkingSlot]:

        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT slot_id, slot_type, occupied
                    FROM parking_slots
                    WHERE slot_type = %s
                    AND occupied = FALSE
                    ORDER BY slot_id
                    LIMIT 1;
                    """,
                    (vehicle_type.value,),
                )

                row = cursor.fetchone()

        if row is None:
            return None

        return ParkingSlot(
            slot_id=row[0],
            slot_type=VehicleType(row[1]),
            occupied=row[2],
        )

    def calculate_fee(
        self,
        vehicle: Vehicle,
        exit_time: Optional[datetime] = None,
    ) -> float:
        if exit_time is None:
            exit_time = datetime.now()

        minutes = int((exit_time - vehicle.entry_time).total_seconds() // 60)

        # Minimum charge is one hour.
        hours = max(1, (minutes + 59) // 60)

        fee = 20.0

        if hours > 1:
            fee += (hours - 1) * 10.0

        if vehicle.vehicle_type == VehicleType.BIKE:
            fee *= 0.5
        elif vehicle.vehicle_type == VehicleType.TRUCK:
            fee *= 1.5

        return fee

    def park_vehicle(
        self,
        number: str,
        vehicle_type: VehicleType,
        entry_time: Optional[datetime] = None,
    ) -> Tuple[bool, str, Optional[int]]:

        number = number.strip().upper()

        if not number:
            return False, "Vehicle number cannot be empty.", None

        if entry_time is None:
            entry_time = datetime.now()

        with get_connection() as connection:
            with connection.cursor() as cursor:

                # Check whether the vehicle is already parked.
                cursor.execute(
                    """
                    SELECT v.id
                    FROM vehicles v
                    JOIN parking_records pr
                        ON v.id = pr.vehicle_id
                    WHERE v.registration_number = %s
                    AND pr.exit_time IS NULL;
                    """,
                    (number,),
                )

                if cursor.fetchone() is not None:
                    return False, "Vehicle is already parked.", None

                # Find available slot.
                cursor.execute(
                    """
                    SELECT slot_id
                    FROM parking_slots
                    WHERE slot_type = %s
                    AND occupied = FALSE
                    ORDER BY slot_id
                    LIMIT 1
                    FOR UPDATE;
                    """,
                    (vehicle_type.value,),
                )

                slot = cursor.fetchone()

                if slot is None:
                    return (
                        False,
                        f"No {vehicle_type.value.lower()} slot is available.",
                        None,
                    )

                slot_id = slot[0]

                # Create/find vehicle.
                cursor.execute(
                    """
                    INSERT INTO vehicles
                        (registration_number, vehicle_type)
                    VALUES (%s, %s)
                    ON CONFLICT (registration_number)
                    DO UPDATE SET vehicle_type = EXCLUDED.vehicle_type
                    RETURNING id;
                    """,
                    (number, vehicle_type.value),
                )

                vehicle_id = cursor.fetchone()[0]

                # Mark slot occupied.
                cursor.execute(
                    """
                    UPDATE parking_slots
                    SET occupied = TRUE
                    WHERE slot_id = %s;
                    """,
                    (slot_id,),
                )

                # Create parking record.
                cursor.execute(
                    """
                    INSERT INTO parking_records
                        (vehicle_id, slot_id, entry_time)
                    VALUES (%s, %s, %s);
                    """,
                    (vehicle_id, slot_id, entry_time),
                )

            connection.commit()

        return (
            True,
            f"Vehicle parked successfully in slot {slot_id}.",
            slot_id,
        )

    def calculate_fee(self, vehicle: Vehicle, exit_time: datetime) -> float:
        duration = exit_time - vehicle.entry_time

        minutes = int(duration.total_seconds() / 60)

        hours = (minutes + 59) // 60

        if hours == 0:
            hours = 1

        fee = 20.0

        if hours > 1:
            fee += (hours - 1) * 10

        if vehicle.vehicle_type == VehicleType.BIKE:
            fee *= 0.5

        elif vehicle.vehicle_type == VehicleType.TRUCK:
            fee *= 1.5

        return fee

    def exit_vehicle(
        self,
        number: str,
        exit_time: Optional[datetime] = None,
    ) -> Tuple[bool, str, Optional[float]]:

        number = number.strip().upper()

        if exit_time is None:
            exit_time = datetime.now()

        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        pr.id,
                        v.id,
                        v.registration_number,
                        v.vehicle_type,
                        pr.slot_id,
                        pr.entry_time
                    FROM parking_records pr
                    JOIN vehicles v
                        ON v.id = pr.vehicle_id
                    WHERE v.registration_number = %s
                    AND pr.exit_time IS NULL;
                    """,
                    (number,),
                )

                row = cursor.fetchone()

                if row is None:
                    return False, "Vehicle not found.", None

                record_id = row[0]
                slot_id = row[4]
                entry_time = row[5]
                vehicle_type = VehicleType(row[3])

                vehicle = Vehicle(
                    number,
                    vehicle_type,
                    entry_time,
                )

                fee = self.calculate_fee(vehicle, exit_time)

                # Complete parking record.
                cursor.execute(
                    """
                    UPDATE parking_records
                    SET exit_time = %s,
                        fee = %s
                    WHERE id = %s;
                    """,
                    (exit_time, fee, record_id),
                )

                # Free slot.
                cursor.execute(
                    """
                    UPDATE parking_slots
                    SET occupied = FALSE
                    WHERE slot_id = %s;
                    """,
                    (slot_id,),
                )

            connection.commit()

        return (
            True,
            f"Vehicle exited successfully from slot {slot_id}.",
            fee,
        )

    def get_active_vehicles(self):
        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        v.registration_number,
                        v.vehicle_type,
                        pr.entry_time,
                        pr.slot_id
                    FROM vehicles v
                    JOIN parking_records pr
                        ON v.id = pr.vehicle_id
                    WHERE pr.exit_time IS NULL
                    ORDER BY pr.slot_id;
                    """
                )

                rows = cursor.fetchall()

        return [
            (
                Vehicle(
                    number=row[0],
                    vehicle_type=VehicleType(row[1]),
                    entry_time=row[2],
                ),
                row[3],
            )
            for row in rows
        ]

    def get_available_slots(self) -> List[ParkingSlot]:

        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT slot_id, slot_type, occupied
                    FROM parking_slots
                    WHERE occupied = FALSE
                    ORDER BY slot_id;
                    """
                )

                rows = cursor.fetchall()

        return [
            ParkingSlot(
                slot_id=row[0],
                slot_type=VehicleType(row[1]),
                occupied=row[2],
            )
            for row in rows
        ]

    def get_occupied_slots(self) -> List[ParkingSlot]:

        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT slot_id, slot_type, occupied
                    FROM parking_slots
                    WHERE occupied = TRUE
                    ORDER BY slot_id;
                    """
                )

                rows = cursor.fetchall()

        return [
            ParkingSlot(
                slot_id=row[0],
                slot_type=VehicleType(row[1]),
                occupied=row[2],
            )
            for row in rows
        ]

    def get_slot(self, slot_id: int) -> Optional[ParkingSlot]:
        for slot in self.slots:
            if slot.slot_id == slot_id:
                return slot
        return None

    def get_vehicle(self, number: str) -> Optional[Vehicle]:
        return self.active_vehicles.get(number.strip().upper())

    def get_total_slots(self) -> int:

        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    "SELECT COUNT(*) FROM parking_slots;"
                )

                return cursor.fetchone()[0]

    def get_occupied_count(self) -> int:

        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM parking_slots
                    WHERE occupied = TRUE;
                    """
                )

                return cursor.fetchone()[0]

    def get_available_count(self) -> int:
        return self.get_total_slots() - self.get_occupied_count()

    def get_occupancy_rate(self) -> float:

        total = self.get_total_slots()

        if total == 0:
            return 0.0

        occupied = self.get_occupied_count()

        return occupied / total * 100

    def get_total_revenue(self) -> float:

        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT COALESCE(SUM(fee), 0)
                    FROM parking_records
                    WHERE fee IS NOT NULL;
                    """
                )

                return float(cursor.fetchone()[0])

    def get_parking_history(self) -> List[ParkingRecord]:

        with get_connection() as connection:
            with connection.cursor() as cursor:

                cursor.execute(
                    """
                    SELECT
                        v.registration_number,
                        v.vehicle_type,
                        pr.slot_id,
                        pr.entry_time,
                        pr.exit_time,
                        pr.fee
                    FROM parking_records pr
                    JOIN vehicles v
                        ON v.id = pr.vehicle_id
                    ORDER BY pr.entry_time DESC;
                    """
                )

                rows = cursor.fetchall()

        return [
            ParkingRecord(
                vehicle_number=row[0],
                vehicle_type=VehicleType(row[1]),
                slot_id=row[2],
                entry_time=row[3],
                exit_time=row[4],
                fee=float(row[5]) if row[5] is not None else None,
            )
            for row in rows
        ]
