from pydantic import BaseModel
from models.mushroom import Mushroom

class Basket(BaseModel):
    id: int
    owner: str
    capacity: int
    mushrooms: list[Mushroom] = []
