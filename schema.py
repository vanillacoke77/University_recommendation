from pydantic import BaseModel

class User(BaseModel):
    name: str
    email: str
    phoneno: str
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