from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.task.schemas import *
from src.task.models import *

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/tasks/add/", response_model=TaskResponse)
async def add_task(task: TaskCreate, db: Session = Depends(get_db)):
    try:
        new_task = Task(**task.dict())
        db.add(new_task)
        db.flush()
        db.commit()
        return {
            "task_sid": new_task.task_sid,
            "task_uuid": str(new_task.task_uuid),
            "description": new_task.description,
            "params": dict(new_task.params)
        }
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/tasks/", response_model=List[TaskResponse])
async def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [{
        "task_sid": str(task.task_sid),
        "task_uuid": str(task.task_uuid),
        "description": str(task.description),
        "params": dict(task.params),
    } for task in tasks]


@app.put("/tasks/{task_sid}", response_model=TaskUpdate)
async def update_task(task_sid: str, updated_task: TaskCreate, db: Session = Depends(get_db)):
    existing_task = db.query(Task).filter(Task.task_sid == task_sid).first()

    if existing_task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    for key, value in updated_task.dict().items():
        setattr(existing_task, key, value)

    db.commit()
    db.refresh(existing_task)
    return {
        "description": str(existing_task.description),
        "params": dict(existing_task.params)
    }
