import tkinter as tk
from tkinter import messagebox
import random
import string
import pyperclip

def generate_random_password(length, include_letters, include_digits, include_special_chars):
    char_pool = ''
    if include_letters:
        char_pool += string.ascii_letters
    if include_digits:
        char_pool += string.digits
    if include_special_chars:
        char_pool += string.punctuation

    if not char_pool:
        raise ValueError("At least one character type must be selected.")

    return ''.join(random.choice(char_pool) for _ in range(length))

def handle_generate():
    try:
        length = int(password_length_entry.get())
        use_letters = letters_var.get()
        use_numbers = numbers_var.get()
        use_symbols = symbols_var.get()

        if length <= 0:
            raise ValueError("Password length must be a positive integer.")

        password = generate_random_password(length, use_letters, use_numbers, use_symbols)
        result_entry.delete(0, tk.END)
        result_entry.insert(0, password)
    except ValueError as error:
        messagebox.showerror("Input Error", str(error))

def handle_copy():
    password = result_entry.get()
    if password:
        pyperclip.copy(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")
    else:
        messagebox.showwarning("No Password", "Generate a password first.")

# GUI Setup
app_window = tk.Tk()
app_window.title("Password Generator")

tk.Label(app_window, text="Password Length:").grid(row=0, column=0, sticky='e')
password_length_entry = tk.Entry(app_window)
password_length_entry.grid(row=0, column=1)

letters_var = tk.BooleanVar(value=True)
numbers_var = tk.BooleanVar(value=True)
symbols_var = tk.BooleanVar(value=True)

tk.Checkbutton(app_window, text="Include Letters", variable=letters_var).grid(row=1, column=0, columnspan=2)
tk.Checkbutton(app_window, text="Include Numbers", variable=numbers_var).grid(row=2, column=0, columnspan=2)
tk.Checkbutton(app_window, text="Include Symbols", variable=symbols_var).grid(row=3, column=0, columnspan=2)

tk.Button(app_window, text="Generate", command=handle_generate).grid(row=4, column=0, columnspan=2)
tk.Button(app_window, text="Copy to Clipboard", command=handle_copy).grid(row=5, column=0, columnspan=2)

tk.Label(app_window, text="Generated Password:").grid(row=6, column=0, sticky='e')
result_entry = tk.Entry(app_window, width=40)
result_entry.grid(row=6, column=1)

app_window.mainloop()
