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

Window.size = (1200, 600)
screen_width, screen_height = Window.system_size  
Window.left = (screen_width - Window.width) // 2 

class ManpowerEstimator(App):
    def build(self):
        Window.maximize()

        self.height = 40
        self.width_1 = 250
        self.width_2 = 350
        self.spacing = 10
        self.padding = 10

        self.root = BoxLayout(orientation='vertical', padding=self.padding, spacing=self.spacing)
        self.title = 'Manpower Estimator'
        self.icon = "assets/timaslogo.ico"

        scroll_view = ScrollView(size_hint=(1, 1))

        self.main_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        self.main_layout.bind(minimum_height=self.main_layout.setter('height'))
        scroll_view.add_widget(self.main_layout)
        self.root.add_widget(scroll_view)

        self.footer_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=100, padding=(10, 0), spacing=self.spacing)
        
        input_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.height, spacing=self.spacing)
        input_layout.add_widget(Widget())
        self.salary_input = TextInput(hint_text="Avg Salary (Juta Rupiah)", multiline=False, size_hint=(None, None), width=self.width_1, height=self.height, write_tab = False)
        input_layout.add_widget(self.salary_input)
        self.profit_percentage = TextInput(hint_text="Profit Percentage (%)", multiline=False, size_hint=(None, None), width=self.width_1, height=self.height, write_tab = False)
        input_layout.add_widget(self.profit_percentage)
        input_layout.add_widget(Widget())
        self.footer_layout.add_widget(input_layout)

        finance_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.height, spacing=self.spacing)
        finance_layout.add_widget(Widget())
        self.sum_salary = Label(text="Sum Salary : Rp0", size_hint_y=None, height=self.height, size_hint_x = None, width = self.width_2)
        finance_layout.add_widget(self.sum_salary)
        self.revenue = Label(text="Revenue : Rp0", size_hint_y=None, height=self.height, size_hint_x = None, width = self.width_2)
        finance_layout.add_widget(self.revenue)
        self.profit = Label(text="Profit : Rp0", size_hint_y=None, height=self.height, size_hint_x = None, width = self.width_2)
        finance_layout.add_widget(self.profit)
        finance_layout.add_widget(Widget())
        self.footer_layout.add_widget(finance_layout)

        human_resource = BoxLayout(size_hint_y=None, height=self.height, padding=(10, 0), spacing=self.spacing)
        human_resource.add_widget(Widget())
        self.total_tpp = Label(text="Total Time/Person : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = self.width_2)
        human_resource.add_widget(self.total_tpp)
        self.total_manpower = Label(text="Total Manpower : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = self.width_2)
        human_resource.add_widget(self.total_manpower)
        self.total_people = Label(text="Total People : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = self.width_2)
        human_resource.add_widget(self.total_people)
        human_resource.add_widget(Widget())
        self.footer_layout.add_widget(human_resource)

        button_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=self.height)
        button_layout.add_widget(Widget())
        self.recalculate_button = Button(text="Recalculate", size_hint_y=None, size_hint_x = None, pos_hint = {"right" : 1}, halign = 'right', height = self.height, width = 130)
        self.recalculate_button.bind(on_press=self.recalculate)
        button_layout.add_widget(self.recalculate_button)
        self.compare_button = Button(text="Compare", size_hint_y=None, size_hint_x = None, pos_hint = {"right" : 1}, halign = 'right', height = self.height, width = 130)
        self.compare_button.bind(on_press=self.compare_footer)
        button_layout.add_widget(self.compare_button)
        self.reset_button = Button(text="Reset", size_hint_y=None, size_hint_x = None, pos_hint = {"right" : 1}, halign = 'right', height = self.height, width = 130)
        self.reset_button.bind(on_press=self.clear_comparison)
        button_layout.add_widget(self.reset_button)
        # self.clear_button = Button(text="Clear", size_hint_y=None, size_hint_x = None, pos_hint = {"right" : 1}, halign = 'right', height = self.height, width = 130)
        # self.clear_button.bind(on_press=self.clearall)
        # button_layout.add_widget(self.clear_button)
        button_layout.add_widget(Widget())
        self.footer_layout.add_widget(button_layout)

        self.previous_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.height, padding=(10, 0), spacing=self.spacing)
        self.footer_layout.add_widget(self.previous_layout)

        self.comparison_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=self.height, padding=(10, 0), spacing=self.spacing)
        self.footer_layout.add_widget(self.comparison_layout)

        auvi = BoxLayout(orientation='horizontal', size_hint_y=None, height=10, padding=(10, 0), spacing=self.spacing)
        auvi.add_widget(Widget())
        develoby = Label(text="TIMAS SUPLINDO • Developed by Auvi A", size_hint_y=None, height=10, size_hint_x = None, font_size = 10, halign = 'center')
        auvi.add_widget(develoby)
        auvi.add_widget(Widget())
        self.footer_layout.add_widget(auvi)

        self.bangtolingbangudahpusingbang = []
        self.tpps = []
        self.manpowers = []
        self.spm = []
        self.ts = []
        self.comparison = []
        self.comparison_ison = False

        self.add_checkbox_group("Mechanical", ["Static Equipment", "Rotatic Equipment", "Steel Structure"])
        self.add_checkbox_group("Piping", ["Carbon Steel", "Stainless Steel"])
        self.add_checkbox_group("Insulation", ["Hot Insulation", "Cold Insulation"])

        self.root.add_widget(self.footer_layout)
        return self.root

    def add_checkbox_group(self, label, sub_labels):
        group_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        group_layout.bind(minimum_height=group_layout.setter('height'))
        group_checkbox = CheckBox(size_hint_x=0.1)
        group_label = Label(text=label, size_hint_x=0.9, halign='left', valign='middle')
        group_label.bind(size=group_label.setter('text_size'))

        header_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=30)
        header_layout.add_widget(group_checkbox)
        header_layout.add_widget(group_label)
        group_layout.add_widget(header_layout)

        def on_checkbox_active(checkbox, value):
            if value: 
                for sub_label in sub_labels[::-1]:
                    self.add_input_row(group_layout, sub_label)
                    self.recalculate()
            else:
                widgets_to_remove = group_layout.children[:-1]
                for widget in widgets_to_remove:
                    group_layout.remove_widget(widget)
                self.recalculate()

        group_checkbox.bind(active=on_checkbox_active)
        self.main_layout.add_widget(group_layout)

    def add_input_row(self, group_layout, label_text):
        row_layout = GridLayout(cols=9, size_hint_y=None, height=self.height)

        row_layout.add_widget(Label(text=label_text, size_hint_y=None, height=self.height, size_hint_x = None, width = 150))

        qty_input = TextInput(hint_text="QTY", multiline=False, size_hint_y=None, height=self.height, size_hint_x = None, width = 100, write_tab = False)
        row_layout.add_widget(qty_input)

        uom_spinner = Spinner(text="Unit", values=["TON", "ID", "M2"], size_hint_y=None, height=self.height)
        row_layout.add_widget(uom_spinner)

        productivity_input = TextInput(hint_text="Productivity", multiline=False, size_hint_y=None, height=self.height, write_tab = False)
        row_layout.add_widget(productivity_input)

        duration_input = TextInput(hint_text="Duration (day)", multiline=False, size_hint_y=None, height=self.height, write_tab = False)
        row_layout.add_widget(duration_input)

        tpp_label = Label(text="Time/Person : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 200)
        row_layout.add_widget(tpp_label)

        manpower_label = Label(text="Manpower : 0", size_hint_y=None, height=self.height, size_hint_x = None, width = 150)
        row_layout.add_widget(manpower_label)

        salary_month_label = Label(text="Salary/Month : Rp0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        row_layout.add_widget(salary_month_label)

        total_salary_label = Label(text="Total Salary : Rp0", size_hint_y=None, height=self.height, size_hint_x = None, width = 350)
        row_layout.add_widget(total_salary_label)

        def calculate_result(*args):
            try:
                qty = float(qty_input.text) if qty_input.text else 0
                prod = float(productivity_input.text) if productivity_input.text else 1  # Default 1 jika kosong
                dur = float(duration_input.text) if duration_input.text else 1
                salary = float(self.salary_input.text) * 1_000_000 if self.salary_input.text else 1
                tpp = (qty / prod) if prod > 0 else 0
                manpower = (tpp / dur) if dur > 0 else 0
                salary_month = manpower * salary
                total_salary = salary_month/25*dur

                # Update label pada baris
                tpp_label.text = f"Time/Person : {tpp:.0f}"
                manpower_label.text = f"Manpower : {manpower:.0f}"
                salary_month_label.text = "Salary/Month : Rp{:,.0f}".format(salary_month)
                total_salary_label.text = "Total Salary : Rp{:,.0f}".format(total_salary)
                
            except ValueError:
                tpp_label.text = "Time/Person : 0"
                manpower_label.text = "Manpower : 0"
                salary_month_label.text = "Salary/Month : Rp0"
                total_salary_label.text = "Total Salary : Rp0"
            
            self.recalculate()
            
            # self.update_total()
        
        qty_input.bind(text=calculate_result)
        productivity_input.bind(text=calculate_result)
        duration_input.bind(text=calculate_result)
        self.salary_input.bind(text=calculate_result)
        self.profit_percentage.bind(text=calculate_result)

        group_layout.add_widget(row_layout, index=len(group_layout.children) - 1)

    def recalculate(self, instance = None):
        self.bangtolingbangudahpusingbang.clear()
        self.tpps.clear()
        self.manpowers.clear()
        self.ts.clear()
        self.spm.clear()
        for i in self.main_layout.children:
            for j in i.children :
                for k in j.children : 
                    for l in j.children : 
                        # print(f"{getattr(l, 'text', 'N/A')}")
                        self.bangtolingbangudahpusingbang.append(f"{getattr(l, 'text', 'N/A')}")
                    break

        for i in self.bangtolingbangudahpusingbang:
            if "Total Salary" in i :
                text = float(i.replace("Total Salary : Rp", "").replace(",",""))
                self.ts.append(text)
            if "Salary/Month" in i :
                text = float(i.replace("Salary/Month : Rp", "").replace(",",""))
                self.spm.append(text)
            if "Manpower" in i :
                text = int(i.replace("Manpower : ", ""))
                self.manpowers.append(text)
            if "Time/Person" in i:
                text = int(i.replace("Time/Person : ", ""))
                self.tpps.append(text)
        self.update_total()
    
    def update_total(self):
        total = 0
        manpower_total = 0
        sum_salary_total = 0

        for value in self.tpps:
            try:
                total += value
            except:
                pass
        self.total_tpp.text = f"Total Time/Person : {total:.0f}"

        for value in self.manpowers:
            try:
                manpower_total += value
            except:
                pass
        self.total_manpower.text = f"Total Manpower : {manpower_total:.0f}"

        for value in self.ts:
            try:
                sum_salary_total += value
            except:
                pass
        self.sum_salary.text = f"Sum salary : Rp{sum_salary_total:,.0f}"

        profit_percentage = (float(self.profit_percentage.text)*0.01) if self.profit_percentage.text else 0
        revenue = sum_salary_total * (1 + profit_percentage)
        profit_total = sum_salary_total*profit_percentage

        mp = int(self.total_manpower.text.replace("Total Manpower : ",""))
        self.revenue.text = "Revenue : Rp{:,.0f}".format(revenue)
        self.profit.text = "Profit : Rp{:,.0f}".format(profit_total)
        self.total_people.text = f"Total People : {mp*1.40:.0f}"

        self.compared(sum_salary_total, revenue, profit_total, mp*1.40)

    def compare_footer(self, instance):
        self.comparison_ison = True
        self.previous_layout.clear_widgets()
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
        
        snapshot_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, padding=(10, 0), spacing=10)
        snapshot_layout.add_widget(Label(text=f"[Previous] {snapshot['total_salary']}"))
        snapshot_layout.add_widget(Label(text=f"[Previous] {snapshot['revenue']}"))
        snapshot_layout.add_widget(Label(text=f"[Previous] {snapshot['profit']}"))
        snapshot_layout.add_widget(Label(text=f"[Previous] {snapshot['total_people']}"))
        
        self.previous_layout.add_widget(snapshot_layout, index=0)

    def clear_comparison(self, instance):
        self.comparison_layout.clear_widgets()
        self.comparison.clear()
        self.previous_layout.clear_widgets()
        self.comparison_ison = False

    def compared(self, sumsal, rev, prof, totpeo):
        if self.comparison_ison is True :
            self.comparison_layout.clear_widgets()
            self.comparison[0] = self.comparison[0].replace("Sum salary : Rp", "").replace(",","")
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

            self.comparison_layout.add_widget(Label(text=f"[Comparison] Profit Surplus Rp{compare_sumsalary:,.0f}"))
            # self.compare.add_widget(Label(text=f"[Difference] Revenue Rp{compare_revenue:,.0f}"))
            self.comparison_layout.add_widget(Label(text=f"[Comparison] Profit Total Rp{compare_profit:,.0f}"))
            self.comparison_layout.add_widget(Label(text=f"[Comparison] Total People {compare_totalpeople:,.0f}"))    


if __name__ == '__main__':
    ManpowerEstimator().run()

#EoL
#pyinstaller --onedir --noconsole --add-data 'assets/timaslogo.ico;assets' --name "Manpower Estimator" cleani