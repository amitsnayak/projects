import json
from datetime import datetime

class Task:
  
    def __init__(self, title, priority, deadline, done=False):
        self.title = title
        self.priority = priority
        self.deadline = deadline
        self.done = done

    def mark_done(self):

        self.done = True

    def to_dict(self):
       
        return {
            "title": self.title,
            "priority": self.priority,
            "deadline": self.deadline,
            "done": self.done
        }

    @staticmethod
    def from_dict(data):
        return Task(data["title"], data["priority"], data["deadline"], data["done"])


class TodoList:
  
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.load_tasks()


    # Task Management
  
    def add_task(self, title, priority, deadline):
      
        try:
            datetime.strptime(deadline, "%Y-%m-%d")  # Validate date format
            task = Task(title, priority, deadline)
            self.tasks.append(task)
            print(f" Task '{title}' added successfully!")
        except ValueError:
            print(" Invalid date format. Please use YYYY-MM-DD.")

    def view_tasks(self, sort_by="priority"):
        if not self.tasks:
            print(" No tasks available.")
            return

        if sort_by == "priority":
            sorted_tasks = sorted(self.tasks, key=lambda t: t.priority)
        elif sort_by == "deadline":
            sorted_tasks = sorted(self.tasks, key=lambda t: t.deadline)
        else:
            sorted_tasks = self.tasks

        print("\n Your To-Do List:")
        for i, task in enumerate(sorted_tasks, start=1):
            status = "✔" if task.done else ""
            print(f"{i}. [{status}] {task.title} | Priority: {task.priority} | Deadline: {task.deadline}")
        print("")

    def mark_task_done(self, task_index):
        
        try:
            task = self.tasks[task_index - 1]
            task.mark_done()
            print(f" Task '{task.title}' marked as done!")
        except IndexError:
            print(" Invalid task number.")

   
    # Persistence
   
    def save_tasks(self):
        
        with open(self.filename, "w") as f:
            json.dump([task.to_dict() for task in self.tasks], f, indent=4)
        print("💾 Tasks saved successfully!")

    def load_tasks(self):
        
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task) for task in data]
        except FileNotFoundError:
            self.tasks = []

  
    # CLI Interface
    
    def run_cli(self):
       
        while True:
            print("\n=== To-Do List Menu ===")
            print("1. Add Task")
            print("2. View Tasks (sorted by priority)")
            print("3. View Tasks (sorted by deadline)")
            print("4. Mark Task as Done")
            print("5. Save & Exit")

            choice = input("Select an option (1-5): ")

            if choice == "1":
                title = input("Enter task title: ")
                priority = int(input("Enter priority (1=High, 2=Medium, 3=Low): "))
                deadline = input("Enter deadline (YYYY-MM-DD): ")
                self.add_task(title, priority, deadline)
            elif choice == "2":
                self.view_tasks(sort_by="priority")
            elif choice == "3":
                self.view_tasks(sort_by="deadline")
            elif choice == "4":
                self.view_tasks()
                try:
                    index = int(input("Enter task number to mark as done: "))
                    self.mark_task_done(index)
                except ValueError:
                    print(" Invalid input. Enter a number.")
            elif choice == "5":
                self.save_tasks()
                print(" Goodbye!")
                break
            else:
                print(" Invalid option. Please choose a number between 1-5.")


if __name__ == "__main__":
    todo_list = TodoList()
    todo_list.run_cli()

