import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random

DATA_FILE = "data/quotes.json"

# Предопределённые цитаты (текст, автор, тема)
PREDEFINED_QUOTES = [
    {"text": "Величайшая слава не в том, чтобы никогда не ошибаться, а в том, чтобы уметь подняться каждый раз, когда падаешь.", "author": "Конфуций", "theme": "Мотивация"},
    {"text": "Единственный способ сделать выдающуюся работу — любить то, чем занимаешься.", "author": "Стив Джобс", "theme": "Работа"},
    {"text": "Жизнь — это то, что происходит, пока ты строишь другие планы.", "author": "Джон Леннон", "theme": "Жизнь"},
    {"text": "Не ошибается тот, кто ничего не делает.", "author": "Народная мудрость", "theme": "Ошибки"},
    {"text": "Будущее принадлежит тем, кто верит в красоту своей мечты.", "author": "Элеонора Рузвельт", "theme": "Мечты"},
]

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def generate_quote():
    quote = random.choice(PREDEFINED_QUOTES)
    quote_text.set(f'"{quote["text"]}"')
    author_text.set(f"— {quote['author']}")
    theme_text.set(f"Тема: {quote['theme']}")
    history.append(quote)
    save_data(history)
    update_history_list()

def filter_history():
    author = author_filter.get().strip().lower()
    theme = theme_filter.get().strip().lower()
    filtered = history
    if author:
        filtered = [q for q in filtered if author in q["author"].lower()]
    if theme:
        filtered = [q for q in filtered if theme in q["theme"].lower()]
    update_history_list(filtered)

def update_history_list(data=None):
    history_listbox.delete(0, tk.END)
    for q in (data if data else history):
        history_listbox.insert(tk.END, f'"{q["text"]}" — {q["author"]} | Тема: {q["theme"]}')

# Загрузка истории
history = load_data()

# Основное окно
root = tk.Tk()
root.title("Random Quote Generator")
root.geometry("600x500")

# Вкладки
tab_control = ttk.Notebook(root)
tab1 = ttk.Frame(tab_control)
tab2 = ttk.Frame(tab_control)
tab_control.add(tab1, text="Генератор")
tab_control.add(tab2, text="История")
tab_control.pack(expand=1, fill="both")

# Вкладка 1: Генерация цитаты
tk.Label(tab1, text="Случайная цитата:").pack(pady=5)
quote_text = tk.StringVar()
tk.Label(tab1, textvariable=quote_text, wraplength=500, justify="center").pack(pady=5)
author_text = tk.StringVar()
tk.Label(tab1, textvariable=author_text).pack(pady=2)
theme_text = tk.StringVar()
tk.Label(tab1, textvariable=theme_text).pack(pady=2)
tk.Button(tab1, text="Сгенерировать цитату", command=generate_quote).pack(pady=10)

# Вкладка 2: История и фильтрация
tk.Label(tab2, text="Фильтр по автору:").pack(pady=5)
author_filter = tk.Entry(tab2)
author_filter.pack(pady=2)
tk.Label(tab2, text="Фильтр по теме:").pack(pady=5)
theme_filter = tk.Entry(tab2)
theme_filter.pack(pady=2)
tk.Button(tab2, text="Фильтровать", command=filter_history).pack(pady=5)

history_listbox = tk.Listbox(tab2, width=70, height=15)
history_listbox.pack(pady=10)
update_history_list()

root.mainloop()
