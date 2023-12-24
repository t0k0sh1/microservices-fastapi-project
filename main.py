"""Main module for the API."""

import os
from fastapi import FastAPI

from app.api.v1.hello import router as hello_router
from app.api.v1.task import router as task_router

ENV = os.getenv("ENVIRONMENT", "development")

if ENV == "production":
    app = FastAPI(docs_url=None, redoc_url=None)
else:
    app = FastAPI()

app.include_router(hello_router, prefix="/api/v1/hello")
app.include_router(task_router, prefix="/api/v1/tasks")
