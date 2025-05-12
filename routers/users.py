from fastapi import APIRouter, Depends, HTTPException, status
from models.base import User
from utils.auth import get_current_user, get_admin_user
from utils.database import get_user
from typing import List

router = APIRouter()

@router.get("/me", response_model=User)
async def get_current_user_info(current_user: dict = Depends(get_current_user)):
    return current_user

@router.get("/{user_id}", response_model=User)
async def get_user_info(
    user_id: str,
    current_user: dict = Depends(get_admin_user)
):
    user = await get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user 