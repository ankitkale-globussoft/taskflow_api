from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.api.deps import get_current_user
from app.repositories.task import TaskRepository
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/create", response_model=TaskResponse)
async def create_task(task_in: TaskCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    repo=TaskRepository(db)
    service=TaskService(repo)
    task = await service.create_task(task_in, current_user.id)
    return task