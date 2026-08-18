from dataclasses import dataclass

from .enums import VehicleType


@dataclass
class ParkingSlot:
    slot_id: int
    slot_type: VehicleType
    occupied: bool = False
