import json
from datetime import datetime

expenses = []

def add_expense():
    amount = float(input("Enter amount: "))
    category = input("Enter category (e.g., food, transport): ")
    note = input("Enter note (optional): ")
    date = input("Enter date (YYYY-MM-DD) or leave blank for today: ")
    if not date:
        date = datetime.today().strftime('%Y-%m-%d')
    
    expenses.append({
        "amount": amount,
        "category": category,
        "note": note,
        "date": date
    })
    print("Expense added!")

def view_expenses():
    if not expenses:
        print("No expenses recorded yet.")
    else:
        for i, expense in enumerate(expenses, 1):
            print(f"{i}. {expense['date']} | {expense['category']} | ${expense['amount']} | {expense['note']}")

def save_expenses():
    with open('expenses.json', 'w') as file:
        json.dump(expenses, file)
    print("Expenses saved to expenses.json")



while True:
    print("\n📊 Personal Expense Tracker")
    print("1. Add Expense")
    print("2. View Expenses")
    print("3. Save Expenses")
    print("4. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        add_expense()
    elif choice == "2":
        view_expenses()
    elif choice == "3":
        save_expenses()
    elif choice == "4":
        print("Goodbye!")
        break
    else:
        print("Invalid option, try again.")
