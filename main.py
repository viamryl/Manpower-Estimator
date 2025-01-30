import math
import tkinter as tk
from tkinter import ttk
import shutil
import os
import threading

class DynamicTableApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dynamic GUI Table")
        self.root.geometry("800x600")

        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.footer_frame = ttk.Frame(root)
        self.footer_frame.pack(fill=tk.X, padx=10, pady=10)

        self.rows = []

        # self.create_headers()

        # Tambahkan 3 checkbox dengan default entry yang bisa diperluas
        for _ in range(3):
            self.add_heading1_row()

        self.create_footer()

    def create_headers(self):
        headers = ["Title", "Quantity", "Unit", "Productivity", "Time/Person", "Duration", "Manpower"]
        for col, header in enumerate(headers):
            label = ttk.Label(self.table_frame, text=header, anchor=tk.CENTER)
            label.grid(row=0, column=col, sticky="nsew", padx=5, pady=5)

    def add_heading1_row(self):
        row_index = len(self.rows) + 1

        # Checkbox dan entry untuk Heading 1
        checkbox_var = tk.BooleanVar()
        checkbox = ttk.Checkbutton(self.table_frame, variable=checkbox_var, text="Heading 1", command=lambda: self.toggle_heading2(row_index, checkbox_var))
        checkbox.grid(row=row_index, column=0, padx=5, pady=5, sticky="w")

        title_entry = ttk.Entry(self.table_frame)
        title_entry.grid(row=row_index, column=1, columnspan=6, sticky="ew", padx=5, pady=5)

        # Heading 2 rows (initially hidden)
        heading2_entries = []
        for _ in range(3):
            entries = []
            sub_row_index = row_index + len(heading2_entries) + 1
            for col in range(1, 7):
                entry = ttk.Entry(self.table_frame)
                entry.grid(row=sub_row_index, column=col, padx=5, pady=5)
                entry.grid_remove()
                entries.append(entry)

            heading2_entries.append(entries)

        self.rows.append((checkbox_var, heading2_entries))

    def toggle_heading2(self, row_index, checkbox_var):
        # Ensure the row index corresponds to the correct data structure
        if row_index - 1 < len(self.rows):
            _, heading2_entries = self.rows[row_index - 1]
            if isinstance(heading2_entries, list):
                for entries in heading2_entries:
                    if isinstance(entries, list):
                        for entry in entries:
                            if checkbox_var.get():
                                entry.grid()
                            else:
                                entry.grid_remove()

    def create_footer(self):
        self.summary_label = ttk.Label(self.footer_frame, text="Summary: ...", anchor=tk.W)
        self.summary_label.pack(side=tk.LEFT, padx=5, pady=5)

        calculate_button = ttk.Button(self.footer_frame, text="Calculate", command=self.calculate_summary)
        calculate_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def calculate_summary(self):
        total_quantity = 0
        total_manpower = 0

        for checkbox_var, entries in self.rows:
            if checkbox_var and checkbox_var.get():
                for entry_row in entries:
                    if isinstance(entry_row, list):
                        try:
                            quantity = float(entry_row[0].get())
                            manpower = float(entry_row[-1].get())
                        except ValueError:
                            quantity = 0
                            manpower = 0

                        total_quantity += quantity
                        total_manpower += manpower

        self.summary_label.config(text=f"Summary: Total Quantity = {total_quantity}, Total Manpower = {total_manpower}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DynamicTableApp(root)
    root.mainloop()
