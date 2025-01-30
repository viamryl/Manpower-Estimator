import tkinter as tk
from tkinter import ttk

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manpower Management System")
        self.root.geometry("1200x600")

        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.footer_frame = ttk.Frame(root)
        self.footer_frame.pack(fill=tk.X, padx=10, pady=10)

        self.rows = []
        self.init_checkboxes()

    def create_checkboxes (self, checkbox_name):
        self.add_checkbox(checkbox_name)

    def init_checkboxes(self):
        # Tambahkan checkbox pertama
        self.add_checkbox("Mechanical")
        self.add_checkbox("Piping")
        self.add_checkbox("Insulation")

    def add_checkbox(self, label_text):
        row_index = len(self.rows)
        checkbox_var = tk.IntVar()  # Variabel kontrol untuk checkbox
        checkbox = ttk.Checkbutton(
            self.table_frame,
            variable=checkbox_var,
            text=label_text,
            command=lambda: self.toggle_heading2(row_index, checkbox_var)
        )
        checkbox.grid(row=row_index, column=0, padx=5, pady=5, sticky="w")

        # Menambahkan checkbox ke dalam rows (untuk manajemen struktur baris jika diperlukan)
        self.rows.append([checkbox, checkbox_var, None, None, None, None])

    def toggle_heading2(self, row_index, checkbox_var):
        pass

root = tk.Tk()
app = MyApp(root)
root.mainloop()
