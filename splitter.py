import json
import os

DATA_FILE = "expenses.json"


def initialize_data_file():
    """Initialize JSON file if it doesn't exist."""
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w") as f:
            json.dump({"friends": [], "expenses": []}, f)


def load_data():
    """Load data from JSON file."""
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    """Save data to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def add_friend():
    """Add a new friend to the friends list."""
    name = input("Enter friend's name: ").strip()
    if not name:
        print("⚠️ Name cannot be empty!\n")
        return

    data = load_data()
    if name in data["friends"]:
        print("⚠️ Friend already exists!\n")
        return

    data["friends"].append(name)
    save_data(data)
    print(f"✔ Friend '{name}' added successfully!\n")


def add_expense():
    """Add a new expense and assign it to participants."""
    data = load_data()
    if not data["friends"]:
        print("⚠️ No friends found. Add friends first!\n")
        return

    try:
        amount = float(input("Enter total expense amount: "))
    except ValueError:
        print("⚠️ Invalid amount!\n")
        return

    paid_by = input("Who paid? (enter exact name): ").strip()
    if paid_by not in data["friends"]:
        print("⚠️ Friend not found in the list!\n")
        return

    print("\nSelect friends who shared this expense (comma-separated names):")
    print(f"Available friends: {', '.join(data['friends'])}")
    shared_by_input = input("Shared by: ").strip()
    shared_by = [name.strip() for name in shared_by_input.split(",") if name.strip() in data["friends"]]

    if not shared_by:
        print("⚠️ No valid participants selected!\n")
        return

    expense = {"amount": amount, "paid_by": paid_by, "shared_by": shared_by}
    data["expenses"].append(expense)
    save_data(data)
    print(f"✔ Expense of {amount:.2f} added successfully!\n")


def calculate_balances():
    """Calculate net balance for each friend."""
    data = load_data()
    friends = data["friends"]
    expenses = data["expenses"]

    balances = {friend: 0.0 for friend in friends}

    for exp in expenses:
        amount = exp["amount"]
        paid_by = exp["paid_by"]
        shared_by = exp["shared_by"]

        split_amount = amount / len(shared_by)
        balances[paid_by] += amount
        for participant in shared_by:
            balances[participant] -= split_amount

    return balances


def show_summary():
    """Display balances and debts between friends."""
    balances = calculate_balances()
    if not balances:
        print("⚠️ No friends or expenses found!\n")
        return

    print("\n====== BALANCE SUMMARY ======")
    for friend, balance in balances.items():
        print(f"{friend}: {balance:.2f}")
    print("=============================\n")

    # Determine debts
    debtors = {f: abs(v) for f, v in balances.items() if v < 0}
    creditors = {f: v for f, v in balances.items() if v > 0}

    if not debtors:
        print("Everyone is settled up! 🎉\n")
        return

    print("====== WHO OWES WHOM ======")
    debtor_list = list(debtors.items())
    creditor_list = list(creditors.items())

    i = j = 0
    while i < len(debtor_list) and j < len(creditor_list):
        debtor, debt_amt = debtor_list[i]
        creditor, credit_amt = creditor_list[j]

        settle_amt = min(debt_amt, credit_amt)
        print(f"{debtor} → {creditor}: {settle_amt:.2f}")

        debt_amt -= settle_amt
        credit_amt -= settle_amt
        debtor_list[i] = (debtor, debt_amt)
        creditor_list[j] = (creditor, credit_amt)

        if debt_amt == 0:
            i += 1
        if credit_amt == 0:
            j += 1

    print("=============================\n")


def menu():
    """Display main menu and handle user input."""
    while True:
        print("====== EXPENSE SPLITTER ======")
        print("1. Add Friend")
        print("2. Add Expense")
        print("3. Show Balance Summary")
        print("4. Exit")
        print("===============================")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_friend()
        elif choice == "2":
            add_expense()
        elif choice == "3":
            show_summary()
        elif choice == "4":
            print("Goodbye! 👋")
            break
        else:
            print("⚠️ Invalid choice. Try again.\n")


if __name__ == "__main__":
    initialize_data_file()
    menu()
