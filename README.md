# The-Matrix-Bank
An ATM/Banking software built in Python using Object Oriented Programming(OOP).

## Features

- Customer registration 
- Login with account number and pin
- Deposit, withdraw, and balance check
- File Storage and Management for New and Existing Accounts.
  
## How to run

```
python bp1.py
```

You'll be asked whether you're a new or existing customer, then walked through registration or login.

## Account Data Storage and Management

Every time an account is registered, or a deposit/withdrawal happens, account data is written to `savings.json` or `current.json` depending on the account type. On startup, both files are read back in automatically, so accounts and balances survive closing and reopening the program.
