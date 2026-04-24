from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskListResponse

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task_in: TaskCreate, user_id: str) -> Task:
        task = Task(**task_in.model_dump(), user_id=user_id)
        self.db.add(task)

        await self.db.commit()
        await self.db.refresh(task)
        
        return task
    
    async def get_by_user(self, user_id: str) -> TaskListResponse:
        result = await self.db.execute(select(Task).options(selectinload(Task.owner)).where(Task.user_id == user_id))
        tasks = result.scalars().all()
        length = len(tasks)
        return TaskListResponse(
            tasks=tasks,
            total=length
        )
    
    async def get_by_id(self, task_id: str) -> Task | None:
        result = await self.db.execute(select(Task).options(selectinload(Task.owner)).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def update(self, task_id: str, task_in: TaskUpdate) -> Task | None:
        task = await self.get_by_id(task_id)
        if not task:
            return None
        update_data = task_in.model_dump(exclude_unset=True)
        for feild, value in update_data.items():
            setattr(task, feild, value)
        
        await self.db.commit()
        await self.db.refresh(task)
        return task
    
    async def delete(self, task_id: str) -> bool:
        task = await self.get_by_id(task_id)
        if not task:
            return False
        
        await self.db.delete(task)
        await self.db.commit()
        return True