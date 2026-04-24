from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.auth import UserRepository
from app.models.user import User
from app.schemas.user import UserRegister, UserUpdate, Token
from app.core.secqurity import hash_password, verify_password, create_access_token

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db
        self.repo = UserRepository(db)
    
    async def register(self, user_in: UserRegister) -> User:
        existing = await self.repo.get_by_username(user_in.username)
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")

        user = User(
            email = user_in.email,
            username = user_in.username,
            hashed_password = hash_password(user_in.password)
        )

        await self.repo.create(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user
    
    async def login(self, user_in: OAuth2PasswordRequestForm):
        user = await self.repo.get_by_username(user_in.username)

        if not user:
            raise HTTPException(status_code=400, detail="Invalid Credentials")

        if not verify_password(user_in.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Invalid Credentials")

        token = create_access_token({"sub": user.id})

        return Token(access_token=token)
    
    async def get_user(self, user_id: str) -> User | None:
        user = await self.repo.get_user_by_id(user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def update_user(self, user_id: str, user_in: UserUpdate) -> User:
        await self.get_user(user_id)
        user = await self.repo.update(user_id, user_in)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    
    async def delete_user(self, user_id: str) -> dict:
        await self.get_user(user_id)
        deleted = await self.repo.delete(user_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="User not found")
        return{"message": "Account Deleted successfully"}