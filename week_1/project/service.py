from typing import List
from models import TaskModel
from repository import TaskRepository


class TaskService:

    def __init__(self, repository: TaskRepository):
        self.repository = repository  # composition

    async def create_task(self, task: TaskModel):
        await self.repository.add_task(task)

    async def list_tasks(self) -> List[TaskModel]:
        return await self.repository.list_tasks()

    async def delete_task(self, task_id: str):
        await self.repository.delete_task(task_id)