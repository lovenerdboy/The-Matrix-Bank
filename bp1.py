import json
import os
import getpass
from inputvalidator import InputValidator


# Account classes
class Account:
    next_account_number = 100

    def __init__(self, first_name, last_name, middle_name, dob, gender, address, account_type, pin, balance=0, account_number=None):
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.dob = dob
        self.gender = gender
        self.address = address
        self.account_type = account_type
        self.pin = pin
        self.balance = balance

        if account_number is not None:
            self.account_number = account_number
        else:
            self.account_number = Account.generate_account_number()


    @classmethod
    def generate_account_number(cls):
        Account.next_account_number += 1
        return Account.next_account_number


    def check_pin(self, entered_pin):
        return str(entered_pin) == str(self.pin)


    def show_balance(self):
        print(f"Your balance is ${self.balance:,.2f}")


    def deposit(self, amount):
        self.balance += amount
        print(f"${amount:,.2f} has been deposited!")


    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds")
            return False
        self.balance -= amount
        print(f"${amount:,.2f} has been withdrawn")
        return True


    def cus_dict(self):
        return {
            "account_number": self.account_number,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "middle_name": self.middle_name,
            "dob": self.dob,
            "gender": self.gender,
            "address": self.address,
            "account_type": self.account_type,
            "pin": self.pin,
            "balance": self.balance,
        }


    def __str__(self):
        full_name = f"{self.first_name} {self.middle_name} {self.last_name}".replace("  ", " ")
        return (f"Account #{self.account_number} * {full_name} * {self.account_type} * Balance: ${self.balance:,.2f}")


class SavingsAccount(Account):
    DATA_FILE = "savings.json"


class CurrentAccount(Account):
    DATA_FILE = "current.json"
    OVERDRAFT_LIMIT = 10000

    def withdraw(self, amount):
        if amount > self.balance + CurrentAccount.OVERDRAFT_LIMIT:
            print("Insufficient funds (overdraft limit reached)")
            return False
        self.balance -= amount
        print(f"${amount:,.2f} has been withdrawn")
        return True

    
#  Bank class registration, login, menu, file storage
class Bank:
    bank_name = "The Matrix Bank"

    def __init__(self):
        self.accounts = {}
        self.load_accounts()


    #FILE HANDLING
    def load_accounts(self):
        self.load_one_file(SavingsAccount)
        self.load_one_file(CurrentAccount)


    def load_one_file(self, account_class):
        if not os.path.exists(account_class.DATA_FILE):
            return

        with open(account_class.DATA_FILE, "r") as file:
            data = json.load(file)

        for details in data.values():
            account = account_class(
                details["first_name"],
                details["last_name"],
                details["middle_name"],
                details["dob"],
                details["gender"],
                details["address"],
                details["account_type"],
                details["pin"],
                details["balance"],
                details["account_number"]
            )
            self.accounts[account.account_number] = account

            Account.next_account_number = max(Account.next_account_number, account.account_number)


    def save_accounts(self):
        savings_data = {}
        current_data = {}

       
        for account in self.accounts.values():
            if account.account_type == "Savings":
                savings_data[account.account_number] = account.cus_dict()
            else:
                current_data[account.account_number] = account.cus_dict()

        
        with open(SavingsAccount.DATA_FILE, "w") as file:
            json.dump(savings_data, file, indent=4)

        with open(CurrentAccount.DATA_FILE, "w") as file:
            json.dump(current_data, file, indent=4)

    # registration and login

    def register_customer(self):
        print(f"WELCOME TO {Bank.bank_name.upper()}")

        first_name = InputValidator.get_valid_name("\nEnter your first name: ")
        if first_name is None:
            return None

        last_name = InputValidator.get_valid_name("Enter your last name: ")
        if last_name is None:
            return None

        middle_name = InputValidator.get_valid_name("Enter your middle name (or B to skip): ", allow_skip=True)
        if middle_name is None:
            return None

        dob = InputValidator.get_valid_date("Enter your date of birth (DD/MM/YYYY): ")
        if dob is None:
            return None

        gender = InputValidator.get_valid_choice("Enter your gender (Male/Female): ", ["male", "female"])
        if gender is None:
            return None

        account_type = InputValidator.get_valid_choice("Enter account type (Savings/Current): ", ["savings", "current"])
        if account_type is None:
            return None

        address = input("Enter your address: ").strip().title()
        if not address:
            print("Address can not be empty. Registration ended.")
            return None

        pin = InputValidator.get_valid_pin("Enter your 4 digit pin: ")
        if pin is None:
            return None

        if account_type == "Current":
            account = CurrentAccount(first_name, last_name, middle_name, dob, gender, address, account_type, pin)
        else:
            account = SavingsAccount(first_name, last_name, middle_name, dob, gender, address, account_type, pin)

        self.accounts[account.account_number] = account
        self.save_accounts()

        print("\nREGISTRATION DETAILS")
        print(account)
        print(f"Middle Name: {middle_name if middle_name else 'Not provided'}")
        print(f"Date of Birth: {dob}")
        print(f"Pin: {pin}")
        print(f"\nYour account number is {account.account_number}")
        print("Registration successful...")

        return account

    def login(self):
        attempts = 3
        while attempts > 0:
            raw_number = input("\nEnter your account number: ").strip()
            if not raw_number.isdigit() or int(raw_number) not in self.accounts:
                attempts -= 1
                print(f"Account not found, {attempts} attempt(s) left")
                continue

            account = self.accounts[int(raw_number)]

            pin_attempts = 3
            while pin_attempts > 0:
                entered_pin = getpass.getpass("Enter your pin: ").strip()
                if account.check_pin(entered_pin):
                    return account
                pin_attempts -= 1
                print(f"Incorrect pin, {pin_attempts} attempt(s) left")

            print("Too many pin attempts, try again later")
            return None

        print("Too many attempts, try again later")
        return None


    # main menu
    def run(self):
        print(f"{Bank.bank_name}")
        choice = InputValidator.get_valid_choice("Are you a (N)ew or (E)xisting customer? ", ["n", "e"])

        if choice == "N":
            account = self.register_customer()
        elif choice == "E":
            account = self.login()
        else:
            return

        if account is None:
            return

        is_running = True
        while is_running:
            print(f"\nWelcome, {account.first_name}!")
            print("1. Show Balance")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Exit")

            menu_choice = input("Enter your choice (1-4): ").strip()

            if menu_choice == "1":
                account.show_balance()
            elif menu_choice == "2":
                amount = InputValidator.get_valid_amount("Enter an amount to deposit (or B to go back): ")
                if amount == "back" or amount is None:
                    continue
                account.deposit(amount)
                self.save_accounts()
            elif menu_choice == "3":
                amount = InputValidator.get_valid_amount("Enter an amount to withdraw (or B to go back): ")
                if amount == "back" or amount is None:
                    continue
                account.withdraw(amount)
                self.save_accounts()
            elif menu_choice == "4":
                is_running = False
                print("Have a nice day!")
            else:
                print("Invalid choice, please try again.")


if __name__ == "__main__":
    bank = Bank()
    bank.run()