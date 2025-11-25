import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Setup paths

DATA_FILE = "data/transactions.csv"
REPORT_FOLDER = "reports"

os.makedirs("data", exist_ok=True)
os.makedirs("reports", exist_ok=True)

# Initialize CSV if missing

if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["date", "type", "amount", "category"])
    df.to_csv(DATA_FILE, index=False)


# Load data

def load_data():
    return pd.read_csv(DATA_FILE)



# Add a transaction

def add_transaction(tr_type):
    amount = float(input("Enter amount: "))
    category = input("Enter category (Food, Rent, Travel, Salary): ")

    date = input("Enter date (YYYY-MM-DD) or press Enter for today: ")
    if date.strip() == "":
        date = datetime.today().strftime("%Y-%m-%d")

    df = load_data()
    new_entry = {
        "date": date,
        "type": tr_type,
        "amount": amount,
        "category": category
    }

    df = df.append(new_entry, ignore_index=True)
    df.to_csv(DATA_FILE, index=False)

    print("\n✔ Transaction saved successfully!\n")



# View current balance

def view_balance():
    df = load_data()

    total_income = df[df["type"] == "income"]["amount"].sum()
    total_expense = df[df["type"] == "expense"]["amount"].sum()
    balance = total_income - total_expense

    print("\n------ Balance Summary ------")
    print(f"Total Income : {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Current Balance: {balance}")
    print("-----------------------------\n")



# Monthly report + pie chart

def generate_monthly_report():
    df = load_data()
    if df.empty:
        print("No data available!")
        return

    month = input("Enter month (MM): ")
    year = input("Enter year (YYYY): ")

    df["date"] = pd.to_datetime(df["date"])
    monthly_data = df[(df["date"].dt.month == int(month)) &
                      (df["date"].dt.year == int(year))]

    if monthly_data.empty:
        print("\n❌ No transactions found for that month!\n")
        return

    # Category totals
    category_summary = monthly_data.groupby("category")["amount"].sum()

    # Export CSV
    csv_path = f"{REPORT_FOLDER}/monthly_report_{year}_{month}.csv"
    category_summary.to_csv(csv_path)

    # Create pie chart
    plt.figure(figsize=(6, 6))
    plt.pie(category_summary, labels=category_summary.index, autopct="%1.1f%%")
    plt.title(f"Spending Breakdown - {year}/{month}")

    chart_path = f"{REPORT_FOLDER}/monthly_piechart_{year}_{month}.png"
    plt.savefig(chart_path)
    plt.close()

    print("\n✔ Monthly report generated!")
    print(f"CSV saved to: {csv_path}")
    print(f"Pie chart saved to: {chart_path}\n")



# Menu

def menu():
    while True:
        print("Personal Finance Tracker")
        print("1. Add Income")
        print("2. Add Expense")
        print("3. View Balance")
        print("4. Generate Monthly Report")
        print("5. Exit")
        print("======================================")

        choice = input("Choose an option: ")

        if choice == "1":
            add_transaction("income")
        elif choice == "2":
            add_transaction("expense")
        elif choice == "3":
            view_balance()
        elif choice == "4":
            generate_monthly_report()
        elif choice == "5":
            print("Exiting program...")
            break
        else:
            print("Invalid option. Try again!\n")



# Run program

if __name__ == "__main__":
    menu()
