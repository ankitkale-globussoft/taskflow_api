from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.cache.client import cache
from app.api.routes import router as api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache.connect()
    print("✅ Redis connected")

    yield

    await cache.disconnect()
    print("🔴 Redis disconnected")

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan, debug=settings.DEBUG)
app.include_router(api_router)