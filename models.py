from dataclasses import dataclass
from decimal import Decimal


@dataclass
class Building:
    id: int | None
    address: str
    city: str
    floors: int


@dataclass
class Owner:
    id: int | None
    full_name: str
    phone: str
    email: str


@dataclass
class Apartment:
    id: int | None
    apartment_number: int
    rooms: int
    area: Decimal
    price: Decimal
    building_id: int
    owner_id: int
    