# import asyncio
# from models import TaskModel, Priority
# from storage import InMemoryTaskRepository
# from service import TaskService


# async def main():
#     repo = InMemoryTaskRepository()
#     service = TaskService(repo)

#     while True:
#         command = input("Enter command (add/list/delete/exit): ")

#         if command == "add":
#             title = input("Title: ")
#             category = input("Category: ")
#             priority = Priority(int(input("Priority (1=High,2=Med,3=Low): ")))

#             task = TaskModel(
#                 title=title,
#                 description="",
#                 category=category,
#                 priority=priority
#             )

#             await service.create_task(task)

#         elif command == "list":
#             tasks = await service.list_tasks()
#             for t in tasks:
#                 print(t)

#         elif command == "exit":
#             break


# asyncio.run(main())



import asyncio
from models import TaskModel, Priority
from storage import InMemoryTaskRepository
from service import TaskService


async def main():
    repo = InMemoryTaskRepository()
    service = TaskService(repo)

    while True:
        command = input("Enter command (add/list/delete/save/load/exit): ")

        if command == "add":
            try:
                title = input("Title: ")
                category = input("Category: ")
                priority = Priority(int(input("Priority (1=High,2=Med,3=Low): ")))

                task = TaskModel(
                    title=title,
                    description="",
                    category=category,
                    priority=priority
                )

                await service.create_task(task)
                print("Task created successfully!\n")
            except (ValueError, KeyError) as e:
                print(f"Error creating task: {e}\n")

        elif command == "list":
            tasks = await service.list_tasks()
            if not tasks:
                print("No tasks found.\n")
            else:
                for i, t in enumerate(tasks):
                    print(f"[{i}] {t}")
                print()

        elif command == "delete":
            try:
                tasks = await service.list_tasks()
                if not tasks:
                    print("No tasks to delete.\n")
                else:
                    task_id = input("Enter task ID to delete: ")
                    await service.delete_task(task_id)
                    print("Task deleted successfully!\n")
            except (ValueError, IndexError) as e:
                print(f"Error deleting task: {e}\n")

        elif command == "save":
            filename = input("Enter filename to save (e.g., tasks.json): ")
            await repo.save_to_file(filename)
            print("Tasks saved successfully!\n")

        elif command == "load":
            filename = input("Enter filename to load (e.g., tasks.json): ")
            await repo.load_from_file(filename)
            print("Tasks loaded successfully!\n")

        elif command == "exit":
            break
        else:
            print("Invalid command. Try again.\n")


asyncio.run(main())