from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.popup import Popup
from kivy.uix.actionbar import ActionBar, ActionView, ActionPrevious, ActionButton
from tkinter import Tk, filedialog
import json
import os
import locale

locale.setlocale(locale.LC_ALL, '')
# Set ukuran jendela
Window.size = (1200, 600)

screen_width, screen_height = Window.system_size  # Ukuran layar sistem
Window.left = (screen_width - Window.width) // 2  # Posisi tengah horizontal

class TabTextInput(TextInput):

    def __init__(self, *args, **kwargs):
        self.next = kwargs.pop('next', None)
        super(TabTextInput, self).__init__(*args, **kwargs)

    def set_next(self, next):
        self.next = next

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        key, key_str = keycode
        if key in (9, 13) and self.next is not None:
            self.next.focus = True
            self.next.select_all()
        else:
            super(TabTextInput, self)._keyboard_on_key_down(window, keycode, text, modifiers)

class ManpowerCalculatorApp(App):
    def build(self):
        Window.maximize()

        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.title = 'Manpower Estimator'

        # Bungkus GridLayout dalam ScrollView
        scroll_view = ScrollView(size_hint=(1, 1))

        # ** MENU BAR **
        self.menu_bar = ActionBar()
        action_view = ActionView()
        action_view.add_widget(ActionPrevious(title="Manpower Estimator", with_previous=False))

        # Tombol Save
        save_button = ActionButton(text="Save As")
        save_button.bind(on_release=self.show_save_dialog)
        action_view.add_widget(save_button)

        # Tombol Load
        load_button = ActionButton(text="Load File")
        load_button.bind(on_release=self.show_load_dialog)
        action_view.add_widget(load_button)

        self.menu_bar.add_widget(action_view)

        # Tambahkan menu bar ke root layout
        self.root.add_widget(self.menu_bar)


        # GridLayout untuk tabel utama
        self.main_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))

        # Tambahkan checkbox group
        self.add_checkbox_group("Mechanical", ["Static Equipment", "Rotatic Equipment", "Steel Structure"])
        self.add_checkbox_group("Piping", ["Carbon Steel", "Stainless Steel"])
        self.add_checkbox_group("Insulation", ["Hot Insulation", "Cold Insulation"])

        # Tambahkan GridLayout ke ScrollView
        scroll_view.add_widget(self.main_layout)

        self.height = 40

        # Tambahkan ScrollView ke layout utama
        self.root.add_widget(scroll_view)

        # Footer untuk menampilkan total
        self.footer_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=(10, 0), spacing=10)

        # Baris pertama footer: TextInput untuk perhitungan matematika
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        # TextInput pertama dengan lebar 250
        self.salary_input = TextInput(hint_text="Avg Salary (Juta Rupiah)", multiline=False, size_hint=(None, None), width=220, height=40, write_tab = False)
        input_layout.add_widget(self.salary_input)

        # TextInput kedua dengan lebar 250
        self.profit_percentage = TextInput(hint_text="Profit Percentage (0.0 - 1.0)", multiline=False, size_hint=(None, None), width=250, height=40, write_tab = False)
        input_layout.add_widget(self.profit_percentage)

        # Label total salary
        self.sum_salary = Label(text="Sum Salary : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350, halign='left')
        self.sum_salary.bind(size=self.sum_salary.setter('text_size'))
        input_layout.add_widget(self.sum_salary)

        self.revenue = Label(text="Revenue : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350, halign='left')
        self.revenue.bind(size=self.revenue.setter('text_size'))
        input_layout.add_widget(self.revenue)

        self.profit = Label(text="Profit : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350, halign='left')
        self.profit.bind(size=self.profit.setter('text_size'))
        input_layout.add_widget(self.profit)

        # Menambahkan input_layout ke footer_layout
        self.footer_layout.add_widget(input_layout)

        # Baris kedua footer: Layout untuk total TPP dan Manpower
        self.footer_sub_layout = BoxLayout(size_hint_y=None, height=50, padding=(10, 0), spacing=10)

        self.total_tpp = Label(text="Total Time/Person: 0", size_hint_x=None, halign='left', valign='middle', width =300)
        self.total_tpp.bind(size=self.total_tpp.setter('text_size'))
        self.footer_sub_layout.add_widget(self.total_tpp)

        self.total_manpower = Label(text="Total Manpower : 0", size_hint_x=None, halign='left', valign='middle', width = 300)
        self.total_manpower.bind(size=self.total_manpower.setter('text_size'))
        self.footer_sub_layout.add_widget(self.total_manpower)

        self.total_people = Label(text="Total People : 0", size_hint_x=None, halign='left', valign='middle', width = 300)
        self.total_people.bind(size=self.total_people.setter('text_size'))
        self.footer_sub_layout.add_widget(self.total_people)

        self.footer_layout.add_widget(self.footer_sub_layout)
        
        self.root.add_widget(self.footer_layout)

        # self.root.add_widget(self.footer_layout)

        # List untuk menyimpan referensi ke setiap label hasil
        self.tpps = []
        self.tms =[]
        self.spm = []
        self.ts = []

        return self.root

    def add_checkbox_group(self, label, sub_labels):
        # Layout vertikal untuk setiap grup (checkbox + input)
        group_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        group_layout.bind(minimum_height=group_layout.setter('height'))

        # Checkbox utama
        group_checkbox = CheckBox(size_hint_x=0.1)
        group_label = Label(text=label, size_hint_x=0.9, halign='left', valign='middle')
        group_label.bind(size=group_label.setter('text_size'))

        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        header_layout.add_widget(group_checkbox)
        header_layout.add_widget(group_label)

        # Tambahkan header ke grup
        group_layout.add_widget(header_layout)

        # Fungsi untuk menambahkan atau menghapus input baris
        def on_checkbox_active(checkbox, value):
            if value:  # Jika dicentang
                for sub_label in sub_labels[::-1]:
                    self.add_input_row(group_layout, sub_label)
            else:  # Jika tidak dicentang
                # Hanya sisakan header layout
                widgets_to_remove = group_layout.children[:-1]
                for widget in widgets_to_remove:
                    group_layout.remove_widget(widget)

        group_checkbox.bind(active=on_checkbox_active)
        self.main_layout.add_widget(group_layout)

    def add_input_row(self, group_layout, label_text):
        # Layout untuk setiap baris input
        row_layout = GridLayout(cols=9, size_hint_y=None, height=self.height)

        # Kolom label deskripsi
        row_layout.add_widget(Label(text=label_text, size_hint_y=None, height=self.height, size_hint_x = None, width = 150))

        # Kolom QTY
        qty_input = TextInput(hint_text="QTY", multiline=False, size_hint_y=None, height=self.height, size_hint_x = None, width = 100, write_tab = False)
        row_layout.add_widget(qty_input)

        # Kolom UOM
        uom_spinner = Spinner(text="Unit", values=["TON", "ID", "M2"], size_hint_y=None, height=self.height)
        row_layout.add_widget(uom_spinner)

        # Kolom Productivity
        productivity_input = TextInput(hint_text="Productivity", multiline=False, size_hint_y=None, height=self.height, write_tab = False)
        row_layout.add_widget(productivity_input)

        # Kolom Duration
        duration_input = TextInput(hint_text="Duration (day)", multiline=False, size_hint_y=None, height=self.height, write_tab = False)
        row_layout.add_widget(duration_input)

        # Kolom untuk hasil operasi matematika
        tpp_label = Label(text="Time/Person: 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 200)
        row_layout.add_widget(tpp_label)

        manpower_label = Label(text="Manpower : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 150)
        row_layout.add_widget(manpower_label)

        salary_month_label = Label(text="Salary/Month : Rp0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        row_layout.add_widget(salary_month_label)

        total_salary_label = Label(text="Total Salary : Rp0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        row_layout.add_widget(total_salary_label)

        # Tambahkan label hasil ke daftar untuk total
        self.tpps.append(tpp_label)
        self.tms.append(manpower_label)
        self.ts.append(total_salary_label)
        self.spm.append(salary_month_label)

        # Fungsi untuk menghitung hasil secara real-time
        def calculate_result(*args):
            try:
                print("Calculate Result Triggered")
                print(f"QTY: {qty_input.text}, Productivity: {productivity_input.text}, Duration: {duration_input.text}")
                qty = float(qty_input.text) if qty_input.text else 0
                prod = float(productivity_input.text) if productivity_input.text else 1  # Default 1 jika kosong
                dur = float(duration_input.text) if duration_input.text else 1
                salary = float(self.salary_input.text) * 1_000_000 if self.salary_input.text else 1
                result = (qty / prod) if prod > 0 else 0
                manpower = (result / dur) if dur > 0 else 0
                salary_month = manpower * salary
                total_salary = salary_month/25*dur

                # Update label pada baris
                tpp_label.text = f"Time/Person: {result:.0f}"
                manpower_label.text = f"Manpower : {manpower:.0f}"
                salary_month_label.text = "Salary/Month : Rp{:,.0f}".format(salary_month)
                total_salary_label.text = "Total Salary : Rp{:,.0f}".format(total_salary)
                
            except ValueError:
                tpp_label.text = "Time/Person: 0"
                manpower_label.text = "Manpower : 0"
                salary_month_label.text = "Salary/Month : Rp0"
                total_salary_label.text = "Total Salary : Rp0"

            # Panggil update total untuk merekap semua nilai
            self.update_total()


        # Bind setiap input ke fungsi perhitungan
        qty_input.bind(text=calculate_result)
        productivity_input.bind(text=calculate_result)
        duration_input.bind(text=calculate_result)
        self.salary_input.bind(text=calculate_result)
        self.profit_percentage.bind(text=calculate_result)

        # Tambahkan baris baru ke group_layout (di bawah checkbox)
        group_layout.add_widget(row_layout, index=len(group_layout.children) - 1)

    def update_total(self):
        total = 0
        manpower_total = 0
        sum_salary_total = 0

        # Total Time/Person
        for label in self.tpps:
            try:
                result_text = label.text.replace("Time/Person: ", "")
                total += float(result_text)
            except ValueError:
                pass
        self.total_tpp.text = f"Total Time/Person: {total:.0f}"

        # Total Manpower
        for label in self.tms:
            try:
                manpower_text = label.text.replace("Manpower : ", "")
                manpower_total += float(manpower_text)
            except ValueError:
                pass
        self.total_manpower.text = f"Total Manpower: {manpower_total:.0f}"

        # Total Salary
        for label in self.ts:
            try:
                sum_salary_text = label.text.replace("Total Salary : Rp", "").replace(",", "")
                sum_salary_total += float(sum_salary_text)
            except ValueError:
                pass
        self.sum_salary.text = "Sum Salary : Rp{:,.0f}".format(sum_salary_total)

        # Calculate Revenue
        profit_percentage = float(self.profit_percentage.text) if self.profit_percentage.text else 0
        revenue = sum_salary_total * (1 + profit_percentage)
        profit_total = sum_salary_total*profit_percentage

        mp = int(self.total_manpower.text.replace("Total Manpower: ",""))
        self.revenue.text = "Revenue : Rp{:,.0f}".format(revenue)
        self.profit.text = "Profit : Rp{:,.0f}".format(profit_total)
        self.total_people.text = f"Total People : {mp*1.40:.0f}"
        
    def show_save_dialog(self, instance):
        """Menampilkan dialog save file khas Windows"""
        Tk().withdraw()  # Sembunyikan jendela utama Tkinter
        file_path = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            self.save_data(file_path)

    def show_load_dialog(self, instance):
        """Menampilkan dialog open file khas Windows"""
        Tk().withdraw()
        file_path = filedialog.askopenfilename(
            filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")]
        )
        if file_path:
            self.load_data(file_path)

    def save_data(self, file_path):
        """Menyimpan semua data input ke dalam file JSON"""
        data = {
            "salary_input": self.salary_input.text,
            "profit_percentage": self.profit_percentage.text,
            "rows": []
        }
        
        for group in self.main_layout.children:
            if isinstance(group, BoxLayout):
                for row in group.children:
                    if isinstance(row, GridLayout) and len(row.children) == 9:
                        row_data = {
                            "label": row.children[8].text,  # Label deskripsi
                            "qty": row.children[7].text,
                            "uom": row.children[6].text,
                            "productivity": row.children[5].text,
                            "duration": row.children[4].text,
                            "tpp": row.children[3].text,
                            "manpower": row.children[2].text,
                            "salary_month": row.children[1].text,
                            "total_salary": row.children[0].text
                        }
                        data["rows"].append(row_data)
        
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)
        
        print(f"Data saved successfully at {file_path}")


    def load_data(self, file_path):
        """Memuat data dari file JSON dan memperbarui UI"""
        try:
            with open(file_path, "r") as file:
                data = json.load(file)
            
            # Muat nilai global
            self.salary_input.text = data.get("salary_input", "")
            self.profit_percentage.text = data.get("profit_percentage", "")
            
            # Bersihkan layout utama sebelum memuat data baru
            for group in self.main_layout.children[:]:
                if isinstance(group, BoxLayout):
                    self.main_layout.remove_widget(group)
            
            # Tambahkan kembali data dari file
            for row_data in data.get("rows", []):
                group_layout = BoxLayout(orientation='vertical', size_hint_y=None)
                self.main_layout.add_widget(group_layout)
                
                self.add_input_row(group_layout, row_data["label"])
                row = group_layout.children[0]
                
                row.children[7].text = row_data.get("qty", "")
                row.children[6].text = row_data.get("uom", "Unit")
                row.children[5].text = row_data.get("productivity", "")
                row.children[4].text = row_data.get("duration", "")
                row.children[3].text = row_data.get("tpp", "Time/Person: 0")
                row.children[2].text = row_data.get("manpower", "Manpower : 0")
                row.children[1].text = row_data.get("salary_month", "Salary/Month : Rp0")
                row.children[0].text = row_data.get("total_salary", "Total Salary : Rp0")
            
            print("Data loaded successfully.")
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Failed to load data: {e}")

        

if __name__ == '__main__':
    ManpowerCalculatorApp().run()
