from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.spinner import Spinner
from kivy.core.window import Window

Window.size = (400, 700)

class StressAnalyzerApp(App):
    def build(self):
        # ========== داده‌های ذخیره‌شده (داده‌های واقعی شما) ==========
        self.data = {
            'POD': {'کنترل': 107.22, 'تنش 5%': 0.115, 'تنش 10%': 0.081, 'تنش 15%': 0.029},
            'SOD': {'کنترل': 0.190, 'تنش 5%': 0.092, 'تنش 10%': 0.097, 'تنش 15%': 0.099},
            'CAT': {'کنترل': 0.129, 'تنش 5%': 0.217, 'تنش 10%': 0.067, 'تنش 15%': 0.149},
            'Proline': {'کنترل': 5.700, 'تنش 5%': 24.053, 'تنش 10%': 29.176, 'تنش 15%': 21.270},
            'FlavonoidT': {'کنترل': 107.22, 'تنش 5%': 237.1, 'تنش 10%': 120.41, 'تنش 15%': 205.36},
            'PhenolT': {'کنترل': 63.301, 'تنش 5%': 177.496, 'تنش 10%': 94.27, 'تنش 15%': 155.11}
        }
        
        # ========== ساخت تب‌ها ==========
        tab_panel = TabbedPanel(size_hint=(1, 1))
        
        # ---------- تب 1: تحلیل تکی ----------
        tab1 = TabbedPanelItem(text='🔬 تحلیل تکی')
        layout1 = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout1.add_widget(Label(text='تحلیل یک شاخص (با چند تکرار)', font_size=18, size_hint_y=None, height=40))
        layout1.add_widget(Label(text='شاخص را انتخاب کن:', size_hint_y=None, height=25))
        
        self.spinner = Spinner(
            text='POD',
            values=list(self.data.keys()),
            size_hint=(1, None),
            height=45
        )
        layout1.add_widget(self.spinner)
        
        layout1.add_widget(Label(text='مقادیر تکرارها را وارد کن:', size_hint_y=None, height=25))
        
        self.inputs_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=5)
        self.inputs_layout.bind(minimum_height=self.inputs_layout.setter('height'))
        self.input_fields = []
        
        btn_layout = BoxLayout(size_hint_y=None, height=50, spacing=10)
        add_btn = Button(text='➕ افزودن تکرار')
        add_btn.bind(on_press=self.add_input_field)
        remove_btn = Button(text='➖ حذف آخرین')
        remove_btn.bind(on_press=self.remove_input_field)
        btn_layout.add_widget(add_btn)
        btn_layout.add_widget(remove_btn)
        
        self.add_input_field(None)
        
        layout1.add_widget(self.inputs_layout)
        layout1.add_widget(btn_layout)
        
        analyze_btn = Button(text='📊 تحلیل و مقایسه', size_hint_y=None, height=50)
        analyze_btn.bind(on_press=self.analyze_single)
        layout1.add_widget(analyze_btn)
        
        self.single_result = Label(text='نتیجه تحلیل اینجا نمایش داده میشود', halign='left', valign='top', size_hint_y=None)
        self.single_result.bind(texture_size=self.single_result.setter('size'))
        scroll1 = ScrollView(size_hint=(1, 0.4))
        scroll1.add_widget(self.single_result)
        layout1.add_widget(scroll1)
        
        tab1.add_widget(layout1)
        
        # ---------- تب 2: تحلیل گروهی ----------
        tab2 = TabbedPanelItem(text='📊 تحلیل گروهی')
        layout2 = BoxLayout(orientation='vertical', padding=15, spacing=10)
        
        layout2.add_widget(Label(text='تحلیل همه شاخص‌ها (هرکدام چند تکرار)', font_size=16, size_hint_y=None, height=40))
        
        self.group_grid = GridLayout(cols=2, spacing=10, size_hint_y=None)
        self.group_grid.bind(minimum_height=self.group_grid.setter('height'))
        self.group_fields = {}
        
        for param in self.data.keys():
            self.group_grid.add_widget(Label(text=f'{param}:', size_hint_y=None, height=35))
            field_box = BoxLayout(orientation='vertical', size_hint_y=None, height=120, spacing=5)
            fields = []
            for i in range(2):
                inp = TextInput(hint_text=f'تکرار {i+1}', multiline=False, input_filter='float', size_hint_y=None, height=35)
                field_box.add_widget(inp)
                fields.append(inp)
            add_field_btn = Button(text='➕', size_hint_y=None, height=30, width=40)
            add_field_btn.bind(on_press=lambda btn, p=param: self.add_group_replicate(p))
            field_box.add_widget(add_field_btn)
            self.group_grid.add_widget(field_box)
            self.group_fields[param] = fields
        
        scroll2 = ScrollView(size_hint=(1, 0.6))
        scroll2.add_widget(self.group_grid)
        layout2.add_widget(scroll2)
        
        group_analyze_btn = Button(text='📊 تحلیل همه شاخص‌ها', size_hint_y=None, height=50)
        group_analyze_btn.bind(on_press=self.analyze_group)
        layout2.add_widget(group_analyze_btn)
        
        self.group_result = Label(text='نتیجه تحلیل گروهی اینجا نمایش داده میشود', halign='left', valign='top', size_hint_y=None)
        self.group_result.bind(texture_size=self.group_result.setter('size'))
        scroll3 = ScrollView(size_hint=(1, 0.3))
        scroll3.add_widget(self.group_result)
        layout2.add_widget(scroll3)
        
        tab2.add_widget(layout2)
        
        tab_panel.add_widget(tab1)
        tab_panel.add_widget(tab2)
        
        return tab_panel
    
    # ========== توابع تب 1 ==========
    def add_input_field(self, instance):
        inp = TextInput(hint_text=f'تکرار {len(self.input_fields)+1}', multiline=False, 
                        input_filter='float', size_hint_y=None, height=35)
        self.input_fields.append(inp)
        self.inputs_layout.add_widget(inp)
        self.inputs_layout.height = len(self.input_fields) * 40
    
    def remove_input_field(self, instance):
        if len(self.input_fields) > 1:
            last = self.input_fields.pop()
            self.inputs_layout.remove_widget(last)
            self.inputs_layout.height = len(self.input_fields) * 40
    
    def analyze_single(self, instance):
        try:
            param = self.spinner.text
            values = []
            for inp in self.input_fields:
                if inp.text.strip():
                    values.append(float(inp.text))
            
            if not values:
                self.single_result.text = '⚠️ حداقل یک مقدار معتبر وارد کن!'
                return
            
            avg_value = sum(values) / len(values)
            stored = self.data[param]
            
            closest_level = min(stored.keys(), key=lambda k: abs(stored[k] - avg_value))
            closest_value = stored[closest_level]
            control_value = stored['کنترل']
            diff = avg_value - control_value
            
            if closest_level == 'کنترل':
                stress_status = '✅ وضعیت نرمال (کنترل)'
            elif '5%' in closest_level:
                stress_status = '🌱 تنش ملایم (5%)'
            elif '10%' in closest_level:
                stress_status = '🌿 تنش متوسط (10%)'
            else:
                stress_status = '⚡ تنش شدید (15%)'
            
            result = f'📌 شاخص: {param}\n'
            result += f'🔹 تعداد تکرارها: {len(values)}\n'
            result += f'🔸 مقادیر واردشده: {", ".join([str(v) for v in values])}\n'
            result += f'📊 میانگین محاسبهشده: {avg_value:.3f}\n'
            result += f'🎯 نزدیک‌ترین سطح تنش: {closest_level} (مقدار {closest_value})\n'
            result += f'📈 اختلاف با کنترل: {diff:+.3f}\n'
            result += f'🔰 {stress_status}\n\n'
            result += '📋 جدول مقادیر ذخیرهشده:\n'
            for level, value in stored.items():
                result += f'   {level}: {value}\n'
            
            self.single_result.text = result
            
        except ValueError:
            self.single_result.text = '❌ لطفاً فقط اعداد معتبر وارد کن!'
        except Exception as e:
            self.single_result.text = f'⚠️ خطا: {str(e)}'
    
    # ========== توابع تب 2 ==========
    def add_group_replicate(self, param):
        for child in self.group_grid.children:
            if isinstance(child, BoxLayout):
                fields = [c for c in child.children if isinstance(c, TextInput)]
                if len(fields) >= 5:
                    break
                if len(fields) > 0 and fields[0].hint_text.startswith(param):
                    new_inp = TextInput(hint_text=f'{param} تکرار جدید', multiline=False, 
                                       input_filter='float', size_hint_y=None, height=35)
                    child.add_widget(new_inp, index=len(child.children)-1)
                    self.group_fields[param].append(new_inp)
                    break
    
    def analyze_group(self, instance):
        try:
            all_results = []
            total_diff = 0
            valid_count = 0
            
            for param, fields in self.group_fields.items():
                values = []
                for inp in fields:
                    if inp.text.strip():
                        values.append(float(inp.text))
                
                if not values:
                    all_results.append(f'{param}: ⚠️ مقداری وارد نشده')
                    continue
                
                avg_value = sum(values) / len(values)
                stored = self.data[param]
                
                closest_level = min(stored.keys(), key=lambda k: abs(stored[k] - avg_value))
                control_value = stored['کنترل']
                diff = avg_value - control_value
                
                total_diff += diff
                valid_count += 1
                
                all_results.append(f'{param}: میانگین {avg_value:.3f} → نزدیک‌ترین {closest_level} (اختلاف {diff:+.3f})')
            
            if valid_count == 0:
                self.group_result.text = '⚠️ هیچ مقدار معتبری وارد نشده!'
                return
            
            avg_diff = total_diff / valid_count
            
            final_result = '📊 نتیجه کلی:\n'
            final_result += f'میانگین اختلاف همه شاخص‌ها با کنترل: {avg_diff:+.3f}\n'
            if avg_diff > 1:
                final_result += '⚡ وضعیت کلی: تنش شدید\n'
            elif avg_diff > 0.3:
                final_result += '🌿 وضعیت کلی: تنش متوسط\n'
            else:
                final_result += '✅ وضعیت کلی: نرمال (نزدیک به کنترل)\n\n'
            
            final_result += '📋 جزئیات:\n'
            final_result += '\n'.join(all_results)
            
            self.group_result.text = final_result
            
        except ValueError:
            self.group_result.text = '❌ لطفاً فقط اعداد معتبر وارد کن!'
        except Exception as e:
            self.group_result.text = f'⚠️ خطا: {str(e)}'

if __name__ == '__main__':
    StressAnalyzerApp().run()
