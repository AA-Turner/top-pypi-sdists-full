from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Simple Pet Store API")


# Pet model
class Pet(BaseModel):
    id: int
    name: str
    type: str


# In-memory pet storage
pets_db: List[Pet] = [Pet(id=24, name="Happy Fox", type="dog"), Pet(id=24, name="Sad Cow", type="cow")]


# Get all pets
@app.get("/pets", response_model=List[Pet])
def get_pets():
    return pets_db


# Get a pet by ID
@app.get("/pets/{pet_id}", response_model=Pet)
def get_pet(pet_id: int):
    for pet in pets_db:
        if pet.id == pet_id:
            return pet
    raise HTTPException(status_code=404, detail="Pet not found")


# Add a new pet
@app.post("/pets", response_model=Pet)
def add_pet(pet: Pet):
    if any(p.id == pet.id for p in pets_db):
        raise HTTPException(status_code=400, detail="Pet with this ID already exists")
    pets_db.append(pet)
    return pet
