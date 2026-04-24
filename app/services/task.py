from fastapi import HTTPException

from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskListResponse, TaskResponse
from app.models.task import Task

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def get_task(self, user_id: str, task_id: str) -> Task:
        task = await self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorised to edit this task")
        return task

    async def create_task(self, task_in: TaskCreate, user_id: str) -> Task:
        return await self.repo.create(task_in, user_id)
    
    async def get_user_tasks(self, user_id: str) -> TaskListResponse:
        tasks = await self.repo.get_by_user(user_id)
        return tasks
    
    async def update_task(self, task_id: str, user_id: str, task_in: TaskUpdate) -> Task:
        await self.get_task(task_id=task_id, user_id=user_id)
        task = await self.repo.update(task_id=task_id, task_in=task_in)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    
    async def delete_task(self, task_id: str, user_id: str) -> dict:
        await self.get_task(user_id=user_id, task_id=task_id)
        deleted = await self.repo.delete(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        return {"message": "Task deleted successfully"}