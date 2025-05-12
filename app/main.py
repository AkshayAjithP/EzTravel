from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from firebase_admin import credentials, initialize_app
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Firebase Admin
cred = credentials.Certificate("firebase-credentials.json")
firebase_app = initialize_app(cred)

app = FastAPI(
    title="Trip Planner API",
    description="A FastAPI backend for trip planning application",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Import and include routers
from routers import auth, cities, places, users

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(cities.router, prefix="/cities", tags=["Cities"])
app.include_router(places.router, prefix="/places", tags=["Places"])
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/")
async def root():
    return {"message": "Welcome to Trip Planner API"} 