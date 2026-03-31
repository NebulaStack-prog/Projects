import tkinter as tk
from tkinter import font, ttk, messagebox
import math
import json
import os
from typing import Union
import matplotlib.pyplot as plt
import numpy as np

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("1200x800")

        self.button_formulas = {
            "Сложение": "a + b",
            "Вычитание": "a - b",
            "Умножение": "a × b",
            "Деление": "a : b",
            "Степень": "aᵇ",
            "Корень числа": "√a",
            "Факториал": "a! = 1 × ... × a",
            "Дв-й Факториал": "a!! = ×Чет/Нечет",
            "Простое?": "Простое?",
            "Множители": "a = b1 × ... × bn",
            "НОК": "НОК a и b",
            "НОД": "НОД a и b",
            "Синус": "sin(a)",
            "Косинус": "cos(a)",
            "Тангенс": "tg(a)",
            "Котангенс": "ctg(a)",
            "° → rad": "° → rad",
            "rad → °": "rad → °",
            "Уравнение Х": "ax + b = 0",
            "Уравнение Х²": "ax² + bx + c = 0",
            "Логарифм": "logₐb",
            "Модуль": "|a|",
            "Дробная Часть": "{a}",
            "Целая Часть": "[a]",
            "Прямая": "y = ax + b",
            "Парабола": "y = ax² + bx + c",
            "Гипербола": "y = a / (x + b) + c",
            "Синусоида": "y = a×sin(x) + b",
            "Косинусоида": "y = a×cos(x) + b",
            "Тангенсоида": "y = a×tg(x) + b",
            "Окружность": "(y-a)² + (x-b)² = c²",
            "Модуль Х": "y = a|x| + b",
            "Модуль Y": "|y| = ax + b",
            "Модуль Y и Х": "|y| = a|x| + b",
            "Котангенсоида": "y = a×ctg(x) + b",
            "Сердце": "Подарок от NS"
        }

        self.colors = {
            'bg': '#0a0a0f',
            'surface': '#151522',
            'card': '#1e1e2e',
            'primary': '#7c3aed',
            'secondary': '#06b6d4',
            'accent': '#10b981',
            'text': '#e2e8f0',
            'text_light': '#94a3b8',
            'danger': '#ef4444',
            'warning': '#f59e0b',
            'border': '#2d3748'
        }

        self.root.configure(bg=self.colors['bg'])
        self.setup_fonts()
        self.setup_variables()
        self.create_layout()
        self.load_history()

        self.bind_keys()

        self.root.after(100, self.center_window)

    def setup_fonts(self):
        self.font_title = font.Font(family="SF Pro Display", size=24, weight="bold")
        self.font_subtitle = font.Font(family="SF Pro Display", size=14)
        self.font_button = font.Font(family="Inter", size=11, weight="bold")
        self.font_input = font.Font(family="JetBrains Mono", size=13)
        self.font_result = font.Font(family="JetBrains Mono", size=14, weight="bold")

        try:
            self.font_title = font.Font(family="Segoe UI", size=24, weight="bold")
            self.font_subtitle = font.Font(family="Segoe UI", size=14)
            self.font_button = font.Font(family="Arial", size=11, weight="bold")
            self.font_input = font.Font(family="Consolas", size=13)
            self.font_result = font.Font(family="Consolas", size=14, weight="bold")
        except:
            pass

    def setup_variables(self):
        self.current_function = None
        self.input_fields = []
        self.history = []
        self.result_var = tk.StringVar(value="ВЫБЕРИТЕ ОПЕРАЦИЮ И ЗАПОЛНИТЕ СТРОКИ")
        self.expression_var = tk.StringVar(value="")

    def create_layout(self):
        main_container = tk.Frame(self.root, bg=self.colors['bg'])
        main_container.pack(fill='both', expand=True, padx=20, pady=20)

        self.create_header(main_container)

        content_frame = tk.Frame(main_container, bg=self.colors['bg'])
        content_frame.pack(fill='both', expand=True, pady=20)

        left_panel = self.create_left_panel(content_frame)
        right_panel = self.create_right_panel(content_frame)

        left_panel.pack(side='left', fill='both', expand=True)
        right_panel.pack(side='right', fill='both', expand=True, padx=(20, 0))

    def create_header(self, parent):
        header = tk.Frame(parent, bg=self.colors['bg'], height=80)
        header.pack(fill='x', pady=(0, 10))
        header.pack_propagate(False)

        title_frame = tk.Frame(header, bg=self.colors['bg'])
        title_frame.pack(side='left', fill='y')

        tk.Label(
            title_frame,
            text="CALCULATOR",
            font=self.font_title,
            bg=self.colors['bg'],
            fg=self.colors['text']
        ).pack(side='left', padx=(10, 0))

        tk.Label(
            title_frame,
            text="NS",
            font=self.font_title,
            bg=self.colors['bg'],
            fg=self.colors['primary']
        ).pack(side='left')

        tk.Label(
            title_frame,
            text="v2.0",
            font=self.font_subtitle,
            bg=self.colors['bg'],
            fg=self.colors['text_light']
        ).pack(side='left', padx=(15, 0))

        controls = tk.Frame(header, bg=self.colors['bg'])
        controls.pack(side='right', fill='y')

        self.create_small_button(controls, "⟳ Сброс", self.reset_all, self.colors['surface'])
        self.create_small_button(controls, "История", self.show_history_dialog, self.colors['surface'])

    def create_small_button(self, parent, text, command, bg):
        btn = tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=self.colors['text'],
            font=self.font_subtitle,
            relief='flat',
            bd=0,
            padx=15,
            pady=8,
            cursor='hand2'
        )
        btn.pack(side='left', padx=5)
        btn.bind("<Enter>", lambda e: btn.config(bg=self.colors['border']))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    def create_left_panel(self, parent):
        panel = tk.Frame(parent, bg=self.colors['surface'], relief='flat', bd=1)

        tk.Label(
            panel,
            text="ОПЕРАЦИИ",
            font=self.font_button,
            bg=self.colors['surface'],
            fg=self.colors['text_light'],
            anchor='w'
        ).pack(fill='x', padx=20, pady=(20, 10))

        canvas = tk.Canvas(panel, bg=self.colors['surface'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(panel, orient="vertical", command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=self.colors['surface'])

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True, padx=(10, 0))
        scrollbar.pack(side="right", fill="y")


        categories = [
            ("#3b82f6", "АРИФМЕТИКА", [
                ("Сложение", self.add, 2),
                ("Вычитание", self.subtract, 2),
                ("Умножение", self.multiply, 2),
                ("Деление", self.divide, 2),
                ("Степень", self.power, 2),
                ("Корень числа", self.sqrt, 1)
            ]),
            ("#8b5cf6", "ЧИСЛА", [
                ("Факториал", self.factorial, 1),
                ("Дв-й Факториал", self.double_fact, 1),
                ("Простое?", self.is_prime, 1),
                ("Множители", self.prime_factors, 1),
                ("НОД", self.gcd, 2),
                ("НОК", self.lcm, 2)
            ]),
            ("#10b981", "ГЕОМЕТРИЯ", [
                ("Синус", self.sin, 1),
                ("Косинус", self.cos, 1),
                ("Тангенс", self.tan, 1),
                ("Котангенс", self.ctg, 1),
                ("° → rad", self.deg_to_rad, 1),
                ("rad → °", self.rad_to_deg, 1)
            ]),
            ("#f59e0b", "АЛГЕБРА", [
                ("Уравнение Х", self.solve_linear, 2),
                ("Уравнение Х²", self.solve_quadratic, 3),
                ("Логарифм", self.logarithm, 2),
                ("Модуль", self.abs, 1),
                ("Дробная Часть", self.fractional, 1),
                ("Целая Часть", self.integer, 1)
            ]),

            ("#ff0000", "ФУНКЦИИ", [
                ("Прямая", self.line, 2),
                ("Парабола", self.parabola, 3),
                ("Гипербола", self.hiperbola, 3),
                ("Косинусоида", self.cosinus, 2),
                ("Синусоида", self.sinus, 2),
                ("Тангенсоида", self.tang, 2)
            ]),

            ("#ff69b4", "ГРАФИКИ", [
                ("Окружность", self.circle, 3),
                ("Модуль Х", self.moduleX, 2),
                ("Модуль Y", self.moduleY, 2),
                ("Модуль Y и Х", self.moduleXY, 2),
                ("Котангенсоида", self.cotang, 2),
                ("Сердце", self.heart, 1)
            ])
        ]

        for color, title, functions in categories:
            self.create_category(scrollable_frame, color, title, functions)

        def on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", on_mousewheel)

        return panel

    def create_category(self, parent, color, title, functions):
        frame = tk.Frame(parent, bg=self.colors['surface'])
        frame.pack(fill='x', padx=10, pady=(0, 7.5))

        tk.Label(
            frame,
            text=title,
            font=self.font_button,
            bg=self.colors['surface'],
            fg=color,
            anchor='w'
        ).pack(fill='x', pady=(0, 1))

        buttons_frame = tk.Frame(frame, bg=self.colors['surface'])
        buttons_frame.pack(fill='x')

        for i in range(3):
            buttons_frame.grid_columnconfigure(i, weight=1, uniform="group1")

        for i, (text, func, args) in enumerate(functions):
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=lambda f=func, a=args: self.select_operation(f, a),
                bg=self.colors['card'],
                fg=self.colors['text'],
                font=self.font_button,
                relief='flat',
                bd=1,
                padx=5,
                pady=5,
                cursor='hand2',
            )

            btn.grid(row=i // 3, column=i % 3, padx=3, pady=3, sticky='ew')

            btn.original_text = text
            btn.formula_text = self.button_formulas.get(text, text)

            btn.bind("<Enter>", lambda e, b=btn, c=color: self.on_button_enter(e, b, c))
            btn.bind("<Leave>", lambda e, b=btn: self.on_button_leave(e, b))

        for i in range(3):
            buttons_frame.grid_columnconfigure(i, weight=1)

    def create_right_panel(self, parent):
        panel = tk.Frame(parent, bg=self.colors['surface'])

        self.create_input_section(panel)
        self.create_output_section(panel)

        return panel

    def create_input_section(self, parent):
        frame = tk.Frame(parent, bg=self.colors['surface'])
        frame.pack(fill='x', pady=(0, 20))

        tk.Label(
            frame,
            text="ВВОД",
            font=self.font_button,
            bg=self.colors['surface'],
            fg=self.colors['text_light'],
            anchor='w'
        ).pack(fill='x', padx=20, pady=(0, 10))

        input_card = tk.Frame(frame, bg=self.colors['card'], relief='flat', bd=1)
        input_card.pack(fill='x', padx=20)

        self.expression_display = tk.Label(
            input_card,
            textvariable=self.expression_var,
            font=self.font_input,
            bg=self.colors['card'],
            fg=self.colors['text_light'],
            anchor='w',
            height=2
        )
        self.expression_display.pack(fill='x', padx=15, pady=5)

        self.input_container = tk.Frame(input_card, bg=self.colors['card'])
        self.input_container.pack(fill='x', padx=15, pady=(0, 15))

        self.status_label = tk.Label(
            input_card,
            text="Строки для ввода переменных",
            font=self.font_subtitle,
            bg=self.colors['card'],
            fg=self.colors['text_light'],
            anchor='w'
        )
        self.status_label.pack(fill='x', padx=15, pady=(0, 10))

    def create_output_section(self, parent):
        frame = tk.Frame(parent, bg=self.colors['surface'])
        frame.pack(fill='both', expand=True)

        tk.Label(
            frame,
            text="РЕЗУЛЬТАТ",
            font=self.font_button,
            bg=self.colors['surface'],
            fg=self.colors['text_light'],
            anchor='w'
        ).pack(fill='x', padx=20, pady=(0, 10))

        output_card = tk.Frame(frame, bg=self.colors['card'], relief='flat', bd=1)
        output_card.pack(fill='both', expand=True, padx=20)

        result_display = tk.Label(
            output_card,
            textvariable=self.result_var,
            font=self.font_result,
            bg=self.colors['card'],
            fg=self.colors['accent'],
            anchor='w',
            justify='left',
            wraplength=400
        )
        result_display.pack(fill='both', expand=True, padx=20, pady=20)

        controls = tk.Frame(output_card, bg=self.colors['card'])
        controls.pack(fill='x', padx=20, pady=(0, 20))

        tk.Button(
            controls,
            text="Вычислить",
            command=self.calculate,
            bg=self.colors['primary'],
            fg='white',
            font=self.font_button,
            relief='flat',
            padx=30,
            pady=12,
            cursor='hand2'
        ).pack(side='left')

        tk.Button(
            controls,
            text="Копировать",
            command=self.copy_result,
            bg=self.colors['surface'],
            fg=self.colors['text'],
            font=self.font_button,
            relief='flat',
            padx=20,
            pady=12,
            cursor='hand2'
        ).pack(side='left', padx=(10, 0))

    def select_operation(self, func, num_args):
        self.current_function = func
        self.num_args = num_args

        for widget in self.input_container.winfo_children():
            widget.destroy()

        self.input_fields = []
        self.expression_var.set("")

        for i in range(num_args):
            field_frame = tk.Frame(self.input_container, bg=self.colors['card'])
            field_frame.pack(fill='x', pady=3)

            label_text = ["a:", "b:", "c:", "x:", "y:"][i] if i < 5 else f"arg{i + 1}:"

            tk.Label(
                field_frame,
                text=label_text,
                bg=self.colors['card'],
                fg=self.colors['text_light'],
                font=self.font_input,
                width=4
            ).pack(side='left')

            entry = tk.Entry(
                field_frame,
                font=self.font_input,
                bg=self.colors['surface'],
                fg=self.colors['text'],
                insertbackground=self.colors['text'],
                relief='flat',
                bd=1
            )
            entry.pack(side='left', fill='x', expand=True, padx=(10, 0))

            self.input_fields.append(entry)

            entry.bind('<Return>', lambda e: self.calculate())
            entry.bind('<KeyRelease>', self.update_expression)

    def update_expression(self, event=None):
        values = []
        for entry in self.input_fields:
            val = entry.get().strip()
            if val:
                try:
                    float(val)
                    values.append(val)
                except:
                    values.append(val)

        func_name = self.current_function.__name__.replace('_', ' ').title() if self.current_function else ""

        if values:
            args_str = ', '.join(values)
            self.expression_var.set(f"{func_name}({args_str})")
        else:
            self.expression_var.set(func_name)

    def calculate(self):
        if not self.current_function:
            messagebox.showinfo("Внимание", "Сначала выберите операцию")
            return

        try:
            args = []
            for entry in self.input_fields:
                val = entry.get().strip()
                if not val:
                    messagebox.showwarning("Ошибка", "Заполните все поля")
                    return

                try:
                    if '/' in val and val.count('/') == 1:
                        num, den = val.split('/')
                        args.append(float(num) / float(den))
                    elif val.lower() == 'pi':
                        args.append(math.pi)
                    elif val.lower() == 'e':
                        args.append(math.e)
                    else:
                        args.append(float(val))
                except:
                    args.append(val)

            result = self.current_function(*args)

            if isinstance(result, float):
                if abs(result) > 1e10 or (abs(result) < 1e-10 and result != 0):
                    result = f"{result:.4e}"
                elif result.is_integer():
                    result = int(result)
                else:
                    result = round(result, 10)

            self.result_var.set(f"{result}")
            self.add_to_history(result)

        except ZeroDivisionError:
            self.result_var.set("ERROR: Деление на ноль")
        except ValueError as e:
            self.result_var.set(f"ERROR: {str(e)}")
        except Exception as e:
            self.result_var.set(f"ERROR: Ошибка вычисления")

    def add_to_history(self, result):
        if self.current_function:
            func_name = self.current_function.__name__
            args = [entry.get() for entry in self.input_fields]

            entry = {
                'function': func_name,
                'args': args,
                'result': str(result)
            }

            self.history.append(entry)
            if len(self.history) > 50:
                self.history.pop(0)

            self.save_history()

    def save_history(self):
        try:
            with open('calc_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.history[-20:], f, ensure_ascii=False, indent=2)
        except:
            pass

    def load_history(self):
        try:
            if os.path.exists('calc_history.json'):
                with open('calc_history.json', 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except:
            self.history = []

    def show_history_dialog(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("История вычислений")
        dialog.geometry("600x500")
        dialog.configure(bg=self.colors['bg'])
        dialog.transient(self.root)

        header = tk.Frame(dialog, bg=self.colors['surface'], height=60)
        header.pack(fill='x')
        header.pack_propagate(False)

        tk.Label(
            header,
            text="ИСТОРИЯ",
            font=self.font_title,
            bg=self.colors['surface'],
            fg=self.colors['text']
        ).pack(side='left', padx=20)

        tk.Button(
            header,
            text="Очистить",
            command=lambda: self.clear_history(dialog),
            bg=self.colors['danger'],
            fg='white',
            font=self.font_button,
            relief='flat'
        ).pack(side='right', padx=20)

        canvas = tk.Canvas(dialog, bg=self.colors['bg'], highlightthickness=0)
        scrollbar = ttk.Scrollbar(dialog, orient='vertical', command=canvas.yview)
        scroll_frame = tk.Frame(canvas, bg=self.colors['bg'])

        scroll_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox('all')))

        canvas.create_window((0, 0), window=scroll_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side='left', fill='both', expand=True, padx=20, pady=20)
        scrollbar.pack(side='right', fill='y')

        if not self.history:
            tk.Label(
                scroll_frame,
                text="История пуста",
                font=self.font_subtitle,
                bg=self.colors['bg'],
                fg=self.colors['text_light']
            ).pack(pady=50)
        else:
            for i, entry in enumerate(reversed(self.history)):
                self.create_history_item(scroll_frame, entry, i)

    def create_history_item(self, parent, entry, index):
        frame = tk.Frame(parent, bg=self.colors['card'], relief='flat', bd=1)
        frame.pack(fill='x', pady=5)

        func_name = entry['function'].replace('_', ' ').title()
        args_str = ', '.join(entry['args'])

        expr_label = tk.Label(
            frame,
            text=f"{func_name}({args_str})",
            font=self.font_input,
            bg=self.colors['card'],
            fg=self.colors['text']
        )
        expr_label.pack(anchor='w', padx=15, pady=(10, 0))

        result_label = tk.Label(
            frame,
            text=f"= {entry['result']}",
            font=self.font_result,
            bg=self.colors['card'],
            fg=self.colors['accent']
        )
        result_label.pack(anchor='w', padx=15, pady=(5, 10))

    def clear_history(self, dialog=None):
        self.history = []
        self.save_history()
        if dialog:
            dialog.destroy()
            self.show_history_dialog()

    def copy_result(self):
        result = self.result_var.get()
        if result and result != "ВЫБЕРИТЕ ОПЕРАЦИЮ И ЗАПОЛНИТЕ СТРОКИ":
            self.root.clipboard_clear()

            self.result_var.set("Скопировано!")
            self.root.after(1000, lambda: self.result_var.set(result))

    def reset_all(self):
        self.current_function = None
        self.expression_var.set("")
        self.result_var.set("ВЫБЕРИТЕ ОПЕРАЦИЮ И ЗАПОЛНИТЕ СТРОКИ")
        self.status_label.config(text="Строки для ввода переменных")

        for widget in self.input_container.winfo_children():
            widget.destroy()
        self.input_fields = []

    def bind_keys(self):
        self.root.bind('<Escape>', lambda e: self.reset_all())
        self.root.bind('<Control-c>', lambda e: self.copy_result())
        self.root.bind('<Control-l>', lambda e: self.show_history_dialog())

    def center_window(self):
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def add(self, a, b):
        return a + b

    def subtract(self, a, b):
        return a - b

    def multiply(self, a, b):
        return a * b

    def divide(self, a, b):
        if b == 0:
            raise ZeroDivisionError("Деление на ноль")
        return a / b

    def power(self, a, b):
        return a ** b

    def sqrt(self, x):
        if x < 0:
            raise ValueError("Корень из отрицательного числа")
        return math.sqrt(x)

    def factorial(self, n):
        if n < 0:
            raise ValueError("Факториал отрицательного числа")
        if n > 100:
            return math.inf
        return math.factorial(int(n))

    def double_fact(self, n):
        n = int(n)
        if n < 0:
            raise ValueError("Отрицательное число")
        result = 1
        start = 2 if n % 2 == 0 else 1
        for i in range(start, n + 1, 2):
            result *= i
        return result

    def is_prime(self, n):
        n = int(n)
        if n < 1:
            return "Функция работает только на натуральных числах!"
        if n == 1:
            return "Единица"
        if n == 2:
            return "Простое"
        if n % 2 == 0:
            return "Составное"
        for i in range(3, int(math.sqrt(n)) + 1, 2):
            if n % i == 0:
                return "Составное"
        return "Простое"

    def prime_factors(self, n):
        n = int(n)
        if n == 0:
            return "0"
        if n == 1:
            return "1"

        result = []
        temp = abs(n)

        while temp % 2 == 0:
            result.append(2)
            temp //= 2

        i = 3
        while i * i <= temp:
            while temp % i == 0:
                result.append(i)
                temp //= i
            i += 2

        if temp > 1:
            result.append(temp)

        if n < 0:
            result.insert(0, -1)

        return ' × '.join(map(str, result))

    def gcd(self, a, b):
        a, b = int(a), int(b)
        while b:
            a, b = b, a % b
        return abs(a)

    def lcm(self, a, b):
        a, b = int(a), int(b)
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // self.gcd(a, b)

    def sin(self, a):
        return math.sin(math.radians(a))

    def cos(self, a):
        return math.cos(math.radians(a))

    def tan(self, a):
        if a - 90 % 180 == 0:
            raise ZeroDivisionError("Деление на ноль")

        if a % 180 == 0:
            return 0
        else:
            return math.tan(math.radians(a))

    def ctg(self, a):
        if a % 180 == 0:
            raise ZeroDivisionError("Деление на ноль")
        if a - 90 % 180 == 0:
            return 0
        else:
            return 1 / math.tan(math.radians(a))

    def deg_to_rad(self, deg):
        return math.radians(deg)

    def rad_to_deg(self, rad):
        return math.degrees(rad)

    def solve_linear(self, a, b):
        if a == 0:
            if b == 0:
                return "Бесконечно решений"
            return "Нет решений"
        return -b / a

    def solve_quadratic(self, a, b, c):
        if a == 0:
            return self.solve_linear(b, c)

        D = b ** 2 - 4 * a * c
        if D > 0:
            x1 = (-b + math.sqrt(D)) / (2 * a)
            x2 = (-b - math.sqrt(D)) / (2 * a)
            return f"x₁ = {x1}, x₂ = {x2}"
        elif D == 0:
            x = -b / (2 * a)
            return f"x = {x} (кратный)"
        else:
            real = -b / (2 * a)
            imag = math.sqrt(-D) / (2 * a)
            return f"x₁ = {real} + {imag}i, x₂ = {real} - {imag}i"

    def logarithm(self, base, a):
        if base <= 0 or base == 1:
            raise ValueError("Основание должно быть >0 и ≠1")
        if a <= 0:
            raise ValueError("Аргумент должен быть >0")
        return math.log(a, base)

    def abs(self, a):
        return abs(a)

    def integer(self, x):
        if x >= 0:
            return int(x)
        else:
            if x - int(x) < 0:
                return int(x) - 1

            else:
                return int(x)

    def fractional(self, x):
        if x >= 0:
            return x - int(x)
        else:
            if x - int(x) < 0:
                return x - (int(x) - 1)

            else:
                return 0

    def line(self, a, b):
        x = np.linspace(-11, 11, 400)
        y = a * x + b
        plt.figure(figsize=(10, 10))
        plt.plot(x, y, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, c, d = "", "", ""

        if a == 0:
            c = ""
        elif a == 1:
            c = "x "
        elif a == -1:
            c = "-x "
        else:
            c = f'{a}x '

        if c != "":
            if b == 0:
                d = ""
            elif b > 0:
                d = f'+ {b}'
            else:
                d = f'- {-b}'
        else:
            if b == 0:
                d = ""
            elif b > 0:
                d = f'{b}'
            else:
                d = f'{-b}'

        if c + d == "":
            c = "0"

        string = "Прямая: " + "y = " + c + d

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def parabola(self, a, b, c):
        x = np.linspace(-11, 11, 400)
        y = a * x ** 2 + b * x + c
        plt.figure(figsize=(10, 10))
        plt.plot(x, y, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        string, d, e, f, g = "", "", "", "", "Парабола: "

        if a == 0:
            g = "Прямая: "
            d = ""
        elif a == 1:
            d = "x² "
        elif a == -1:
            d = f'-x² '
        elif a > 0:
            d = f'{a}x² '
        else:
            d = f'{a}x² '

        if d != "":
            if b == 0:
                e = ""
            elif b == 1:
                e = "+ x "
            elif b == -1:
                e = "- x "
            elif b > 0:
                e = f'+ {b}x '
            else:
                e = f'- {-b}x '
        else:
            if b == 0:
                e = ""
            elif b == 1:
                e = "x "
            elif b == -1:
                e = "x "
            elif b > 0:
                e = f'{b}x '
            else:
                e = f'{-b}x '

        if e != "":
            if c == 0:
                f = ""
            elif c > 0:
                f = f'+ {c}'
            else:
                f = f'- {-c}'
        else:
            if c == 0:
                f = ""
            elif c > 0:
                f = f'{c}'
            else:
                f = f'{-c}'

        if d + e + f == "":
            d = "0"

        string = g + "y = " + d + e + f

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.xlim(-11, 11)
        plt.ylim(-11, 11)
        plt.legend()
        plt.show()
        return "График построен"

    def hiperbola(self, a, b, c):
        x = np.linspace(-11, 11, 400)
        y = a / (x + b) + c
        plt.figure(figsize=(10, 10))
        plt.plot(x, y, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, d, e, f, g = "", "", "", "", "Гипербола: "

        if a == 0:
            d, e, g = "0", "", "Прямая: "
        else:
            d = str(a)
            if b == 0:
                e = "/ x"
            elif b > 0:
                e = f'/ (x + {b})'
            else:
                e = f'/ (x - {-b})'

        if d + e != "":
            if c == 0:
                f = ""
            elif c > 0:
                f = f'+ {c}'
            else:
                f = f'- {-c}'
        else:
            if c == 0:
                f = ""
            elif c > 0:
                f = f'{c}'
            else:
                f = f'{-c}'

        if d + e + f == "":
            d = "0"

        string = g + "y = " + d + e + f

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def circle(self, a, b, c):
        t = np.linspace(0, 2 * np.pi, 100)
        x = a + c * np.cos(t)
        y = b + c * np.sin(t)

        plt.figure(figsize=(10, 10))
        plt.plot(x, y, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, d, e = "", "", ""

        if a == 0:
            d = "x² + "
        elif a > 0:
            d = f'(x - {a})² + '
        else:
            d = f'(x + {-a})² + '

        if b == 0:
            e = "y²"
        elif b > 0:
            e = f'(y - {b})²'
        else:
            e = f'(y + {-b})²'

        string = "Окружность: " + d + e + " = " + str(c ** 2)

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def moduleX(self, a, b, c):
        x = np.linspace(-11, 11, 400)
        y = a * np.abs(x + b) + c

        plt.figure(figsize=(10, 10))
        plt.plot(x, y, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, d, e, f, g = "", "", "", "", "Модуль Х: "

        if a == 0:
            g = "Прямая: "
            d, e = "", ""
        elif a == 1:
            d = ""
            if b == 0:
                e = "|x| "
            elif b > 0:
                e = f'|x + {b}| '
            else:
                e = f'|x - {-b}| '
        elif a == -1:
            d = "-"
            if b == 0:
                e = "|x| "
            elif b > 0:
                e = f'|x + {b}| '
            else:
                e = f'|x - {-b}| '
        else:
            d = str(a)
            if b == 0:
                e = "|x| "
            elif b > 0:
                e = f'|x + {b}| '
            else:
                e = f'|x - {-b}| '

        if d + e != "":
            if c == 0:
                f = ""
            elif c > 0:
                f = f'+ {c}'
            else:
                f = f'- {-c}'
        else:
            if c == 0:
                f = ""
            elif c > 0:
                f = f'{c}'
            else:
                f = f'{-c}'

        if d + e + f == 0:
            d = "0"

        string = g + "y = " + d + e + f

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def moduleY(self, a, b):
        x = np.linspace(-10, 10, 400)
        y_plus = a * x + b
        y_minus = -a * x - b

        plt.figure(figsize=(10, 10))
        plt.plot(x, y_plus, 'b-', linewidth=3, label='График')
        plt.plot(x, y_minus, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, d, e, g = "", "", "", "Модуль Y: "

        if a == 0:
            g = "Прямая: "
            d = ""
        elif a == 1:
            d = "x "
        elif a == -1:
            d = "-x "
        else:
            d = f'{a}x '

        if d != "":
            if b == 0:
                e = ""
            elif b > 0:
                e = f'+ {b}'
            else:
                e = f'- {-b}'
        else:
            if b == 0:
                e = ""
            elif b > 0:
                e = f'{b}'
            else:
                e = f'{-b}'

        if d + e == "":
            d = "0"

        string = g + "|y| = " + d + e

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def moduleXY(self, a, b):
        x = np.linspace(-11, 11, 400)
        y_plus = a * np.abs(x) + b
        y_minus = -a * np.abs(x) - b

        plt.figure(figsize=(10, 10))
        plt.plot(x, y_plus, 'b-', linewidth=3, label='График')
        plt.plot(x, y_minus, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, d, e, g = "", "", "", "Модуль Х и Y: "

        if a == 0:
            g = "Прямая: "
            d = ""
        elif a == 1:
            d = "|x| "
        elif a == -1:
            d = "-|x| "
        else:
            d = f'{a}|x| '

        if d != "":
            if b == 0:
                e = ""
            elif b > 0:
                e = f'+ {b}'
            else:
                e = f'- {-b}'
        else:
            if b == 0:
                e = ""
            elif b > 0:
                e = f'{b}'
            else:
                e = f'{-b}'

        if d + e == "":
            d = "0"

        string = g + "|y| = " + d + e

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def sinus(self, a, b):
        x = np.linspace(-11, 11, 400)
        y = a * np.sin(x) + b

        plt.figure(figsize=(10, 10))
        plt.plot(x, y, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, c, d, e = "", "", "", "Синусоида: "

        if a == 0:
            c = ""
            e = "Прямая: "
        elif a == 1:
            c = "sin(x) "
        elif a == -1:
            c = "-sin(x) "
        else:
            c = f'{a}sin(x) '

        if c != "":
            if b == 0:
                d = ""
            elif b > 0:
                d = f'+ {b}'
            else:
                d = f'- {-b}'
        else:
            if b == 0:
                d = ""
            elif b > 0:
                d = f'{b}'
            else:
                d = f'{-b}'

        if c + d == "":
            c = "0"

        string = e + "y = " + c + d

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def cosinus(self, a, b):
        x = np.linspace(-11, 11, 400)
        y = a * np.cos(x) + b

        plt.figure(figsize=(10, 10))
        plt.plot(x, y, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, c, d, e = "", "", "", "Косинусоида: "

        if a == 0:
            c = ""
            e = "Прямая: "
        elif a == 1:
            c = "cos(x) "
        elif a == -1:
            c = "-cos(x) "
        else:
            c = f'{a}cos(x) '

        if c != "":
            if b == 0:
                d = ""
            elif b > 0:
                d = f'+ {b}'
            else:
                d = f'- {-b}'
        else:
            if b == 0:
                d = ""
            elif b > 0:
                d = f'{b}'
            else:
                d = f'{-b}'

        if c + d == "":
            c = "0"

        string = e + "y = " + c + d

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def tang(self, a, b):
        x = np.linspace(-11, 11, 400)
        y = a * np.tan(x) + b

        plt.figure(figsize=(10, 10))
        plt.plot(x, y, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, c, d, e = "", "", "", "Тангенс: "

        if a == 0:
            c = ""
            e = "Прямая: "
        elif a == 1:
            c = "tg(x) "
        elif a == -1:
            c = "-tg(x) "
        else:
            c = f'{a}tg(x) '

        if c != "":
            if b == 0:
                d = ""
            elif b > 0:
                d = f'+ {b}'
            else:
                d = f'- {-b}'
        else:
            if b == 0:
                d = ""
            elif b > 0:
                d = f'{b}'
            else:
                d = f'{-b}'

        if c + d == "":
            c = "0"

        string = e + "y = " + c + d

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def cotang(self, a, b):
        x = np.linspace(-10, 10, 400)
        y = a / np.tan(x) + b

        plt.figure(figsize=(10, 10))
        plt.plot(x, y, 'b-', linewidth=3, label='График')

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-11, 11)
        plt.ylim(-11, 11)

        string, c, d, e = "", "", "", "Котангенс: "

        if a == 0:
            c = ""
            e = "Прямая: "
        elif a == 1:
            c = "ctg(x) "
        elif a == -1:
            c = "-ctg(x) "
        else:
            c = f'{a}ctg(x) '

        if c != "":
            if b == 0:
                d = ""
            elif b > 0:
                d = f'+ {b}'
            else:
                d = f'- {-b}'
        else:
            if b == 0:
                d = ""
            elif b > 0:
                d = f'{b}'
            else:
                d = f'{-b}'

        if c + d == "":
            c = "0"

        string = e + "y = " + c + d

        plt.title(string, fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def heart(self, a):
        x = np.linspace(-1.5, 1.5, 1000) * a
        y = np.linspace(-1.5, 1.5, 1000) * a
        X, Y = np.meshgrid(x, y)

        f = (X ** 2 + Y ** 2 - 1) ** 3 - X ** 2 * Y ** 3

        plt.figure(figsize=(10, 10))
        plt.contour(X, Y, f, levels=[0], colors='#ff69b4', linewidth=10, label="Сердце")

        plt.axhline(y=0, color='black', linestyle='-', linewidth=2.5, label='Ось Х')
        plt.axvline(x=0, color='black', linestyle='-', linewidth=2.5, label='Ось Y')

        plt.arrow(10, 0, 0.5, 0, head_width=0.3, head_length=0.3, fc='black', ec='black')
        plt.arrow(0, 10, 0, 0.5, head_width=0.3, head_length=0.3, fc='black', ec='black')

        plt.text(10.5, -1, 'X', fontsize=14, fontweight='bold', color='black')
        plt.text(-0.8, 10.3, 'Y', fontsize=14, fontweight='bold', color='black')

        plt.xlim(-1.5 * a, 1.5 * a)
        plt.ylim(-1.5 * a, 1.5 * a)

        plt.title(f'y = С любовью, NebulaStack!', fontsize=14)
        plt.grid(True, alpha=0.3)
        plt.legend()
        plt.show()
        return "График построен"

    def on_button_enter(self, event, button, color):
        button.config(
            bg=color,
            fg='white',
            text=button.formula_text
        )

    def on_button_leave(self, event, button):
        button.config(
            bg=self.colors['card'],
            fg=self.colors['text'],
            text=button.original_text
        )

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
