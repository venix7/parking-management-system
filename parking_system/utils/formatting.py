from parking_system.models import ParkingSlot, ParkingRecord, Vehicle


def format_vehicle(vehicle: Vehicle, slot_id: int) -> str:
    return (
        f"Number: {vehicle.number} | "
        f"Type: {vehicle.vehicle_type.value} | "
        f"Slot: {slot_id} | "
        f"Entry: {vehicle.entry_time.strftime('%Y-%m-%d %H:%M:%S')}"
    )


def format_slot(slot: ParkingSlot) -> str:
    status = "Occupied" if slot.occupied else "Available"
    return f"Slot {slot.slot_id:02d} ({slot.slot_type.value}) - {status}"


def format_record(record: ParkingRecord) -> str:
    exit_text = (
        record.exit_time.strftime("%Y-%m-%d %H:%M:%S")
        if record.exit_time
        else "-"
    )
    fee_text = f"Rs {record.fee:.2f}" if record.fee is not None else "-"
    return (
        f"{record.vehicle_number} | {record.vehicle_type.value} | "
        f"Slot {record.slot_id:02d} | "
        f"Entry: {record.entry_time.strftime('%Y-%m-%d %H:%M:%S')} | "
        f"Exit: {exit_text} | Fee: {fee_text}"
    )
