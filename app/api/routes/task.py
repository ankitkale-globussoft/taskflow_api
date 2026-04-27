from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.api.deps import get_current_user
from app.repositories.task import TaskRepository
from app.services.task import TaskService
from app.schemas.task import TaskCreate, TaskResponse, TaskListResponse, TaskUpdate

from app.cache.limiter import limiter
from fastapi import Request

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/create", response_model=TaskResponse)
@limiter.limit("30/minute")
async def create_task(request: Request, task_in: TaskCreate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    repo=TaskRepository(db)
    service=TaskService(repo)
    task = await service.create_task(task_in, current_user.id)
    return task
    
@router.get("/list", response_model=TaskListResponse)
@limiter.limit("60/minute")
async def get_tasks(request: Request, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    repo=TaskRepository(db)
    service=TaskService(repo)
    task_list = await service.get_user_tasks(current_user.id)
    return task_list

@router.get("/{task_id}", response_model=TaskResponse)
@limiter.limit("60/minute")
async def get_task(request: Request, task_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    repo = TaskRepository(db)
    service = TaskService(repo)
    return await service.get_task(user_id=current_user.id, task_id=task_id)

@router.patch("/{task_id}", response_model=TaskResponse)
@limiter.limit("30/minute")
async def update_task(request: Request, task_id: str, task_in: TaskUpdate, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    repo = TaskRepository(db)
    service = TaskService(repo)
    return await service.update_task(task_id=task_id, user_id=current_user.id, task_in=task_in)

@router.delete("/{task_id}")
@limiter.limit("30/minute")
async def delete_task(request: Request, task_id: str, db: AsyncSession = Depends(get_db), current_user=Depends(get_current_user)):
    repo = TaskRepository(db)
    service = TaskService(repo)
    return await service.delete_task(task_id, current_user.id)