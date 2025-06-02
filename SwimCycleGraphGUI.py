import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Lists to store weekly data
weeks = []
cycling_km = []
swimming_km = []

# Adds data to the table and update lists
def add_data():
    week = len(weeks) + 1
    try:
        cycle = float(cycle_entry.get())
        swim = float(swim_entry.get())
    except ValueError:
        return  # Ignore if input is not a number

    weeks.append(f"Week {week}")
    cycling_km.append(cycle)
    swimming_km.append(swim)

    tree.insert("", "end", values=(f"Week {week}", cycle, swim, cycle + swim))
    cycle_entry.delete(0, tk.END)
    swim_entry.delete(0, tk.END)
    update_graph()

# Plot graph
def update_graph():
    total_km = [c + s for c, s in zip(cycling_km, swimming_km)]
    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(weeks, cycling_km, label="Cycling (km)", marker='o')
    ax.plot(weeks, swimming_km, label="Swimming (km)", marker='o')
    ax.plot(weeks, total_km, label="Total (km)", marker='o')
    ax.set_title("Weekly Distance")
    ax.set_ylabel("Distance (km)")
    ax.legend()
    ax.grid(True)
    canvas.draw()

# GUI Setup
root = tk.Tk()
root.title("Weekly Distance Tracker")

# Input fields
tk.Label(root, text="Cycling Distance (km):").grid(row=0, column=0, padx=5, pady=5)
cycle_entry = tk.Entry(root)
cycle_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(root, text="Swimming Distance (km):").grid(row=1, column=0, padx=5, pady=5)
swim_entry = tk.Entry(root)
swim_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(root, text="Add Week", command=add_data).grid(row=2, column=0, columnspan=2, pady=10)

# Table for data
columns = ("Week", "Cycling (km)", "Swimming (km)", "Total (km)")
tree = ttk.Treeview(root, columns=columns, show="headings")
for col in columns:
    tree.heading(col, text=col)
tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

# Graph display
fig = plt.Figure(figsize=(6, 4), dpi=100)
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(row=4, column=0, columnspan=2)

root.mainloop()
