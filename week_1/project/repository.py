from abc import ABC, abstractmethod
from typing import List
from models import TaskModel


class TaskRepository(ABC):

    @abstractmethod
    async def add_task(self, task: TaskModel) -> None:
        pass

    @abstractmethod
    async def get_task(self, task_id: str) -> TaskModel:
        pass

    @abstractmethod
    async def list_tasks(self) -> List[TaskModel]:
        pass

    @abstractmethod
    async def delete_task(self, task_id: str) -> None:
        pass