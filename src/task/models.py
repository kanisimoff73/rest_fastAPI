from sqlalchemy import Column, String, JSON, Integer, Sequence
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
import uuid
from src.database import Base


class Task(Base):
    __tablename__ = "task"

    task_sid = Column(
        Integer,
        Sequence('task_sid_seq'),
        unique=True,
        index=True,
        nullable=False
    )
    task_uuid = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        server_default=text("gen_random_uuid()")
    )
    description = Column(String, index=True)
    params = Column(JSON)
