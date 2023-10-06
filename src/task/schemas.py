from pydantic import BaseModel


class TaskCreate(BaseModel):
    description: str
    params: dict


class TaskResponse(BaseModel):
    task_uuid: str
