import math
import os

DATA_FILE = "bank.txt"
MIN_BALANCE = 500
FIRST_ACCOUNT_NO = 1001


def load_accounts():
    accounts = {}
    if not os.path.exists(DATA_FILE):
        return accounts

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split("|")
            if len(parts) != 3:
                continue
            try:
                acc_no = int(parts[0])
                balance = float(parts[2])
            except ValueError:
                continue
            accounts[acc_no] = {"name": parts[1], "balance": balance}
    return accounts


def save_accounts(accounts):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        for acc_no in sorted(accounts):
            acc = accounts[acc_no]
            f.write(f"{acc_no}|{acc['name']}|{acc['balance']}\n")


def fmt(amount):
    amount = round(amount, 2)
    if amount == int(amount):
        return str(int(amount))
    return str(amount)


def read_amount(prompt):
    text = input(prompt).strip()
    try:
        value = float(text)
    except ValueError:
        print("Invalid amount. Please enter a number.")
        return None
    if math.isnan(value) or math.isinf(value) or value <= 0:
        print("Invalid amount. Amount must be greater than 0.")
        return None
    return round(value, 2)


def read_account_no(prompt):
    text = input(prompt).strip()
    if not text.isdigit():
        print("Invalid account number. Please enter digits only.")
        return None
    return int(text)


def generate_account_no(accounts):
    if not accounts:
        return FIRST_ACCOUNT_NO
    return max(accounts) + 1


def create_account(accounts):
    name = input("Name: ").strip()
    if not name or "|" in name:
        print("Invalid name. Name cannot be empty or contain '|'.")
        return

    amount = read_amount("Opening deposit: ")
    if amount is None:
        return
    if amount < MIN_BALANCE:
        print(f"Opening deposit must be at least Rs.{MIN_BALANCE}. Account not created.")
        return

    acc_no = generate_account_no(accounts)
    accounts[acc_no] = {"name": name, "balance": amount}
    save_accounts(accounts)
    print(f"Account created. A/C No: {acc_no} | Balance: {fmt(amount)}")


def deposit(accounts):
    acc_no = read_account_no("Account number: ")
    if acc_no is None:
        return
    if acc_no not in accounts:
        print(f"Account {acc_no} not found.")
        return

    amount = read_amount("Deposit amount: ")
    if amount is None:
        return

    accounts[acc_no]["balance"] += amount
    save_accounts(accounts)
    print(f"Deposit successful. Balance: {fmt(accounts[acc_no]['balance'])}")


def withdraw(accounts):
    acc_no = read_account_no("Account number: ")
    if acc_no is None:
        return
    if acc_no not in accounts:
        print(f"Account {acc_no} not found.")
        return

    amount = read_amount("Withdraw amount: ")
    if amount is None:
        return

    if accounts[acc_no]["balance"] - amount < MIN_BALANCE:
        print(f"Insufficient balance. Minimum balance of Rs.{MIN_BALANCE} must remain.")
        return

    accounts[acc_no]["balance"] -= amount
    save_accounts(accounts)
    print(f"Withdrawal successful. Balance: {fmt(accounts[acc_no]['balance'])}")


def transfer(accounts):
    from_acc = read_account_no("From account number: ")
    if from_acc is None:
        return
    if from_acc not in accounts:
        print(f"Account {from_acc} not found. Transfer cancelled.")
        return

    to_acc = read_account_no("To account number: ")
    if to_acc is None:
        return
    if to_acc not in accounts:
        print(f"Account {to_acc} not found. Transfer cancelled.")
        return

    if from_acc == to_acc:
        print("Cannot transfer to the same account. Transfer cancelled.")
        return

    amount = read_amount("Transfer amount: ")
    if amount is None:
        return

    if accounts[from_acc]["balance"] - amount < MIN_BALANCE:
        print(f"Insufficient balance. Minimum balance of Rs.{MIN_BALANCE} must remain. "
              "Transfer cancelled.")
        return

    accounts[from_acc]["balance"] -= amount
    accounts[to_acc]["balance"] += amount
    save_accounts(accounts)
    print("Transfer successful.")
    print(f"{from_acc} balance: {fmt(accounts[from_acc]['balance'])} | "
          f"{to_acc} balance: {fmt(accounts[to_acc]['balance'])}")


def balance_enquiry(accounts):
    acc_no = read_account_no("Account number: ")
    if acc_no is None:
        return
    if acc_no not in accounts:
        print(f"Account {acc_no} not found.")
        return
    acc = accounts[acc_no]
    print(f"A/C No: {acc_no} | Name: {acc['name']} | Balance: {fmt(acc['balance'])}")


def show_menu():
    print("\n===== SIMPLE BANKING SYSTEM =====")
    print("1. Create account")
    print("2. Deposit")
    print("3. Withdraw")
    print("4. Transfer")
    print("5. Balance enquiry")
    print("6. Exit")


def main():
    accounts = load_accounts()

    while True:
        show_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            create_account(accounts)
        elif choice == "2":
            deposit(accounts)
        elif choice == "3":
            withdraw(accounts)
        elif choice == "4":
            transfer(accounts)
        elif choice == "5":
            balance_enquiry(accounts)
        elif choice == "6":
            print("Thank you for using the Simple Banking System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
