from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: str
    role: str = "user"

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: str
    created_at: datetime
    is_admin: bool = False

class CityBase(BaseModel):
    name: str
    country: str
    description: Optional[str] = None

class City(CityBase):
    id: str
    created_at: datetime
    created_by: str

class PlaceBase(BaseModel):
    name: str
    description: str
    city_id: str
    image_urls: List[str] = []
    room_rates: dict = {
        "low": 0,
        "medium": 0,
        "high": 0
    }

class Place(PlaceBase):
    id: str
    created_at: datetime
    created_by: str

class VisitedPlace(BaseModel):
    user_id: str
    place_id: str
    visited_at: datetime 