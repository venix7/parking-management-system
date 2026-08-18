from fastapi import APIRouter

from parking_system.api.schemas import (
    DashboardResponse,
    ExitVehicleRequest,
    ExitVehicleResponse,
    ParkVehicleRequest,
    ParkVehicleResponse,
    SlotResponse,
    VehicleResponse,
)

from parking_system.services.parking_service import ParkingService


router = APIRouter()

service = ParkingService()

@router.post("/vehicles/park", response_model=ParkVehicleResponse)
def park_vehicle(request: ParkVehicleRequest):

    success, message, slot_id = service.park_vehicle(
        request.registration_number,
        request.vehicle_type,
    )

    return ParkVehicleResponse(
        success=success,
        message=message,
        slot_id=slot_id,
    )

@router.post("/vehicles/exit", response_model=ExitVehicleResponse)
def exit_vehicle(request: ExitVehicleRequest):

    success, message, fee = service.exit_vehicle(
        request.registration_number
    )

    return ExitVehicleResponse(
        success=success,
        message=message,
        fee=fee,
    )

@router.get("/vehicles", response_model=list[VehicleResponse])
def get_active_vehicles():

    vehicles = service.get_active_vehicles()

    return [
        VehicleResponse(
            registration_number=vehicle.number,
            vehicle_type=vehicle.vehicle_type.value,
            slot_id=slot_id,
            entry_time=vehicle.entry_time.isoformat(),
        )
        for vehicle, slot_id in vehicles
    ]

@router.get("/slots/available", response_model=list[SlotResponse])
def get_available_slots():

    slots = service.get_available_slots()

    return [
        SlotResponse(
            slot_id=slot.slot_id,
            slot_type=slot.slot_type.value,
            occupied=slot.occupied,
        )
        for slot in slots
    ]

@router.get("/slots/occupied", response_model=list[SlotResponse])
def get_occupied_slots():

    slots = service.get_occupied_slots()

    return [
        SlotResponse(
            slot_id=slot.slot_id,
            slot_type=slot.slot_type.value,
            occupied=slot.occupied,
        )
        for slot in slots
    ]

@router.get("/dashboard", response_model=DashboardResponse)
def get_dashboard():

    return DashboardResponse(
        total_slots=service.get_total_slots(),
        occupied_slots=service.get_occupied_count(),
        available_slots=service.get_available_count(),
        occupancy_rate=service.get_occupancy_rate(),
        total_revenue=service.get_total_revenue(),
    )

@router.get("/history")
def get_history():

    records = service.get_parking_history()

    return [
        {
            "vehicle_number": record.vehicle_number,
            "vehicle_type": record.vehicle_type.value,
            "slot_id": record.slot_id,
            "entry_time": record.entry_time.isoformat(),
            "exit_time": (
                record.exit_time.isoformat()
                if record.exit_time
                else None
            ),
            "fee": record.fee,
        }
        for record in records
    ]