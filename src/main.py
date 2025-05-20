from fastapi import FastAPI
from src.endpoints.endpoints import router as rooms_router

app = FastAPI()

app.include_router(rooms_router)