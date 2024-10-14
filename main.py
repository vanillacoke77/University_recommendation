from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def read_root():
    return {"Hello": "World"}

@app.get("/recommendation")
def recommendation():
    return {"Recommendation": "Hello"}