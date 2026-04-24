from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.deps import get_current_user

from app.api.deps import get_db
from app.services.auth import AuthService
from app.schemas.user import UserRegister, UserUpdate, Token, UserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.register(user_in)

@router.post("/login", response_model=Token)
async def login(user_in: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    service = AuthService(db)
    return await service.login(user_in)

@router.get("/me", response_model=UserResponse)
async def me(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    service = AuthService(db)
    return await service.get_user(current_user.id)

@router.patch("/{user_id}", response_model=UserResponse)
async def update_user(user_in: UserUpdate, db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    service = AuthService(db)
    return await service.update_user(current_user.id, user_in)

@router.delete("/{user_id")
async def delete_user(db: AsyncSession = Depends(get_db), current_user = Depends(get_current_user)):
    service = AuthService(db)
    return await service.delete_user(current_user.id)