import pytest
import asyncio
from models import TaskModel, Priority
from storage import InMemoryTaskRepository
from service import TaskService


@pytest.mark.asyncio
async def test_add_task():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    task = TaskModel(
        title="Test",
        description="Test desc",
        priority=Priority.HIGH,
        category="Work"
    )

    await service.create_task(task)
    tasks = await service.list_tasks()

    assert len(tasks) == 1


@pytest.mark.asyncio
async def test_delete_task():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    task = TaskModel(
        title="Test",
        description="Test desc",
        priority=Priority.HIGH,
        category="Work"
    )

    await service.create_task(task)
    await service.delete_task(task.id)

    tasks = await service.list_tasks()
    assert len(tasks) == 0


@pytest.mark.asyncio
async def test_list_tasks_priority_order():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    task1 = TaskModel(title="Low", description="", priority=Priority.LOW, category="Work")
    task2 = TaskModel(title="High", description="", priority=Priority.HIGH, category="Work")

    await service.create_task(task1)
    await service.create_task(task2)

    tasks = await service.list_tasks()
    assert tasks[0].priority == Priority.HIGH  # Highest priority first
    assert tasks[1].priority == Priority.LOW

@pytest.mark.asyncio
async def test_categories_tracking():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    task = TaskModel(title="Test", description="", priority=Priority.HIGH, category="Work")
    await service.create_task(task)

    assert "Work" in repo.categories
    assert task.id in repo.categories["Work"]

@pytest.mark.asyncio
async def test_tags_tracking():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    task = TaskModel(title="Test", description="", priority=Priority.HIGH, category="Work", tags={"urgent", "personal"})
    await service.create_task(task)

    assert "urgent" in repo.tags
    assert task.id in repo.tags["urgent"]

@pytest.mark.asyncio
async def test_save_and_load_file():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    task = TaskModel(title="Test", description="", priority=Priority.HIGH, category="Work")
    await service.create_task(task)

    await repo.save_to_file("test_tasks.json")
    new_repo = InMemoryTaskRepository()
    await new_repo.load_from_file("test_tasks.json")

    tasks = await new_repo.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "Test"