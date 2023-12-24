from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import app.services.task as task_service
import app.database as db

import app.schemas.task as task_schema


router = APIRouter()


@router.get("", response_model=list[task_schema.Task])
async def list_tasks(session: AsyncSession = Depends(db.get_session)):
    """ List all tasks. """
    return await task_service.get_tasks(session)


@router.post("", response_model=task_schema.TaskCreateResponse)
async def create_task(task_body: task_schema.TaskCreate, session: AsyncSession = Depends(db.get_session)):
    """ Create a new task. """
    return await task_service.create_task(session, task_body)


@router.put("/{task_id}", response_model=task_schema.TaskCreateResponse)
async def update_task(task_id: int, task_body: task_schema.TaskCreate, session: AsyncSession = Depends(db.get_session)):
    """ Update an existing task. """
    task = await task_service.get_task(session, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    return await task_service.update_task(session, task_body, original=task)


@router.delete("/{task_id}", response_model=None)
async def delete_task(task_id: int, session: AsyncSession = Depends(db.get_session)):
    """ Delete an existing task. """
    task = await task_service.get_task(session, task_id=task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    await task_service.delete_task(session, original=task)
    return None
