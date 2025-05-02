from cryptography.fernet import Fernet
import json
import os

# Load the encryption key
def load_key():
    return open("key.key", "rb").read()

key = load_key()
fernet = Fernet(key)

# Add a new password
def add_password(account, password):
    encrypted_password = fernet.encrypt(password.encode())

    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            passwords = json.load(file)
    else:
        passwords = {}

    passwords[account] = encrypted_password.decode()

    with open("passwords.json", "w") as file:
        json.dump(passwords, file)

# View a saved password
def view_password(account):
    if not os.path.exists("passwords.json"):
        print("No passwords stored yet.")
        return

    with open("passwords.json", "r") as file:
        passwords = json.load(file)

    if account in passwords:
        encrypted_password = passwords[account]
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        print(f"Password for {account}: {decrypted_password}")
    else:
        print(f"No password found for {account}.")

# Simple CLI for now (GUI later!)
def main():
    while True:
        mode = input("\nWould you like to add a new password or view an existing one (add/view/quit)? ").lower()
        if mode == "quit":
            break
        elif mode == "add":
            account = input("Enter the account name (e.g., Gmail, Facebook): ")
            password = input("Enter the password: ")
            add_password(account, password)
        elif mode == "view":
            account = input("Enter the account name to view: ")
            view_password(account)
        else:
            print("Invalid option.")

if __name__ == "__main__":
    main()
