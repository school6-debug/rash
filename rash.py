import tkinter as tk
from tkinter import messagebox, Listbox, StringVar, OptionMenu
import json
from datetime import datetime

class ExpenseTrackerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")

        # Поля ввода
        self.amount_label = tk.Label(root, text="Сумма:")
        self.amount_label.pack(pady=5)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.pack(pady=5)

        self.category_label = tk.Label(root, text="Категория:")
        self.category_label.pack(pady=5)
        self.category_var = StringVar(root)
        self.category_var.set("Еда")  # Значение по умолчанию
        self.category_menu = OptionMenu(root, self.category_var, "Еда", "Транспорт", "Развлечения", "Другие")
        self.category_menu.pack(pady=5)

        self.date_label = tk.Label(root, text="Дата (YYYY-MM-DD):")
        self.date_label.pack(pady=5)
        self.date_entry = tk.Entry(root)
        self.date_entry.pack(pady=5)

        # Кнопка добавления расхода
        self.add_button = tk.Button(root, text="Добавить расход", command=self.add_expense)
        self.add_button.pack(pady=10)

        # Таблица расходов
        self.expense_list_label = tk.Label(root, text="Записи расходов:")
        self.expense_list_label.pack(pady=5)

        self.expense_list = Listbox(root, width=50)
        self.expense_list.pack(pady=5)

        # Фильтрация
        self.filter_label = tk.Label(root, text="Фильтрация по категории:")
        self.filter_label.pack(pady=5)
        
        self.filter_category_var = StringVar(root)
        self.filter_category_var.set("Все")  # Значение по умолчанию
        self.filter_category_menu = OptionMenu(root, self.filter_category_var, "Все", "Еда", "Транспорт", "Развлечения", "Другие")
        self.filter_category_menu.pack(pady=5)

        self.filter_button = tk.Button(root, text="Фильтровать", command=self.filter_expenses)
        self.filter_button.pack(pady=5)

        # Подсчет суммы за период
        self.start_date_label = tk.Label(root, text="Дата начала (YYYY-MM-DD):")
        self.start_date_label.pack(pady=5)
        self.start_date_entry = tk.Entry(root)
        self.start_date_entry.pack(pady=5)

        self.end_date_label = tk.Label(root, text="Дата окончания (YYYY-MM-DD):")
        self.end_date_label.pack(pady=5)
        self.end_date_entry = tk.Entry(root)
        self.end_date_entry.pack(pady=5)

        self.calculate_button = tk.Button(root, text="Подсчитать сумму", command=self.calculate_total)
        self.calculate_button.pack(pady=10)

        # Загрузка данных из файла
        self.expenses = []
        self.load_expenses()

    def add_expense(self):
        amount_str = self.amount_entry.get()
        category = self.category_var.get()
        date_str = self.date_entry.get()

        if not self.validate_input(amount_str, date_str):
            return

        expense = {
            "amount": float(amount_str),
            "category": category,
            "date": date_str
        }

        self.expenses.append(expense)
        self.update_expense_display()
        self.save_expenses()

    def validate_input(self, amount_str, date_str):
        # Проверка суммы
        try:
            amount = float(amount_str)
            if amount <= 0:
                raise ValueError("Сумма должна быть положительным числом.")
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректную сумму.")
            return False

        # Проверка даты
        try:
            datetime.strptime(date_str, "%Y-%m-%d")

        except ValueError:
            messagebox.showerror("Ошибка", "Неверный формат даты. Используйте YYYY-MM-DD.")
            return False

        return True

    def update_expense_display(self):
        self.expense_list.delete(0, tk.END)
        
        for expense in self.expenses:
            display_text = f"{expense['date']} - {expense['amount']}₽ - {expense['category']}"
            self.expense_list.insert(tk.END, display_text)

    def filter_expenses(self):
        selected_category = self.filter_category_var.get()
        
        filtered_expenses = [expense for expense in self.expenses if selected_category == "Все" or expense["category"] == selected_category]
        
        self.expense_list.delete(0, tk.END)
        
        for expense in filtered_expenses:
            display_text = f"{expense['date']} - {expense['amount']}₽ - {expense['category']}"
            self.expense_list.insert(tk.END, display_text)

    def calculate_total(self):
        start_date_str = self.start_date_entry.get()
        end_date_str = self.end_date_entry.get()

        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            
            total_amount = sum(expense["amount"] for expense in self.expenses if start_date <= datetime.strptime(expense["date"], "%Y-%m-%d") <= end_date)
            
            messagebox.showinfo("Сумма расходов", f"Общая сумма расходов за выбранный период: {total_amount}₽")
            
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные даты в формате YYYY-MM-DD.")

    def load_expenses(self, filename='expenses.json'):
        try:
            with open(filename, 'r') as f:
                self.expenses = json.load(f)
                self.update_expense_display()
        except FileNotFoundError:
            pass

    def save_expenses(self, filename='expenses.json'):
        with open(filename, 'w') as f:
            json.dump(self.expenses, f)

# Запуск приложения
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
