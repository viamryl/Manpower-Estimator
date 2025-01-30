import tkinter as tk
from tkinter import ttk

class App:
    def __init__(self,root):
        self.root = root
        self.root.title("Manpower Management System")
        self.root.geometry("1200x600")

        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.footer_frame = ttk.Frame(root)
        self.footer_frame.pack(fill=tk.X, padx=10, pady=10)

        self.rows = []

        self.system()

    def system(self):
        row_index = len(self.rows) + 1
        checkbox_var = tk.IntVar()
        checkbox = ttk.Checkbutton(self.table_frame, variable=checkbox_var, text="Mechanical", command=lambda: self.toggle_heading2(row_index, checkbox_var))
        checkbox.grid(row=row_index, column=0, padx=5, pady=5, sticky="w")
        
        self.rows.append([checkbox])
    
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
    


    def add_system(self):
        pass


if __name__ == '__main__':
    root = tk.Tk()
    app = App(root)
    root.mainloop()