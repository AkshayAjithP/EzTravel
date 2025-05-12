from fastapi import APIRouter, HTTPException, status
from firebase_admin import auth
from models.base import UserCreate, User
from utils.database import create_user, is_first_user
from datetime import datetime

router = APIRouter()

@router.post("/register", response_model=User)
async def register(user_data: UserCreate):
    try:
        # Create user in Firebase Auth
        user = auth.create_user(
            email=user_data.email,
            password=user_data.password
        )
        
        # Check if this is the first user
        is_first = await is_first_user()
        
        # Create user in Firestore
        user_dict = {
            "id": user.uid,
            "email": user_data.email,
            "role": "admin" if is_first else "user",
            "is_admin": is_first,
            "created_at": datetime.now()
        }
        
        await create_user(user_dict)
        
        return User(**user_dict)
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        ) 