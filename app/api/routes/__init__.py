from fastapi import APIRouter, Request
from app.api.routes import auth, task

from app.cache.limiter import limiter

router = APIRouter()

@router.get('/')
@limiter.limit("5/minute")
def health(request: Request):
    return {"detail": "the api is running good"}

router.include_router(auth.router)
router.include_router(task.router)