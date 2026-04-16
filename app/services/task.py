from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, task_in: TaskCreate, user_id: str) -> Task:
        return await self.repo.create(task_in, user_id)