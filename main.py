from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.config import settings
from app.cache.client import cache
from app.api.routes import router as api_router

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from app.cache.limiter import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    await cache.connect()
    print("✅ Redis connected")

    yield

    await cache.disconnect()
    print("🔴 Redis disconnected")

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan, debug=settings.DEBUG)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(api_router)