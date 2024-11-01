from fastapi import FastAPI
from schema import UserPreference
from recommendation import get_recommendation

app = FastAPI()

@app.get("/ping")
def read_root():
    return {"Hello": "World"}

@app.post("/recommendation")
def recommendation(user_preference:UserPreference):
    return {"recommendation": get_recommendation(user_preference)}