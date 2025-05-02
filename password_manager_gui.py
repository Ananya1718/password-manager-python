import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
import json
import os

# Load encryption key
def load_key():
    return open("key.key", "rb").read()

key = load_key()
fernet = Fernet(key)

# Add new password
def add_password():
    account = account_entry.get()
    password = password_entry.get()

    if not account or not password:
        messagebox.showwarning("Warning", "Please fill out both fields.")
        return

    encrypted_password = fernet.encrypt(password.encode())

    if os.path.exists("passwords.json"):
        with open("passwords.json", "r") as file:
            passwords = json.load(file)
    else:
        passwords = {}

    passwords[account] = encrypted_password.decode()

    with open("passwords.json", "w") as file:
        json.dump(passwords, file)

    messagebox.showinfo("Success", f"Password saved for {account}!")
    account_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# View password
def view_password():
    account = account_entry.get()

    if not account:
        messagebox.showwarning("Warning", "Please enter an account name.")
        return

    if not os.path.exists("passwords.json"):
        messagebox.showerror("Error", "No passwords stored yet.")
        return

    with open("passwords.json", "r") as file:
        passwords = json.load(file)

    if account in passwords:
        encrypted_password = passwords[account]
        decrypted_password = fernet.decrypt(encrypted_password.encode()).decode()
        messagebox.showinfo("Password Found", f"Password for {account}: {decrypted_password}")
    else:
        messagebox.showerror("Error", f"No password found for {account}.")

# Master password checking
def check_master_password():
    entered_password = master_password_entry.get()
    correct_password = "admin123"  # <-- You can change this to your own!

    if entered_password == correct_password:
        login_window.destroy()
        open_main_window()
    else:
        messagebox.showerror("Error", "Incorrect Master Password.")

# GUI for main app
def open_main_window():
    window = tk.Tk()
    window.title("Password Manager 🔐")
    window.geometry("400x300")
    window.resizable(False, False)

    tk.Label(window, text="Account:").pack(pady=10)
    global account_entry
    account_entry = tk.Entry(window, width=30)
    account_entry.pack()

    tk.Label(window, text="Password:").pack(pady=10)
    global password_entry
    password_entry = tk.Entry(window, width=30, show="*")
    password_entry.pack()

    tk.Button(window, text="Add Password", command=add_password).pack(pady=10)
    tk.Button(window, text="View Password", command=view_password).pack(pady=5)

    window.mainloop()

# Master password window
login_window = tk.Tk()
login_window.title("Login 🔒")
login_window.geometry("300x150")
login_window.resizable(False, False)

tk.Label(login_window, text="Enter Master Password:").pack(pady=10)
master_password_entry = tk.Entry(login_window, width=25, show="*")
master_password_entry.pack()

tk.Button(login_window, text="Login", command=check_master_password).pack(pady=10)

login_window.mainloop()

