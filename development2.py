import tkinter as tk
from tkinter import ttk

def calculate_realtime(event):
    try:
        # Ambil nilai dari entry
        qty = float(qty_entry.get()) if qty_entry.get() else 0
        productivity = float(productivity_entry.get()) if productivity_entry.get() else 0

        # Lakukan perhitungan
        if productivity != 0:
            result = qty / productivity
        else:
            result = 0

        # Tampilkan hasil di label
        result_label.config(text=f"Result: {result:.2f}")
    except ValueError:
        result_label.config(text="Invalid input!")  # Jika input bukan angka

# GUI Utama
root = tk.Tk()
root.title("Realtime Calculation without TextVariable")

# Entry untuk QTY
qty_label = ttk.Label(root, text="QTY:")
qty_label.grid(row=0, column=0, padx=5, pady=5)
qty_entry = ttk.Entry(root)
qty_entry.grid(row=0, column=1, padx=5, pady=5)

# Entry untuk Productivity
productivity_label = ttk.Label(root, text="Productivity:")
productivity_label.grid(row=1, column=0, padx=5, pady=5)
productivity_entry = ttk.Entry(root)
productivity_entry.grid(row=1, column=1, padx=5, pady=5)

# Label untuk menampilkan hasil
result_label = ttk.Label(root, text="Result: 0.00", font=("Arial", 12, "bold"))
result_label.grid(row=2, column=0, columnspan=2, pady=10)

# Bind event "<KeyRelease>" ke entry
qty_entry.bind("<KeyRelease>", calculate_realtime)
productivity_entry.bind("<KeyRelease>", calculate_realtime)

root.mainloop()
