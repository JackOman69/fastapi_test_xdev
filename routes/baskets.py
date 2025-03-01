from fastapi import APIRouter, HTTPException
from models.mushroom import Mushroom
from models.basket import Basket
from core.db import postgres_db

router = APIRouter()

# POST Создать корзинку
@router.post("/baskets/", response_model=Basket)
async def create_basket(basket: Basket):
    pool = await postgres_db.get_pool()
    async with pool.acquire() as connection:
        await connection.execute(
            "INSERT INTO baskets (id, owner, capacity) VALUES ($1, $2, $3)",
            basket.id, basket.owner, basket.capacity
        )
    return basket

# POST Положить в корзинку гриб
@router.post("/baskets/{basket_id}/mushrooms/{mushroom_id}")
async def add_mushroom_to_basket(basket_id: int, mushroom_id: int):
    pool = await postgres_db.get_pool()
    async with pool.acquire() as connection:
        # Проверяем существование корзинки
        basket = await connection.fetchrow("SELECT * FROM baskets WHERE id=$1", basket_id)
        if basket is None:
            raise HTTPException(status_code=404, detail="Basket not found")
        
        # Проверяем существование гриба
        mushroom = await connection.fetchrow("SELECT * FROM mushrooms WHERE id=$1", mushroom_id)
        if mushroom is None:
            raise HTTPException(status_code=404, detail="Mushroom not found")
        
        # Проверяем текущее количество грибов в корзинке
        current_mushroom_count = await connection.fetchval(
            "SELECT COUNT(*) FROM basket_mushrooms WHERE basket_id=$1", basket_id
        )
        
        # Проверяем, не превышает ли добавление нового гриба вместимость корзинки
        if current_mushroom_count >= basket['capacity']:
            raise HTTPException(status_code=400, detail="Cannot add mushroom: basket capacity exceeded")
        
        # Добавляем гриб в корзинку
        await connection.execute(
            "INSERT INTO basket_mushrooms (basket_id, mushroom_id) VALUES ($1, $2)",
            basket_id, mushroom_id
        )
    return {"message": "Mushroom added to basket"}

# DELETE Удалить из корзинки гриб
@router.delete("/baskets/{basket_id}/mushrooms/{mushroom_id}")
async def remove_mushroom_from_basket(basket_id: int, mushroom_id: int):
    pool = await postgres_db.get_pool()
    async with pool.acquire() as connection:
        # Проверяем существование корзинки
        basket = await connection.fetchrow("SELECT * FROM baskets WHERE id=$1", basket_id)
        if basket is None:
            raise HTTPException(status_code=404, detail="Basket not found")
        
        # Удаляем гриб из корзинки
        await connection.execute(
            "DELETE FROM basket_mushrooms WHERE basket_id=$1 AND mushroom_id=$2",
            basket_id, mushroom_id
        )
    return {"message": "Mushroom removed from basket"}

# GET Получить конкретную корзинку (по id)
@router.get("/baskets/{basket_id}", response_model=Basket)
async def get_basket(basket_id: int):
    pool = await postgres_db.get_pool()
    async with pool.acquire() as connection:
        basket_record = await connection.fetchrow("SELECT * FROM baskets WHERE id=$1", basket_id)
        if basket_record is None:
            raise HTTPException(status_code=404, detail="Basket not found")
        
        # Получаем грибы в корзинке
        mushrooms = await connection.fetch(
            "SELECT * FROM mushrooms INNER JOIN basket_mushrooms ON mushrooms.id = basket_mushrooms.mushroom_id WHERE basket_mushrooms.basket_id=$1",
            basket_id
        )
        
        mushroom_list = [Mushroom(**mushroom) for mushroom in mushrooms]

        basket = Basket(
            id=basket_record['id'],
            owner=basket_record['owner'],
            capacity=basket_record['capacity'],
            mushrooms=mushroom_list
        )
        
    return basket