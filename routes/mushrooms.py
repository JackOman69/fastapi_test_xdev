from fastapi import APIRouter, HTTPException
from models.mushroom import Mushroom, MushroomUpdate
from core.db import postgres_db

router = APIRouter()

# POST Создать гриб
@router.post("/mushrooms/", response_model=Mushroom)
async def create_mushroom(mushroom: Mushroom):
    pool = await postgres_db.get_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO mushrooms (id, name, edibility, weight, freshness) VALUES ($1, $2, $3, $4, $5)",
            mushroom.id, mushroom.name, mushroom.edibility, mushroom.weight, mushroom.freshness
        )
    return mushroom

# PUT Обновить информацию о грибе
@router.put("/mushrooms/{mushroom_id}", response_model=Mushroom)
async def update_mushroom(mushroom_id: int, mushroom: MushroomUpdate):
    # The ID is not included in the update model, so we don't need to check it
    pool = await postgres_db.get_pool()
    async with pool.acquire() as connection:
        result = await connection.execute(
            "UPDATE mushrooms SET name=$1, edibility=$2, weight=$3, freshness=$4 WHERE id=$5",
            mushroom.name, mushroom.edibility, mushroom.weight, mushroom.freshness, mushroom_id
        )
        if result == "UPDATE 0":
            raise HTTPException(status_code=404, detail="Mushroom not found")
    return Mushroom(id=mushroom_id, **mushroom.model_dump())

# GET Получить конкретный гриб (по id)
@router.get("/mushrooms/{mushroom_id}", response_model=Mushroom)
async def get_mushroom(mushroom_id: int):
    pool = await postgres_db.get_pool()
    async with pool.acquire() as connection:
        mushroom = await connection.fetchrow(
            "SELECT * FROM mushrooms WHERE id=$1", mushroom_id
        )
        if mushroom is None:
            raise HTTPException(status_code=404, detail="Mushroom not found")
    return Mushroom(**mushroom)

