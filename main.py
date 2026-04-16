from fastapi import FastAPI
from app.api.routes import task

app = FastAPI()

app.include_router(task.router)