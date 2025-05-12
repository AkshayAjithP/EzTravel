from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from models.base import Place, PlaceBase
from utils.auth import get_current_user, get_admin_user
from utils.database import (
    create_place,
    get_place,
    get_places_by_city,
    mark_place_visited,
    get_visited_places
)
from typing import List
import aiofiles
import os
from datetime import datetime

router = APIRouter()

@router.post("/", response_model=Place)
async def create_new_place(
    place: PlaceBase,
    current_user: dict = Depends(get_admin_user)
):
    place_data = place.dict()
    place_data["created_by"] = current_user.id
    place_id = await create_place(place_data)
    return await get_place(place_id)

@router.get("/city/{city_id}", response_model=List[Place])
async def list_places_by_city(city_id: str):
    return await get_places_by_city(city_id)

@router.get("/{place_id}", response_model=Place)
async def get_place_details(place_id: str):
    place = await get_place(place_id)
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    return place

@router.post("/{place_id}/visit")
async def mark_as_visited(
    place_id: str,
    current_user: dict = Depends(get_current_user)
):
    await mark_place_visited(current_user.id, place_id)
    return {"message": "Place marked as visited"}

@router.get("/visited", response_model=List[dict])
async def get_user_visited_places(
    current_user: dict = Depends(get_current_user)
):
    return await get_visited_places(current_user.id)

@router.post("/{place_id}/upload-image")
async def upload_place_image(
    place_id: str,
    image: UploadFile = File(...),
    current_user: dict = Depends(get_admin_user)
):
    # Create uploads directory if it doesn't exist
    os.makedirs("uploads", exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{place_id}_{timestamp}_{image.filename}"
    filepath = os.path.join("uploads", filename)
    
    # Save the file
    async with aiofiles.open(filepath, 'wb') as out_file:
        content = await image.read()
        await out_file.write(content)
    
    # Update place with new image URL
    place = await get_place(place_id)
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Place not found"
        )
    
    place["image_urls"].append(f"/uploads/{filename}")
    await create_place(place)
    
    return {"message": "Image uploaded successfully", "url": f"/uploads/{filename}"} 