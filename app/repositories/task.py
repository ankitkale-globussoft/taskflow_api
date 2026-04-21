from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.task import Task
from app.schemas.task import TaskCreate

class TaskRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, task_in: TaskCreate, user_id: str) -> Task:
        task = Task(**task_in.model_dump(), user_id=user_id)
        self.db.add(task)
        self.db.commit()
        await self.db.refresh(Task)
        return task