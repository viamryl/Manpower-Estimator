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
from kivy.uix.widget import Widget
import locale

locale.setlocale(locale.LC_ALL, '')
# Set ukuran jendela
Window.size = (1200, 600)

screen_width, screen_height = Window.system_size  # Ukuran layar sistem
Window.left = (screen_width - Window.width) // 2  # Posisi tengah horizontal

# class TabTextInput(TextInput):

#     def __init__(self, *args, **kwargs):
#         self.next = kwargs.pop('next', None)
#         super(TabTextInput, self).__init__(*args, **kwargs)

#     def set_next(self, next):
#         self.next = next

#     def _keyboard_on_key_down(self, window, keycode, text, modifiers):
#         key, key_str = keycode
#         if key in (9, 13) and self.next is not None:
#             self.next.focus = True
#             self.next.select_all()
#         else:
#             super(TabTextInput, self)._keyboard_on_key_down(window, keycode, text, modifiers)

class ManpowerCalculatorApp(App):
    def build(self):
        Window.maximize()

        self.root = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.title = 'Manpower Estimator'

        # Bungkus GridLayout dalam ScrollView
        scroll_view = ScrollView(size_hint=(1, 1))

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
        input_layout0 = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)

        input_layout0.add_widget(Widget())

        # TextInput pertama dengan lebar 250
        self.salary_input = TextInput(hint_text="Avg Salary (Juta Rupiah)", multiline=False, size_hint=(None, None), width=250, height=40, write_tab = False)
        input_layout0.add_widget(self.salary_input)

        # TextInput kedua dengan lebar 250
        self.profit_percentage = TextInput(hint_text="Profit Percentage (%)", multiline=False, size_hint=(None, None), width=250, height=40, write_tab = False)
        input_layout0.add_widget(self.profit_percentage)

        input_layout0.add_widget(Widget())

        input_layout.add_widget(Widget())

        # Label total salary
        self.sum_salary = Label(text="Sum Salary : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        self.sum_salary.bind(size=self.sum_salary.setter('text_size'))
        input_layout.add_widget(self.sum_salary)

        self.revenue = Label(text="Revenue : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        self.revenue.bind(size=self.revenue.setter('text_size'))
        input_layout.add_widget(self.revenue)

        self.profit = Label(text="Profit : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        self.profit.bind(size=self.profit.setter('text_size'))
        input_layout.add_widget(self.profit)

        input_layout.add_widget(Widget())

        # Menambahkan input_layout ke footer_layout
        self.footer_layout.add_widget(input_layout0)
        self.footer_layout.add_widget(input_layout)

        # Baris kedua footer: Layout untuk total TPP dan Manpower
        self.footer_sub_layout = BoxLayout(size_hint_y=None, height=50, padding=(10, 0), spacing=10)

        self.footer_sub_layout.add_widget(Widget())

        self.total_tpp = Label(text="Total Time/Person: 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        self.total_tpp.bind(size=self.total_tpp.setter('text_size'))
        self.footer_sub_layout.add_widget(self.total_tpp)

        self.total_manpower = Label(text="Total Manpower : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        self.total_manpower.bind(size=self.total_manpower.setter('text_size'))
        self.footer_sub_layout.add_widget(self.total_manpower)

        self.total_people = Label(text="Total People : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        self.total_people.bind(size=self.total_people.setter('text_size'))
        self.footer_sub_layout.add_widget(self.total_people)

        self.footer_sub_layout.add_widget(Widget())

        self.footer_layout.add_widget(self.footer_sub_layout)
        
        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=40)
        self.compare_button = Button(text="Compare", size_hint_y=None, size_hint_x = None, pos_hint = {"right" : 1}, halign = 'right', height = 40, width = 130)
        self.compare_button.bind(on_press=self.compare_footer)
        self.reset_button = Button(text="Reset", size_hint_y=None, size_hint_x = None, pos_hint = {"right" : 1}, halign = 'right', height = 40, width = 120)
        self.reset_button.bind(on_press=self.clear_comparison)
        
        button_layout.add_widget(Widget())
        button_layout.add_widget(self.compare_button)
        button_layout.add_widget(self.reset_button)
        button_layout.add_widget(Widget())

        self.root.add_widget(self.footer_layout)
        self.root.add_widget(button_layout)

        self.comparison_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 0), spacing=10)
        self.root.add_widget(self.comparison_layout)

        self.compare = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 0), spacing=10)
        self.root.add_widget(self.compare)

        # List untuk menyimpan referensi ke setiap label hasil
        self.tpps = []
        self.tms =[]
        self.spm = []
        self.ts = []
        self.comparison = []

        self.comparison_ison = False

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
                # print("Calculate Result Triggered")
                # print(f"QTY: {qty_input.text}, Productivity: {productivity_input.text}, Duration: {duration_input.text}")
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
        profit_percentage = (float(self.profit_percentage.text)*0.01) if self.profit_percentage.text else 0
        revenue = sum_salary_total * (1 + profit_percentage)
        profit_total = sum_salary_total*profit_percentage

        mp = int(self.total_manpower.text.replace("Total Manpower: ",""))
        self.revenue.text = "Revenue : Rp{:,.0f}".format(revenue)
        self.profit.text = "Profit : Rp{:,.0f}".format(profit_total)
        self.total_people.text = f"Total People : {mp*1.40:.0f}"

        self.compared(sum_salary_total, revenue, profit_total, mp*1.40)


    def clear_comparison(self, instance):
        self.comparison_layout.clear_widgets()
        self.comparison.clear()
        self.compare.clear_widgets()
        self.comparison_ison = False

    def compare_footer(self, instance):
        # Simpan nilai footer saat ini
        self.comparison_ison = True
        self.comparison_layout.clear_widgets()
        snapshot = {
            "total_salary": self.sum_salary.text,
            "revenue": self.revenue.text,
            "profit": self.profit.text,
            "total_people": self.total_people.text
        }

        self.comparison.append(self.sum_salary.text)
        self.comparison.append(self.revenue.text)
        self.comparison.append(self.profit.text)
        self.comparison.append(self.total_people.text)
        
        # Tampilkan snapshot di atas footer utama
        snapshot_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 0), spacing=10)
        snapshot_layout.add_widget(Label(text=f"[Previous] {snapshot['total_salary']}"))
        snapshot_layout.add_widget(Label(text=f"[Previous] {snapshot['revenue']}"))
        snapshot_layout.add_widget(Label(text=f"[Previous] {snapshot['profit']}"))
        snapshot_layout.add_widget(Label(text=f"[Previous] {snapshot['total_people']}"))
        
        self.comparison_layout.add_widget(snapshot_layout, index=0)
        # print(self.comparison_layout)

    def compared(self, sumsal, rev, prof, totpeo):
        if self.comparison_ison is True :
            self.compare.clear_widgets()
            self.comparison[0] = self.comparison[0].replace("Sum Salary : Rp", "").replace(",","")
            self.comparison[1] = self.comparison[1].replace("Revenue : Rp", "").replace(",","")
            self.comparison[2] = self.comparison[2].replace("Profit : Rp", "").replace(",","")
            self.comparison[3] = self.comparison[3].replace("Total People : ", "").replace(",","")

            
            pre_sumsalary = int(self.comparison[0])
            pre_revenue = int(self.comparison[1])
            pre_profit = int(self.comparison[2])
            pre_totalpeople = int(self.comparison[3])

            compare_sumsalary = pre_sumsalary - sumsal
            # compare_revenue = pre_revenue - rev
            compare_profit = pre_revenue - sumsal
            compare_totalpeople = pre_totalpeople - totpeo

            self.compare.add_widget(Label(text=f"[Difference] Salary Rp{compare_sumsalary:,.0f}"))
            # self.compare.add_widget(Label(text=f"[Difference] Revenue Rp{compare_revenue:,.0f}"))
            self.compare.add_widget(Label(text=f"[Difference] Profit Rp{compare_profit:,.0f}"))
            self.compare.add_widget(Label(text=f"[Difference] Total People {compare_totalpeople:,.0f}"))


if __name__ == '__main__':
    ManpowerCalculatorApp().run()
