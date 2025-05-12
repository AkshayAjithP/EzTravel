from fastapi import APIRouter, Depends, HTTPException, status
from models.base import City, CityBase
from utils.auth import get_current_user, get_admin_user
from utils.database import create_city, get_city, get_all_cities
from typing import List

router = APIRouter()

@router.post("/", response_model=City)
async def create_new_city(
    city: CityBase,
    current_user: dict = Depends(get_admin_user)
):
    city_data = city.dict()
    city_data["created_by"] = current_user.id
    city_id = await create_city(city_data)
    return await get_city(city_id)

@router.get("/", response_model=List[City])
async def list_cities():
    return await get_all_cities()

@router.get("/{city_id}", response_model=City)
async def get_city_details(city_id: str):
    city = await get_city(city_id)
    if not city:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="City not found"
        )
    return city 