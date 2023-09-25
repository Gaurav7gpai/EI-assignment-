from datetime import datetime

class TaskMemento:
    def __init__(self, task):
        self.task = task

class TaskBuilder:
    def __init__(self, description):
        self.description = description
        self.due_date = None
        self.completed = False

    def set_due_date(self, due_date):
        self.due_date = due_date
        return self
    
    def set_completed(self, completed):
        self.completed = completed
        return self
    
    def build(self):
        return Task(self)
    
class Task:
    def __init__(self, builder):
        self.description = builder.description
        self.due_date = builder.due_date
        self.completed = builder.completed

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        return f"{self.description} - {status}" + (f", Due: {self.due_date}" if self.due_date else "")

class ToDoListManager:
    def __init__(self):
        self.tasks = []
        self.history = []

    def add_task(self, task):
        self.tasks.append(task)
        self.history.append(TaskMemento(list(self.tasks)))

    def mark_completed(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                task.completed = True
                self.history.append(TaskMemento(list(self.tasks)))
                return
    
    def delete_task(self, task_description):
        self.tasks = [task for task in self.tasks if task.description != task_description]
        self.history.append(TaskMemento(list(self.tasks)))
    
    def undo(self):
        if len(self.history) > 1:
            self.history.pop()
            self.tasks = self.history[-1].tasks

    def view_task(self, filter_type):
        if filter_type == "Show all":
            return self.tasks
        elif filter_type == "Show completed":
            return [task for task in self.tasks if task.completed]
        elif filter_type == "Show pending":
            return [task for task in self.tasks if not task.completed]
        else:
            return[]
        
if __name__ == "__main__":
    todo_manager = ToDoListManager()

    while True:
        print("\nOptions")
        print("1. Add Task")
        print("2. Mark Completed")
        print("3. Delete Task")
        print("4. View Task")
        print("5. Undo")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            description = input("Enter task description: ")
            due_date = input("Enter due date(optional, press Enter to skip): ")
            task_builder = TaskBuilder(description)
            if due_date:
                task_builder.set_due_date(due_date)
            task = task_builder.build()
            todo_manager.add_task(task)

        elif choice == "2":
            task_description = input("Enter task description to mark as completed: ")
            todo_manager.mark_completed(task_description)

        elif choice == "3":
            task_description = input("Enter task description to delete: ")
            todo_manager.delete_task(task_description)

        elif choice == "4":
            filter_type = input("Enter filter type (Show all/Show completed/Show pending):")
            tasks = todo_manager.view_task(filter_type)
            for task in tasks:
                print(task)

        elif choice == "5":
            todo_manager.undo()

        elif choice == "6":
            break
        else:
            print("Invalid choice. Please try again. ")