from pydantic import BaseModel


class TaskCreate(BaseModel):
    description: str
    params: dict


class TaskResponse(BaseModel):
    task_sid: int
    task_uuid: str
    description: str
    params: dict


class TaskUpdate(BaseModel):
    description: str
    params: dict
