from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from .enums import VehicleType


@dataclass
class ParkingRecord:
    vehicle_number: str
    vehicle_type: VehicleType
    slot_id: int
    entry_time: datetime
    exit_time: Optional[datetime] = None
    fee: Optional[float] = None
