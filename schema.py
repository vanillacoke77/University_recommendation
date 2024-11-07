from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    name: str
    email: Optional[str] = None  # Make email optional
    phoneno: Optional[str] = None
    password: str

class UserPreference(BaseModel):
    country: str
    fees: int
    stream: str
    rank: str

class Recommendation(BaseModel):
    name: str
    country: str
    rank: str
    stream: str
    course: str
    fees: int