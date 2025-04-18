import tkinter as tk
from tkinter import messagebox, ttk
import pandas as pd
from datetime import datetime
import pyarrow.parquet as pq
import pyarrow as pa
import os
FILE = "people.parquet"

def load_data():
    if os.path.exists(FILE):
        return pd.read_parquet(FILE)
    return pd.DataFrame(columns=["Фамилия", "Имя", "Телефон", "Дата рождения"])

def save_data(df):
    table = pa.Table.from_pandas(df)
    pq.write_table(table, FILE)

def add_entry():
    last = last_name_var.get()
    first = first_name_var.get()
    phone = phone_var.get()
    bdate = birthdate_var.get()

    try:
        date = datetime.strptime(bdate, "%d.%m.%Y")
        birth_list = [date.day, date.month, date.year]
    except ValueError:
        messagebox.showerror("Ошибка", "Дата в формате ДД.ММ.ГГГГ")
        return

    df = load_data()
    new_row = {"Фамилия": last, "Имя": first, "Телефон": phone, "Дата рождения": birth_list}
    df = pd.concat([df, pd.DataFrame([new_row])])
    df = df.sort_values(by=["Фамилия", "Имя"])
    save_data(df)
    messagebox.showinfo("Успех", "Запись добавлена!")

def filter_by_month():
    try:
        month = int(month_var.get())
        if not 1 <= month <= 12:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Месяц должен быть числом от 1 до 12")
        return

    df = load_data()
    filtered = df[df["Дата рождения"].apply(lambda d: d[1] == month)]
    result_text.delete("1.0", tk.END)
    if filtered.empty:
        result_text.insert(tk.END, "Нет людей с днем рождения в этом месяце.")
    else:
        result_text.insert(tk.END, filtered.to_string(index=False))

def delete_by_column():
    col = delete_column_var.get()
    val = delete_value_var.get()

    df = load_data()
    if col not in df.columns:
        messagebox.showerror("Ошибка", f"Колонка '{col}' не найдена.")
        return

    before = len(df)
    df = df[df[col] != val]
    after = len(df)
    save_data(df)
    messagebox.showinfo("Готово", f"Удалено записей: {before - after}")

okno = tk.Tk()
okno.title("Учет данных о людях")
okno.geometry("600x550")
tk.Label(okno, text="Фамилия").pack()
last_name_var = tk.StringVar()
tk.Entry(okno, textvariable=last_name_var).pack()
tk.Label(okno, text="Имя").pack()
first_name_var = tk.StringVar()
tk.Entry(okno, textvariable=first_name_var).pack()
tk.Label(okno, text="Телефон").pack()
phone_var = tk.StringVar()
tk.Entry(okno, textvariable=phone_var).pack()
tk.Label(okno, text="Дата рождения (ДД.ММ.ГГГГ)").pack()
birthdate_var = tk.StringVar()
tk.Entry(okno, textvariable=birthdate_var).pack()
tk.Button(okno, text="Добавить", command=add_entry).pack(pady=5)
tk.Label(okno, text="Фильтр по месяцу рождения (1-12)").pack()
month_var = tk.StringVar()
tk.Entry(okno, textvariable=month_var).pack()
tk.Button(okno, text="Показать", command=filter_by_month).pack(pady=5)
result_text = tk.Text(okno, height=10, width=70)
result_text.pack()
tk.Label(okno, text="Удалить записи по колонке").pack()
delete_column_var = tk.StringVar()
delete_column_menu = ttk.Combobox(okno, textvariable=delete_column_var)
delete_column_menu['values'] = ["Фамилия", "Имя", "Телефон"]
delete_column_menu.pack()
delete_value_var = tk.StringVar()
tk.Entry(okno, textvariable=delete_value_var).pack()
tk.Button(okno, text="Удалить", command=delete_by_column).pack(pady=5)
okno.mainloop()
