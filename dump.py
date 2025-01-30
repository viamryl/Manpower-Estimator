import tkinter as tk
from tkinter import ttk
import math

class MyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Manpower Calculator")
        self.root.geometry("1200x600")

        self.table_frame = ttk.Frame(root)
        self.table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.footer_frame = ttk.Frame(root)
        self.footer_frame.pack(fill=tk.X, padx=10, pady=10)
        self.data_percols = 0

        self.manpower_total = 0

        self.rows = []
        self.create_checkboxes()    

    def create_checkboxes(self):
        # Tambahkan checkbox pertama
        self.add_checkbox("Mechanical", ["Static", "Rotatic", "Steel Structure"])

        # Tambahkan checkbox kedua
        self.add_checkbox("Piping", ["Stainless", "Carbon"])

        # Tambahkan checkbox kedua
        self.add_checkbox("Insulation", ["Hot Insulation", "Cold Insulation"])

    def add_checkbox(self, label_text, child_label):
        # Menentukan row index berdasarkan jumlah row yang ada
        row_index = len(self.rows)
        checkbox_var = tk.IntVar()  # Variabel kontrol untuk checkbox
        checkbox = ttk.Checkbutton(
            self.table_frame,
            variable=checkbox_var,
            text=label_text,
            command=lambda: self.toggle_heading2(row_index, checkbox_var, child_label)
        )
        checkbox.grid(row=row_index, column=0, padx=5, pady=5, sticky="w")

        # Menambahkan checkbox ke dalam rows (untuk manajemen struktur baris jika diperlukan)
        self.rows.append([checkbox, checkbox_var, None, None, None, None])
        # print(self.rows)
        # print(row_index)

    def toggle_heading2(self, row_index, checkbox_var, child_label):
        # Menampilkan atau menghapus entri berdasarkan status checkbox
        if checkbox_var.get():  # Jika checkbox dicentang
            # Menambahkan entry hanya jika belum ada
            if self.rows[row_index][2] is None:  # Cek jika belum ada widget
                # Hitung posisi dinamis untuk baris baru
                current_row = self.calculate_next_row(row_index)

                # Iterasi melalui child_label untuk membuat widget secara dinamis
                widgets = []
                for idx, label in enumerate(child_label):
                    self.data_percols = 0
                    # Tambahkan widget sesuai dengan tipe label atau data
                    description = ttk.Label(self.table_frame, text=label)
                    description.grid(row=current_row, column=idx, padx=5, pady=5, sticky="w")
                    widgets.append(description)
                    self.data_percols +=1

                    # Menambahkan kolom tambahan di sebelah label seperti QTY, UOM, dan Productivity
                    qty_entry = ttk.Entry(self.table_frame)
                    qty_entry.grid(row=current_row, column=idx+1, padx=5, pady=5)
                    self.set_placeholder(qty_entry, "QTY")
                    widgets.append(qty_entry)
                    self.data_percols +=1

                    uom = ttk.Combobox(self.table_frame, values=["TON", "ID", "M2"], width=4)
                    uom.grid(row=current_row, column=idx+2, padx=2, pady=5)
                    self.set_placeholder(uom, "Unit of Metrics")
                    widgets.append(uom)
                    self.data_percols +=1

                    productivity = ttk.Entry(self.table_frame)
                    productivity.grid(row=current_row, column=idx+3, padx=5, pady=5)
                    self.set_placeholder(productivity, "Productivity")
                    # productivity.insert(0, 0.6)  # Nilai default dimasukkan
                    widgets.append(productivity)
                    self.data_percols +=1

                    duration = ttk.Entry(self.table_frame)
                    duration.grid(row=current_row, column=idx+4, padx=5, pady=5)
                    self.set_placeholder(duration, "Duration (day)")
                    widgets.append(duration)
                    self.data_percols +=1

                    avg_salary = ttk.Entry(self.table_frame)
                    avg_salary.grid(row=current_row, column=idx+5, padx=5, pady=5)
                    self.set_placeholder(avg_salary, "Avg Salary (Juta)")
                    widgets.append(avg_salary)
                    self.data_percols +=1

                    # Label untuk menampilkan hasil perhitungan
                    tpp_label = ttk.Label(self.table_frame, text="Time/person: ")
                    tpp_label.grid(row=current_row, column=idx+6, padx=5, pady=5, sticky="w")
                    widgets.append(tpp_label)
                    self.data_percols +=1

                    manpower_label = ttk.Label(self.table_frame, text="Manpower: ")
                    manpower_label.grid(row=current_row, column=idx+6, padx=5, pady=5, sticky="w")
                    widgets.append(manpower_label)
                    self.data_percols +=1

                    # Bind event "<KeyRelease>" ke entry
                    qty_entry.bind("<KeyRelease>", lambda event, qty=qty_entry, prod=productivity, label=tpp_label, duration = duration, manpower = manpower_label: self.calculate_realtime(qty, prod, label, duration, manpower))
                    productivity.bind("<KeyRelease>", lambda event, qty=qty_entry, prod=productivity, label=tpp_label, duration = duration, manpower = manpower_label: self.calculate_realtime(qty, prod, label, duration, manpower))
                    duration.bind("<KeyRelease>", lambda event, qty=qty_entry, prod=productivity, label=tpp_label, duration = duration, manpower = manpower_label: self.calculate_realtime(qty, prod, label, duration, manpower))

                    current_row += 1  # Perbarui row setelah menambahkan kolom

                # Simpan widget ke dalam self.rows
                self.rows[row_index][2:] = widgets

                # Perbarui posisi checkbox di bawahnya
                self.update_positions()

                # Lakukan perhitungan otomatis setelah nilai default dimasukkan
                self.calculate_realtime(qty_entry, productivity, tpp_label, duration, manpower_label)

        else:  # Jika checkbox tidak dicentang
            # Menghapus entri dan widget berdasarkan child_label
            for widget in self.rows[row_index][2:]:
                if widget:
                    widget.grid_forget()  # Hapus widget dari grid
            self.rows[row_index][2:] = [None] * len(child_label) * 4  # Reset sesuai panjang child_label dan jumlah kolom tambahan

            # Perbarui posisi checkbox di bawahnya
            self.update_positions()

    def calculate_realtime(self, qty_entry, productivity, tpp_label, duration, manpower_label  ):
        try:
        # Ambil nilai dari entry, pastikan jika kosong atau tidak valid maka beri default 0
            qty = float(qty_entry.get()) if qty_entry.get() and qty_entry.get() != "QTY" else 0
            prod = float(productivity.get()) if productivity.get() and productivity.get() != "Productivity" else 0
            dur = float(duration.get()) if duration.get() and duration.get() != "Duration (day)" else 1  # Default 1 untuk hindari pembagian dengan 0

            # Lakukan perhitungan jika nilai valid
            if prod > 0 and dur > 0:
                # Perhitungan Time per Person (tpp)
                tpp_result = qty / prod
                tpp_label.config(text=f"Time/person: {tpp_result:.0f}")

                # Perhitungan Manpower berdasarkan tpp dibagi duration
                manpower_result = tpp_result / dur
                manpower_label.config(text=f"Manpower: {manpower_result:.0f}")
            else:
                tpp_label.config(text="Time/person:")  # Tampilkan error jika ada kesalahan
                manpower_label.config(text="Manpower:")
        except ValueError:
            tpp_label.config(text="Time/person:")  # Jika input bukan angka
            manpower_label.config(text="Manpower:")

    def set_placeholder(self, entry, placeholder):
        entry.insert(0, placeholder)  # Tambahkan teks placeholder
        entry.config(foreground="grey")  # Ubah warna teks placeholder

        def on_focus_in(event):
            if entry.get() == placeholder:
                entry.delete(0, "end")  # Hapus teks placeholder
                entry.config(foreground="black")  # Ubah warna teks menjadi normal

        def on_focus_out(event):
            if not entry.get():  # Jika teks kosong, kembalikan placeholder
                entry.insert(0, placeholder)
                entry.config(foreground="grey")

        entry.bind("<FocusIn>", on_focus_in)  # Bind event saat fokus masuk
        entry.bind("<FocusOut>", on_focus_out)

    def update_positions(self):
        """Perbarui posisi semua checkbox dan form secara dinamis."""
        current_row = 0
        for row in self.rows:
            # Perbarui posisi checkbox
            row[0].grid(row=current_row, column=0, padx=5, pady=5, sticky="w")
            current_row += 1

            # Jika ada form tambahan, posisikan di bawah checkbox
            if row[2] is not None:
                cols = 0
                for idx, widget in enumerate(row[2:]):
                    if idx % self.data_percols == 0:
                        current_row +=1
                        cols = 0
                        widget.grid(row=current_row, column=cols, padx=5, pady=5)
                    else:    
                        cols += 1
                        widget.grid(row=current_row, column=cols, padx=5, pady=5)
                    
                current_row += 1  # Tambah satu baris setelah form
        
        # for i,j in enumerate(self.rows[0]):
        #     print(i,j, type(j))

        # print(self.rows[0][9].cget("text").split(": ", 1)[1])

        for i in self.rows:
            print(i)
        # self.calculate()
        # print(self.manpower_total)

    # def calculate(self):
    #     for i in range(len(self.rows)):
    #         print(i)
    #         if self.rows[i][4] is not None:
    #             try:
    #                 for j in range(9, len(self.rows[i])+1, 8):
    #                     print(i,j,len(self.rows[i]), self.rows[i])
    #                     print(self.rows[i][j].cget("text").split(": ", 1)[1])
    #                     self.manpower_total+=self.rows[i][j].cget("text").split(": ", 1)[1]
    #                     print(self.manpower_total)
    #                     mp = self.rows[i][j].cget("text").split(": ", 1)[1]
    #                     # if mp != " " or mp != "":
    #                     #     print(mp, 'uhuy')
    #             except:
    #                 print("Apaan ini")
    #         else:
    #             print("gabener")



    def calculate_next_row(self, row_index):
        """Hitung baris berikutnya untuk menempatkan entri di bawah checkbox tertentu."""
        current_row = self.rows[row_index][0].grid_info()['row'] + 1
        for i in range(row_index + 1, len(self.rows)):
            if self.rows[i][2] is not None:
                current_row += 2  # Tambahkan dua baris untuk setiap form tambahan
        return current_row
    
    # def summary(self,what):
    #     if what == "tpp":


# Menjalankan aplikasi
root = tk.Tk()
app = MyApp(root)
root.mainloop()
