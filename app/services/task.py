from fastapi import HTTPException

from app.repositories.task import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate, TaskListResponse, TaskResponse
from app.models.task import Task

from app.cache.client import cache
from app.cache.keys import CacheKey

class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def get_task(self, user_id: str, task_id: str) -> Task:
        cache_key = CacheKey.single_task(task_id=task_id)
        cached = await cache.get(cache_key)
        if cached:
            if cached.get("user_id") != user_id:
                raise HTTPException(status_code=403, detail="You are not authoried to view this task")
            return cached
        
        task = await self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        if task.user_id != user_id:
            raise HTTPException(status_code=403, detail="Not authorised to edit this task")
        
        await cache.set(cache_key, task.__dict__ | {"owner": {"id": task.owner.id, "username": task.owner.username}})
        return task

    async def create_task(self, task_in: TaskCreate, user_id: str) -> Task:
        task = await self.repo.create(task_in, user_id)

        await cache.delete(CacheKey.user_tasks(user_id=user_id))

        return task
    
    async def get_user_tasks(self, user_id: str) -> TaskListResponse:
        cache_key = CacheKey.user_tasks(user_id=user_id)
        cached = await cache.get(cache_key)
        if cached:
            return TaskListResponse(**cached)

        tasks = await self.repo.get_by_user(user_id)

        await cache.set(cache_key, tasks.model_dump())
        return tasks
    
    async def update_task(self, task_id: str, user_id: str, task_in: TaskUpdate) -> Task:
        await self.get_task(task_id=task_id, user_id=user_id)
        task = await self.repo.update(task_id=task_id, task_in=task_in)
        if not task:
            raise HTTPException(status_code=404, detail="Task not found")
        
        await cache.get(CacheKey.single_task(task_id=task_id))
        await cache.get(CacheKey.user_tasks(user_id=user_id))
        return task
    
    async def delete_task(self, task_id: str, user_id: str) -> dict:
        await self.get_task(user_id=user_id, task_id=task_id)
        deleted = await self.repo.delete(task_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Task not found")
        
        await cache.get(CacheKey.single_task(task_id=task_id))
        await cache.get(CacheKey.user_tasks(user_id=user_id))
        return {"message": "Task deleted successfully"}