from enum import Enum as Enums
from sqlalchemy import (
    String,
    Integer,
    Column,
    ForeignKey,
    DateTime,
    Enum,
)
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime

Base = declarative_base()

class Status(Enums):
    PENDING = 'PENDING'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'

    def __str__(self):
        return self.value


class AppUser(Base):
    __tablename__ = "appuser"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(128), nullable=False)

    tasks = relationship(
        "Task",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan"
    )


class Task(Base):
    __tablename__ = "task"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(100), nullable=False)
    description = Column(String(256))
    status = Column(Enum(Status), default=Status.PENDING, nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    user_id = Column(Integer, ForeignKey('appuser.id', ondelete='CASCADE'), nullable=False)
