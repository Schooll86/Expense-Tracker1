import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "data.json"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("600x400")

        self.data = self.load_data()

        tk.Label(root, text="Сумма").grid(row=0, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(root, text="Категория").grid(row=1, column=0)
        self.category_entry = ttk.Combobox(root, values=["Еда", "Транспорт", "Развлечения", "Другое"])
        self.category_entry.grid(row=1, column=1)

        tk.Label(root, text="Дата (YYYY-MM-DD)").grid(row=2, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.grid(row=2, column=1)

        tk.Button(root, text="Добавить", command=self.add_expense).grid(row=3, column=1)

        self.tree = ttk.Treeview(root, columns=("date", "category", "amount"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("category", text="Категория")
        self.tree.heading("amount", text="Сумма")
        self.tree.grid(row=4, column=0, columnspan=3)

        tk.Button(root, text="Показать всё", command=self.show_all).grid(row=5, column=0)
        tk.Button(root, text="Сумма всего", command=self.total_sum).grid(row=5, column=1)

        self.refresh_table()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть > 0")
            return

        if not category or not date:
            messagebox.showerror("Ошибка", "Заполните все поля")
            return

        self.data.append({
            "amount": int(amount),
            "category": category,
            "date": date
        })

        self.save_data()
        self.refresh_table()

    def refresh_table(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        for item in self.data:
            self.tree.insert("", "end", values=(item["date"], item["category"], item["amount"]))

    def show_all(self):
        self.refresh_table()

    def total_sum(self):
        total = sum(item["amount"] for item in self.data)
        messagebox.showinfo("Сумма", f"Всего: {total}")

    def save_data(self):
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)

    def load_data(self):
        if not os.path.exists("data.json"):
            return []
        with open("data.json", "r", encoding="utf-8") as f:
            return json.load(f)

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
