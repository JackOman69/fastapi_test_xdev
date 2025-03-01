from pydantic import BaseModel

class Mushroom(BaseModel):
    id: int
    name: str
    edibility: bool
    weight: float
    freshness: int

class MushroomUpdate(BaseModel):
    name: str
    edibility: bool
    weight: float
    freshness: int
