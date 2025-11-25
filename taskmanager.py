def add_task():
    name = input("Enter task name: ")
    description = input("Enter task description: ")
    task = {
        "name": name,
        "description": description,
        "completed": False
    }
    tasks.append(task)
    print(f"Task '{name}' added!")

def view_tasks():
    if not tasks:
        print("No tasks available.")
        return
    
    for task in tasks:
        status = "Completed" if task["completed"] else "Pending"
        print(f"{task['name']} - {status}")

def mark_completed():
    task_name = input("Enter the task name to mark as completed: ")
    for task in tasks:
        if task["name"].lower() == task_name.lower():
            task["completed"] = True
            print(f"Task '{task_name}' marked as completed.")
            return
    print(f"No task found with name '{task_name}'.")

tasks = []

def main():
    while True:
        print("\nSimple Task Manager")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task as Completed")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == "1":
            add_task()
        elif choice == "2":
            view_tasks()
        elif choice == "3":
            mark_completed()
        elif choice == "4":
            print("Exiting Task Manager.")
            break
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
