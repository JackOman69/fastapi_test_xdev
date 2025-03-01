import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from routes.mushrooms import router as MushroomsRoute
from routes.baskets import router as BasketsRoute
from core.db import postgres_db

FILE_STORAGE_DIR = os.environ["FILE_STORAGE_DIR"]

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.isdir(FILE_STORAGE_DIR):
        os.mkdir(FILE_STORAGE_DIR)

    await postgres_db.get_pool()

    yield
    
    await postgres_db.close_pool()
    
    
app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(MushroomsRoute, tags=["Mushrooms"])
app.include_router(BasketsRoute, tags=["Baskets"])