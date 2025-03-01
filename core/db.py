import os
from asyncpg import create_pool

class PostgresDB:
    _pool = None

    @classmethod
    async def get_pool(cls):
        if cls._pool is None:
            cls._pool = await create_pool(
                user=os.environ["POSTGRES_USER"],
                password=os.environ["POSTGRES_PASSWORD"],
                database=os.environ["POSTGRES_NAME"],
                host=os.environ["POSTGRES_HOST"],
                port=os.environ["POSTGRES_PORT"]
            )
        return cls._pool
    
    @classmethod
    async def close_pool(cls):
        if cls._pool:
            await cls._pool.close()
            cls._pool = None
            
postgres_db = PostgresDB()