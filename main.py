import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

DATA_FILE = "data.json"


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.root.geometry("700x500")

        self.data = self.load_data()

        # ===== INPUTS =====
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

        # ===== FILTERS =====
        tk.Label(root, text="Фильтр категория").grid(row=4, column=0)
        self.filter_category = ttk.Combobox(root, values=["", "Еда", "Транспорт", "Развлечения", "Другое"])
        self.filter_category.grid(row=4, column=1)

        tk.Label(root, text="Дата от").grid(row=5, column=0)
        self.date_from = tk.Entry(root)
        self.date_from.grid(row=5, column=1)

        tk.Label(root, text="Дата до").grid(row=6, column=0)
        self.date_to = tk.Entry(root)
        self.date_to.grid(row=6, column=1)

        tk.Button(root, text="Применить фильтр", command=self.apply_filter).grid(row=7, column=1)
        tk.Button(root, text="Показать всё", command=self.show_all).grid(row=7, column=2)
        tk.Button(root, text="Сумма", command=self.total_sum).grid(row=7, column=3)

        # ===== TABLE =====
        self.tree = ttk.Treeview(root, columns=("date", "category", "amount"), show="headings")
        self.tree.heading("date", text="Дата")
        self.tree.heading("category", text="Категория")
        self.tree.heading("amount", text="Сумма")
        self.tree.grid(row=8, column=0, columnspan=4)

        self.refresh_table()

    # ===== ADD EXPENSE =====
    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not amount.isdigit() or int(amount) <= 0:
            messagebox.showerror("Ошибка", "Сумма должна быть числом > 0")
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

    # ===== TABLE =====
    def refresh_table(self, data=None):
        for row in self.tree.get_children():
            self.tree.delete(row)

        data = data if data else self.data

        for item in data:
            self.tree.insert("", "end", values=(item["date"], item["category"], item["amount"]))

    # ===== FILTER =====
    def apply_filter(self):
        category = self.filter_category.get()
        date_from = self.date_from.get()
        date_to = self.date_to.get()

        filtered = self.data

        if category:
            filtered = [x for x in filtered if x["category"] == category]

        if date_from:
            filtered = [x for x in filtered if x["date"] >= date_from]

        if date_to:
            filtered = [x for x in filtered if x["date"] <= date_to]

        self.refresh_table(filtered)

    # ===== SHOW ALL =====
    def show_all(self):
        self.refresh_table()

    # ===== TOTAL SUM =====
    def total_sum(self):
        category = self.filter_category.get()
        date_from = self.date_from.get()
        date_to = self.date_to.get()

        filtered = self.data

        if category:
            filtered = [x for x in filtered if x["category"] == category]
            if date_from:
            filtered = [x for x in filtered if x["date"] >= date_from]

        if date_to:
            filtered = [x for x in filtered if x["date"] <= date_to]

        total = sum(item["amount"] for item in filtered)

        message
