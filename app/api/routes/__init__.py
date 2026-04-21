from fastapi import APIRouter
from app.api.routes import auth, task

router = APIRouter()

@router.get('/')
def health():
    return {"detail": "the api is running good"}

router.include_router(auth.router)
router.include_router(task.router)