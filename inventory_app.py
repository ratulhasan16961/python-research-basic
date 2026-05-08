import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv

def create_table():
    conn = sqlite3.connect('general_inventory.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT, category TEXT, price REAL, stock_count INTEGER)''')
    conn.commit()
    conn.close()

create_table()

def login():
    username = user_entry.get()
    password = pass_entry.get()

    if username == "admin" and password == "1234":
        login_window.destroy() 
        main_app()              
    else:
        messagebox.showerror("Login Failed", "Invalid Username or Password!")

def main_app():
    global tree, name_entry, category_entry, price_entry, stock_entry, search_entry

    root = tk.Tk()
    root.title("Ratul's Smart Inventory v4.0")
    root.geometry("900x750")

    def fetch_data(query="SELECT * FROM products"):
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for item in tree.get_children(): tree.delete(item)
        for row in rows: tree.insert('', tk.END, values=row)
        conn.close()

    def check_low_stock():
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT name, stock_count FROM products WHERE stock_count < 10")
        low_stock_items = cursor.fetchall()
        conn.close()
        
        if low_stock_items:
            items_list = "\n".join([f"• {item[0]} (Stock: {item[1]})" for item in low_stock_items])
            messagebox.showwarning("Low Stock Alert ⚠️", f"The following items are low on stock:\n\n{items_list}")

    def on_tree_select(event):
        selected = tree.selection()
        if selected:
            values = tree.item(selected)['values']
            name_entry.delete(0, tk.END); name_entry.insert(0, values[1])
            category_entry.delete(0, tk.END); category_entry.insert(0, values[2])
            price_entry.delete(0, tk.END); price_entry.insert(0, values[3])
            stock_entry.delete(0, tk.END); stock_entry.insert(0, values[4])

    def add_product():
        name, cat, price, stock = name_entry.get(), category_entry.get(), price_entry.get(), stock_entry.get()
        if not (name and price and stock):
            messagebox.showwarning("Input Error", "Fill all fields!")
            return
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, category, price, stock_count) VALUES (?, ?, ?, ?)",
                       (name, cat, float(price), int(stock)))
        conn.commit()
        conn.close()
        fetch_data()
        messagebox.showinfo("Success", "Product added!")
        check_low_stock() 

    def update_product():
        selected = tree.selection()
        if not selected: return
        p_id = tree.item(selected)['values'][0]
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE products SET name=?, category=?, price=?, stock_count=? WHERE id=?",
                       (name_entry.get(), category_entry.get(), float(price_entry.get()), int(stock_entry.get()), p_id))
        conn.commit()
        conn.close()
        fetch_data()
        check_low_stock() 

    def delete_product():
        selected = tree.selection()
        if not selected: return
        item = tree.item(selected)['values']
        if messagebox.askyesno("Confirm", f"Delete {item[1]}?"):
            conn = sqlite3.connect('general_inventory.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (item[0],))
            conn.commit()
            conn.close()
            fetch_data()

    def search_product():
        term = search_entry.get()
        fetch_data(f"SELECT * FROM products WHERE name LIKE '%{term}%' OR category LIKE '%{term}%'")

    search_frame = tk.Frame(root)
    search_frame.pack(pady=10)
    search_entry = tk.Entry(search_frame, width=30); search_entry.pack(side="left", padx=5)
    tk.Button(search_frame, text="🔍 Search", command=search_product).pack(side="left", padx=5)
    tk.Button(search_frame, text="🔄 Reset", command=lambda: fetch_data()).pack(side="left", padx=5)

    input_frame = tk.LabelFrame(root, text=" Product Management ", padx=10, pady=10)
    input_frame.pack(pady=10, padx=20, fill="x")

    tk.Label(input_frame, text="Name:").grid(row=0, column=0); name_entry = tk.Entry(input_frame); name_entry.grid(row=0, column=1)
    tk.Label(input_frame, text="Stock:").grid(row=0, column=2); stock_entry = tk.Entry(input_frame); stock_entry.grid(row=0, column=3)
    tk.Label(input_frame, text="Price:").grid(row=1, column=0); price_entry = tk.Entry(input_frame); price_entry.grid(row=1, column=1)
    tk.Label(input_frame, text="Category:").grid(row=1, column=2); category_entry = tk.Entry(input_frame); category_entry.grid(row=1, column=3)

    btn_frame = tk.Frame(root)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Add", command=add_product, width=10, bg="#27ae60", fg="black").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Update", command=update_product, width=10, bg="#f39c12", fg="black").pack(side="left", padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_product, width=10, bg="#e74c3c", fg="black").pack(side="left", padx=5)

    columns = ('ID', 'Name', 'Category', 'Price', 'Stock')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns: tree.heading(col, text=col); tree.column(col, width=100, anchor="center")
    tree.pack(pady=10, fill="both", expand=True)
    tree.bind('<<TreeviewSelect>>', on_tree_select)

    fetch_data()
    check_low_stock() 
    root.mainloop()

login_window = tk.Tk()
login_window.title("Login - Ratul's Inventory")
login_window.geometry("350x250")

tk.Label(login_window, text="RESTRICTED ACCESS", font=("Arial", 12, "bold"), fg="red").pack(pady=10)

tk.Label(login_window, text="Username:").pack()
user_entry = tk.Entry(login_window); user_entry.pack(pady=5)

tk.Label(login_window, text="Password:").pack()
pass_entry = tk.Entry(login_window, show="*"); pass_entry.pack(pady=5)

tk.Button(login_window, text="Login", command=login, width=15, bg="#3498db").pack(pady=20)

login_window.mainloop()