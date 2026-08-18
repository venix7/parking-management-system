from dataclasses import dataclass
from datetime import datetime

from .enums import VehicleType


@dataclass
class Vehicle:
    number: str
    vehicle_type: VehicleType
    entry_time: datetime
