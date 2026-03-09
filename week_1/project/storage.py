import heapq
import json
import aiofiles
from typing import Dict, List
from models import TaskModel
from repository import TaskRepository


class InMemoryTaskRepository(TaskRepository):
    def __init__(self):
        self.tasks: Dict[str, TaskModel] = {}
        self.priority_queue = []               # heap of (priority, id)
        self.categories: Dict[str, List[str]] = {}
        self.tags: Dict[str, List[str]] = {}

    async def add_task(self, task: TaskModel) -> None:
        self.tasks[task.id] = task
        heapq.heappush(self.priority_queue, (task.priority, task.id))

        if task.category not in self.categories:
            self.categories[task.category] = []
        self.categories[task.category].append(task.id)

        for tag in task.tags:
            if tag not in self.tags:
                self.tags[tag] = []
            self.tags[tag].append(task.id)

    async def get_task(self, task_id: str) -> TaskModel:
        return self.tasks[task_id]

    async def list_tasks(self) -> List[TaskModel]:
        ordered_tasks = []
        temp_queue = self.priority_queue.copy()
        while temp_queue:
            _, task_id = heapq.heappop(temp_queue)
            # skip entries for tasks that have been deleted
            if task_id in self.tasks:
                ordered_tasks.append(self.tasks[task_id])
        return ordered_tasks

    async def delete_task(self, task_id: str) -> None:
        task = self.tasks.pop(task_id)
        self.categories[task.category].remove(task_id)
        for tag in task.tags:
            if tag in self.tags and task_id in self.tags[tag]:
                self.tags[tag].remove(task_id)

        # remove any remaining references from the heap and re‑heapify
        self.priority_queue = [
            (p, tid) for (p, tid) in self.priority_queue if tid != task_id
        ]
        heapq.heapify(self.priority_queue)

    async def save_to_file(self, filename: str):
        async with aiofiles.open(filename, "w") as f:
            data = [task.model_dump() for task in self.tasks.values()]
            await f.write(json.dumps(data))

    async def load_from_file(self, filename: str):
        try:
            async with aiofiles.open(filename, "r") as f:
                content = await f.read()
                tasks = json.loads(content)
                for t in tasks:
                    await self.add_task(TaskModel(**t))
        except (FileNotFoundError, json.JSONDecodeError):
            # nothing to load or file corrupted
            pass