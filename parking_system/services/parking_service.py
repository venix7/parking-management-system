from datetime import datetime
from typing import Dict, List, Optional, Tuple

from parking_system.models import ParkingRecord, ParkingSlot, Vehicle, VehicleType


class ParkingService:
    """
    Contains the core parking-management logic.

    This class deliberately does not use input(), print(), Streamlit,
    FastAPI, or database code. That keeps the business logic reusable
    by a CLI, API, or GUI later.
    """

    def __init__(self) -> None:
        self.slots: List[ParkingSlot] = []
        self.active_vehicles: Dict[str, Vehicle] = {}
        self.vehicle_to_slot: Dict[str, int] = {}
        self.parking_history: List[ParkingRecord] = []

        self._create_default_slots()

    def _create_default_slots(self) -> None:
        slot_id = 1

        for _ in range(20):
            self.slots.append(ParkingSlot(slot_id, VehicleType.BIKE))
            slot_id += 1

        for _ in range(70):
            self.slots.append(ParkingSlot(slot_id, VehicleType.CAR))
            slot_id += 1

        for _ in range(10):
            self.slots.append(ParkingSlot(slot_id, VehicleType.TRUCK))
            slot_id += 1

    def find_available_slot(self, vehicle_type: VehicleType) -> Optional[ParkingSlot]:
        for slot in self.slots:
            if not slot.occupied and slot.slot_type == vehicle_type:
                return slot
        return None

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

        if number in self.active_vehicles:
            return False, "Vehicle is already parked.", None

        slot = self.find_available_slot(vehicle_type)

        if slot is None:
            return False, f"No {vehicle_type.value.lower()} slot is available.", None

        if entry_time is None:
            entry_time = datetime.now()

        vehicle = Vehicle(number, vehicle_type, entry_time)

        self.active_vehicles[number] = vehicle
        self.vehicle_to_slot[number] = slot.slot_id
        slot.occupied = True

        return (
            True,
            f"Vehicle parked successfully in slot {slot.slot_id}.",
            slot.slot_id,
        )

    def exit_vehicle(
        self,
        number: str,
        exit_time: Optional[datetime] = None,
    ) -> Tuple[bool, str, Optional[float]]:
        number = number.strip().upper()

        vehicle = self.active_vehicles.get(number)

        if vehicle is None:
            return False, "Vehicle not found.", None

        if exit_time is None:
            exit_time = datetime.now()

        fee = self.calculate_fee(vehicle, exit_time)
        slot_id = self.vehicle_to_slot[number]

        slot = next(
            slot for slot in self.slots
            if slot.slot_id == slot_id
        )
        slot.occupied = False

        self.parking_history.append(
            ParkingRecord(
                vehicle_number=vehicle.number,
                vehicle_type=vehicle.vehicle_type,
                slot_id=slot_id,
                entry_time=vehicle.entry_time,
                exit_time=exit_time,
                fee=fee,
            )
        )

        del self.active_vehicles[number]
        del self.vehicle_to_slot[number]

        return (
            True,
            f"Vehicle exited successfully from slot {slot_id}.",
            fee,
        )

    def get_active_vehicles(self) -> List[Tuple[Vehicle, int]]:
        return [
            (vehicle, self.vehicle_to_slot[number])
            for number, vehicle in self.active_vehicles.items()
        ]

    def get_available_slots(self) -> List[ParkingSlot]:
        return [slot for slot in self.slots if not slot.occupied]

    def get_occupied_slots(self) -> List[ParkingSlot]:
        return [slot for slot in self.slots if slot.occupied]

    def get_slot(self, slot_id: int) -> Optional[ParkingSlot]:
        for slot in self.slots:
            if slot.slot_id == slot_id:
                return slot
        return None

    def get_vehicle(self, number: str) -> Optional[Vehicle]:
        return self.active_vehicles.get(number.strip().upper())

    def get_total_slots(self) -> int:
        return len(self.slots)

    def get_occupied_count(self) -> int:
        return len(self.active_vehicles)

    def get_available_count(self) -> int:
        return len(self.slots) - len(self.active_vehicles)

    def get_occupancy_rate(self) -> float:
        if not self.slots:
            return 0.0
        return self.get_occupied_count() / len(self.slots) * 100

    def get_total_revenue(self) -> float:
        return sum(record.fee or 0.0 for record in self.parking_history)

    def get_parking_history(self) -> List[ParkingRecord]:
        return list(self.parking_history)
