from pydantic import BaseModel, Field, field_validator,validator
from typing import Set
from uuid import uuid4
from enum import Enum


class Priority(int, Enum):
    LOW = 3
    MEDIUM = 2
    HIGH = 1


class TaskModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str = Field(..., min_length=3)
    description: str
    priority: Priority
    category: str
    tags: Set[str] = set()
    completed: bool = False

    # @validator("category")
    @field_validator("category")
    def category_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Category cannot be empty")
        return v