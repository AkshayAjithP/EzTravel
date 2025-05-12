from firebase_admin import firestore
from datetime import datetime
from typing import Optional, List, Dict, Any

db = firestore.client()

# User operations
async def create_user(user_data: dict) -> str:
    user_ref = db.collection('users').document(user_data['id'])
    user_data['created_at'] = datetime.now()
    user_ref.set(user_data)
    return user_data['id']

async def get_user(user_id: str) -> Optional[dict]:
    user_ref = db.collection('users').document(user_id)
    user = user_ref.get()
    return user.to_dict() if user.exists else None

async def is_first_user() -> bool:
    users = db.collection('users').limit(1).get()
    return len(users) == 0

# City operations
async def create_city(city_data: dict) -> str:
    city_ref = db.collection('cities').document()
    city_data['id'] = city_ref.id
    city_data['created_at'] = datetime.now()
    city_ref.set(city_data)
    return city_ref.id

async def get_city(city_id: str) -> Optional[dict]:
    city_ref = db.collection('cities').document(city_id)
    city = city_ref.get()
    return city.to_dict() if city.exists else None

async def get_all_cities() -> List[dict]:
    cities = db.collection('cities').get()
    return [city.to_dict() for city in cities]

# Place operations
async def create_place(place_data: dict) -> str:
    place_ref = db.collection('places').document()
    place_data['id'] = place_ref.id
    place_data['created_at'] = datetime.now()
    place_ref.set(place_data)
    return place_ref.id

async def get_place(place_id: str) -> Optional[dict]:
    place_ref = db.collection('places').document(place_id)
    place = place_ref.get()
    return place.to_dict() if place.exists else None

async def get_places_by_city(city_id: str) -> List[dict]:
    places = db.collection('places').where('city_id', '==', city_id).get()
    return [place.to_dict() for place in places]

# Visited places operations
async def mark_place_visited(user_id: str, place_id: str) -> None:
    visited_ref = db.collection('visited_places').document()
    visited_ref.set({
        'user_id': user_id,
        'place_id': place_id,
        'visited_at': datetime.now()
    })

async def get_visited_places(user_id: str) -> List[dict]:
    visited = db.collection('visited_places').where('user_id', '==', user_id).get()
    return [doc.to_dict() for doc in visited] 