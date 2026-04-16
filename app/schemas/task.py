from pydantic import BaseModel, field_validator, ConfigDict
from app.models.task import TaskStatus, TaskPriority
from app.schemas.user import UserSummary


class TaskCreate(BaseModel):
    title: str
    description: str
    status: TaskStatus = TaskStatus.TODO
    priority: TaskPriority = TaskPriority.MEDIUM

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("Title must be atleast 3 characters")
        if len(v) > 200:
            raise ValueError("Title cannot exceed 200 characters")
        return v
    
    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str) -> str:
        if v is None:
            return None
        v = v.strip()
        if not v:
            return None
        if len(v) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")
        
        return v
    

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    is_completed: bool | None = None

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str | None) -> str | None:
        if v is not None:
            v = v.strip()
            if len(v) < 3:
                raise ValueError("Title must be atleast 3 characters")
            if len(v) > 200:
                raise ValueError("Description cannot exceed 1000 characters")
        return v
    

class TaskStatusUpdate(BaseModel):
    status: TaskStatus


class TaskResponse(BaseModel):
    id: str
    title: str
    description: str | None
    status: TaskStatus
    priority: TaskPriority
    is_completed: bool
    user_id: str
    owner: UserSummary

    model_config = ConfigDict(from_attributes=True)


class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int