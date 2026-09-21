import getpass
from datetime import datetime


class InputValidator:
    @staticmethod
    def get_valid_name(prompt, allow_skip=False):
        attempts = 3
        while attempts > 0:
            name = input(prompt).strip()
            if allow_skip and name.upper() == "B":
                return ""
            if name.isalpha():
                return name.title()
            attempts -= 1
            print(f"Invalid name, {attempts} attempt(s) left")
        return None


    @staticmethod
    def get_valid_date(prompt):
        attempts = 3
        while attempts > 0:
            raw_date = input(prompt).strip()
            try:
                date = datetime.strptime(raw_date, "%d/%m/%Y") # noqa: DTZ007
                if date > datetime.now(): 
                    attempts -= 1
                    print(f"Date can not be in the future, {attempts} attempt(s) left!")
                    continue
                return raw_date
            except ValueError:
                attempts -= 1
                print(f"Invalid format, {attempts} attempt(s) left")
        return None


    @staticmethod
    def get_valid_choice(prompt, valid_options):
        attempts = 3
        while attempts > 0:
            choice = input(prompt).strip().lower()
            if choice in valid_options:
                return choice.title()
            attempts -= 1
            print(f"Invalid format, {attempts} attempt(s) left")
        return None


    @staticmethod
    def get_valid_pin(prompt):
        attempts = 3
        while attempts > 0:
            pin =  getpass.getpass(prompt).strip()
            if not pin.isdigit():
                attempts -= 1
                print(f"Invalid format, {attempts} attempt(s) left")
            elif len(pin) != 4:
                attempts -= 1
                print(f"Pin must be 4 digits, {attempts} attempt(s) left")
            else:
                return pin
        return None

    @staticmethod
    def get_valid_amount(prompt):
        attempts = 3
        while attempts > 0:
            raw_amount = input(prompt)
            if raw_amount.upper() == "B":
                return "back"
            try:
                amount = float(raw_amount)
            except ValueError:
                attempts -= 1
                print(f"Invalid format, {attempts} attempt(s) left")
                continue
            if amount <= 0:
                attempts -= 1
                print(f"Amount must be greater than 0, {attempts} attempt(s) left")
            else:
                return amount
        return None