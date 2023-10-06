from typing import List

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from src.database import SessionLocal
from src.task.schemas import *
from src.task.models import *

app = FastAPI()


@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}


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
        db.commit()
        db.refresh(new_task)
        return {"task_uuid": str(new_task.task_uuid)}
    except Exception as e:
        print(e)
        db.rollback()
        raise HTTPException(status_code=500, detail="Internal Server Error")


@app.get("/tasks/", response_model=List[TaskResponse])
async def get_all_tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return [{"task_uuid": str(task.task_uuid) for task in tasks}]
