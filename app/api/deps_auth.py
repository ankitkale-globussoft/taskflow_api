from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

async def get_current_user():
    # jwt logic here
    return {"id": "thisis-user-id"}