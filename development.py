import tkinter as tk
from tkinter import ttk

def calculate(*args):
    try:
        # Ambil input angka dari StringVar
        num1 = float(var1.get() if var1.get() else 0)
        num2 = float(var2.get() if var2.get() else 0)
        # Lakukan perhitungan (misalnya penjumlahan)
        result = num1 + num2
        # Tampilkan hasil ke scorecard
        result_label.config(text=f"Hasil: {result}")
    except ValueError:
        result_label.config(text="Input tidak valid!")

# Inisialisasi window Tkinter
root = tk.Tk()
root.title("Real-Time Scorecard Calculator (ttk)")

# Gunakan StringVar untuk melacak perubahan input
var1 = tk.StringVar()
var2 = tk.StringVar()

# Bind perubahan input ke fungsi calculate
var1.trace_add("write", calculate)
var2.trace_add("write", calculate)

# Styling menggunakan ttk
style = ttk.Style()
style.configure("TLabel", font=("Arial", 10))
style.configure("TEntry", padding=5)
style.configure("TFrame", padding=10)
style.configure("TButton", padding=5)

# Frame utama untuk tata letak
frame = ttk.Frame(root)
frame.grid(padx=10, pady=10)

# Input angka pertama
ttk.Label(frame, text="Angka 1:").grid(row=0, column=0, padx=5, pady=5)
entry1 = ttk.Entry(frame, textvariable=var1, width=20)
entry1.grid(row=0, column=1, padx=5, pady=5)

# Input angka kedua
ttk.Label(frame, text="Angka 2:").grid(row=1, column=0, padx=5, pady=5)
entry2 = ttk.Entry(frame, textvariable=var2, width=20)
entry2.grid(row=1, column=1, padx=5, pady=5)

# Scorecard untuk menampilkan hasil
result_label = ttk.Label(frame, text="Hasil: ", font=("Arial", 12), relief="solid", anchor="w", background="white")
result_label.grid(row=2, column=0, columnspan=2, pady=10, sticky="we")

# Menjalankan aplikasi
root.mainloop()
