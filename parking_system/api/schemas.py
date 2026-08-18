from typing import Optional

from pydantic import BaseModel

from parking_system.models.enums import VehicleType


class ParkVehicleRequest(BaseModel):
    registration_number: str
    vehicle_type: VehicleType


class ParkVehicleResponse(BaseModel):
    success: bool
    message: str
    slot_id: Optional[int]


class ExitVehicleRequest(BaseModel):
    registration_number: str


class ExitVehicleResponse(BaseModel):
    success: bool
    message: str
    fee: Optional[float]


class VehicleResponse(BaseModel):
    registration_number: str
    vehicle_type: str
    slot_id: int
    entry_time: str


class SlotResponse(BaseModel):
    slot_id: int
    slot_type: str
    occupied: bool


class DashboardResponse(BaseModel):
    total_slots: int
    occupied_slots: int
    available_slots: int
    occupancy_rate: float
    total_revenue: float