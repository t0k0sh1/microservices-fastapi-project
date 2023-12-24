from typing import Tuple, Any, Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select, lambda_stmt, Row
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

import app.models.task as task_model
import app.schemas.task as task_schema


async def create_task(session: AsyncSession, task_create: task_schema.TaskCreate) -> task_model.Task:
    task = task_model.Task(**task_create.model_dump())
    session.add(task)
    await session.commit()
    await session.refresh(task)
    return task


async def get_tasks(session: AsyncSession) -> Sequence[Row[tuple[Any, ...] | Any]]:
    result: Result = await session.execute(
        select(
            task_model.Task.id,
            task_model.Task.title,
            task_model.Task.description,
        )
    )

    return result.all()


async def get_task(session: AsyncSession, task_id: int) -> task_model.Task:
    stmt = lambda_stmt(lambda: select(task_model.Task).where(task_model.Task.id == task_id))
    result = await session.execute(stmt)
    return result.scalars().first()


async def update_task(session: AsyncSession, task_create: task_schema.TaskCreate, original: task_model.Task) -> task_model.Task:
    original.title = task_create.title
    session.add(original)
    await session.commit()
    await session.refresh(original)
    return original


async def delete_task(db: AsyncSession, original: task_model.Task) -> None:
    await db.delete(original)
    await db.commit()
