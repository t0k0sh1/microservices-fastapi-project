from pydantic import BaseModel, ConfigDict, Field


class TaskBase(BaseModel):
    title: str | None = Field(None, json_schema_extra={"example": "Buy groceries", "description": "The title of the "
                                                                                                  "task"})
    description: str | None = Field(None, json_schema_extra={"example": "Buy milk, eggs, cheese, and bread.",
                                                             "description": "The description of the task"})


class TaskCreate(TaskBase):
    pass


class TaskCreateResponse(TaskCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Task(TaskBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
