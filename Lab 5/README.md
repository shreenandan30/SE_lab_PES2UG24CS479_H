# Lab 5: Static Code Analysis — Bank Account System

**Application:** `bank_account_system.py`

## About the program

A bank account ledger manager. It handles account creation, deposits, withdrawals, promotional bonus calculation, and ledger exports.

## Run and analyze

1. Run the program:
   ```bash
   python bank_account_system.py
   ```
2. Install the analysis tools:
   ```bash
   pip install pylint bandit flake8
   ```
3. Run the reports:
   ```bash
   pylint bank_account_system.py > pylint_report.txt
   bandit -r bank_account_system.py > bandit_report.txt
   flake8 bank_account_system.py > flake8_report.txt
   ```

## Deliverables

- `bank_account_system.py`: cleaned application code.
- Pylint, Bandit and Flake8 reports from before and after changes.
- `Lab5_Static_Code_Analysis_Report.pdf`: report document.

Refer to the Lab 5 handout for the complete instructions.
