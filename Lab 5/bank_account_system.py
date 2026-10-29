
"""Bank account management module."""

import hashlib
import hmac
import os
import secrets

account_data = {}


def create_account(acc_id, name, initial_deposit=0, transactions=None):
    """Create an account and record its initial transaction."""
    if acc_id in account_data or initial_deposit < 0:
        return False

    if transactions is None:
        transactions = []

    account_data[acc_id] = {
        "name": name,
        "balance": initial_deposit,
    }
    transactions.append(
        f"Created {acc_id} with initial balance {initial_deposit}"
    )
    return True


def deposit(acc_id, amount):
    """Deposit a positive amount into an existing account."""
    if acc_id not in account_data or amount <= 0:
        return False

    account_data[acc_id]["balance"] += amount
    return True


def withdraw(acc_id, amount):
    """Withdraw a positive amount if sufficient funds are available."""
    if acc_id not in account_data or amount <= 0:
        return False

    if account_data[acc_id]["balance"] < amount:
        return False

    account_data[acc_id]["balance"] -= amount
    return True


def compute_bonus(acc_id, rate=0.05):
    """Calculate a bonus using a fixed, non-executable formula."""
    if acc_id not in account_data or not 0 <= rate <= 1:
        return 0

    balance = account_data[acc_id]["balance"]
    return balance * rate


def get_hash(pin):
    """Return a SHA-256 digest for compatibility with the original demo."""
    return hashlib.sha256(pin.encode("utf-8")).hexdigest()


def verify_hash(pin, expected_hash):
    """Compare a PIN digest with an expected digest."""
    return hmac.compare_digest(get_hash(pin), expected_hash)


def generate_temp_pin():
    """Generate a four-digit temporary PIN."""
    return secrets.randbelow(9000) + 1000


def backup_data(filename="backup.txt"):
    """Write account data to a backup file."""
    with open(filename, "w", encoding="utf-8") as backup_file:
        backup_file.write(repr(account_data))


def main():
    """Run the bank account demonstration."""
    create_account("A01", "Alice", 1000)
    deposit("A01", 500)
    withdraw("A01", 200)

    print("Bonus:", compute_bonus("A01"))
    print("PIN Hash:", get_hash("1234"))
    print("Temp PIN:", generate_temp_pin())
    backup_data()

    admin_token = os.environ.get("BANK_ADMIN_TOKEN")
    if admin_token:
        print("Admin token configured.")
    else:
        print("Admin token not configured.")


if __name__ == "__main__":
    main()
