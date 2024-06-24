import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt

# Database initialization
db_connection = sqlite3.connect('bmi_records.db')
db_cursor = db_connection.cursor()
db_cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_entries (
                        entry_id INTEGER PRIMARY KEY AUTOINCREMENT,
                        body_weight REAL,
                        body_height REAL,
                        body_bmi REAL,
                        bmi_category TEXT)''')
db_connection.commit()

def compute_bmi(weight, height_cm):
    height_m = height_cm / 100  # Convert height from cm to meters
    return weight / (height_m ** 2)

def determine_bmi_category(bmi_value):
    if bmi_value < 18.5:
        return "Underweight"
    elif 18.5 <= bmi_value < 24.9:
        return "Normal weight"
    elif 25 <= bmi_value < 29.9:
        return "Overweight"
    else:
        return "Obesity"

def store_bmi_data(weight, height_cm, bmi_value, category):
    db_cursor.execute("INSERT INTO bmi_entries (body_weight, body_height, body_bmi, bmi_category) VALUES (?, ?, ?, ?)",
                      (weight, height_cm, bmi_value, category))
    db_connection.commit()

def compute_and_display_bmi():
    try:
        weight = float(weight_input.get())
        height_cm = float(height_input.get())

        if weight <= 0 or height_cm <= 0:
            raise ValueError("Weight and height must be positive values.")

        bmi_value = compute_bmi(weight, height_cm)
        category = determine_bmi_category(bmi_value)
        store_bmi_data(weight, height_cm, bmi_value, category)

        bmi_label.config(text=f"BMI: {bmi_value:.2f}")
        category_label.config(text=f"Category: {category}")

        messagebox.showinfo("Result", f"Your BMI is {bmi_value:.2f} ({category})")
    except ValueError as error:
        messagebox.showerror("Invalid input", str(error))

def display_bmi_history():
    db_cursor.execute("SELECT * FROM bmi_entries")
    records = db_cursor.fetchall()
    history_text = "\n".join([f"Weight: {record[1]} kg, Height: {record[2]} cm, BMI: {record[3]:.2f}, Category: {record[4]}" for record in records])
    messagebox.showinfo("History", history_text)

def plot_bmi_history():
    db_cursor.execute("SELECT entry_id, body_bmi FROM bmi_entries")
    data = db_cursor.fetchall()
    if not data:
        messagebox.showwarning("No data", "No historical data to plot.")
        return

    entry_ids, bmis = zip(*data)
    plt.plot(entry_ids, bmis, marker='o')
    plt.title("BMI History")
    plt.xlabel("Entry ID")
    plt.ylabel("BMI")
    plt.show()

# GUI setup
app_window = tk.Tk()
app_window.title("BMI Calculator")

tk.Label(app_window, text="Weight (kg):").grid(row=0, column=0)
tk.Label(app_window, text="Height (cm):").grid(row=1, column=0)

weight_input = tk.Entry(app_window)
height_input = tk.Entry(app_window)

weight_input.grid(row=0, column=1)
height_input.grid(row=1, column=1)

tk.Button(app_window, text="Calculate BMI", command=compute_and_display_bmi).grid(row=2, column=0, columnspan=2)
tk.Button(app_window, text="Show History", command=display_bmi_history).grid(row=3, column=0, columnspan=2)
tk.Button(app_window, text="Plot History", command=plot_bmi_history).grid(row=4, column=0, columnspan=2)

bmi_label = tk.Label(app_window, text="BMI: N/A")
bmi_label.grid(row=5, column=0, columnspan=2)

category_label = tk.Label(app_window, text="Category: N/A")
category_label.grid(row=6, column=0, columnspan=2)

app_window.mainloop()

# Close database connection when the application exits
db_connection.close()
