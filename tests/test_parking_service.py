from datetime import datetime, timedelta

from parking_system.models import VehicleType
from parking_system.services import ParkingService


def test_initial_slots():
    service = ParkingService()

    assert service.get_total_slots() == 100
    assert service.get_occupied_count() == 0
    assert service.get_available_count() == 100


def test_park_vehicle_assigns_matching_slot():
    service = ParkingService()

    success, message, slot_id = service.park_vehicle(
        "ka01ab1234",
        VehicleType.CAR,
    )

    assert success is True
    assert slot_id == 21
    assert service.get_vehicle("KA01AB1234") is not None
    assert service.get_slot(slot_id).occupied is True


def test_duplicate_vehicle_is_rejected():
    service = ParkingService()

    service.park_vehicle("KA01AB1234", VehicleType.CAR)
    success, message, slot_id = service.park_vehicle(
        "KA01AB1234",
        VehicleType.CAR,
    )

    assert success is False
    assert "already parked" in message.lower()


def test_exit_vehicle_calculates_fee_and_frees_slot():
    service = ParkingService()

    entry = datetime(2026, 8, 17, 10, 0)
    exit_time = entry + timedelta(hours=2)

    success, _, slot_id = service.park_vehicle(
        "KA01AB1234",
        VehicleType.CAR,
        entry_time=entry,
    )

    assert success is True

    success, message, fee = service.exit_vehicle(
        "KA01AB1234",
        exit_time=exit_time,
    )

    assert success is True
    assert fee == 30.0
    assert service.get_slot(slot_id).occupied is False
    assert service.get_vehicle("KA01AB1234") is None
    assert len(service.get_parking_history()) == 1


def test_vehicle_type_specific_fee():
    service = ParkingService()

    entry = datetime(2026, 8, 17, 10, 0)
    exit_time = entry + timedelta(hours=1)

    service.park_vehicle("BIKE01", VehicleType.BIKE, entry)
    _, _, bike_fee = service.exit_vehicle("BIKE01", exit_time)

    service.park_vehicle("TRUCK01", VehicleType.TRUCK, entry)
    _, _, truck_fee = service.exit_vehicle("TRUCK01", exit_time)

    assert bike_fee == 10.0
    assert truck_fee == 30.0
