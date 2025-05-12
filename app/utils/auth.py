from firebase_admin import auth
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from models.base import User

security = HTTPBearer()

async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    try:
        # Verify the Firebase ID token
        decoded_token = auth.verify_id_token(credentials.credentials)
        
        # Get user from Firestore
        user = User(
            id=decoded_token["uid"],
            email=decoded_token["email"],
            role="user",  # Default role
            created_at=decoded_token.get("created_at"),
            is_admin=False  # Default value
        )
        
        return user
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    return user 