import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

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
    if user_entry.get() == "admin" and pass_entry.get() == "1234":
        login_window.destroy()
        main_app()
    else:
        messagebox.showerror("Error", "Invalid Credentials")

def main_app():
    global tree, root, is_dark_mode, name_entry, category_entry, price_entry, stock_entry
    root = tk.Tk()
    root.title("Ratul's Smart Inventory v5.0")
    root.geometry("1000x850")
    is_dark_mode = True 
    root.config(bg="#2c3e50")

    def show_analysis():
        conn = sqlite3.connect('general_inventory.db')
        df = pd.read_sql_query("SELECT name, stock_count FROM products", conn)
        conn.close()
        if df.empty:
            messagebox.showwarning("No Data", "Add products to see analysis!")
            return
        
        graph_win = tk.Toplevel(root)
        graph_win.title("Inventory Analysis")
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.bar(df['name'], df['stock_count'], color='#3498db')
        ax.set_title("Stock Levels Comparison")
        plt.xticks(rotation=45)
        canvas = FigureCanvasTkAgg(fig, master=graph_win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def export_excel():
        conn = sqlite3.connect('general_inventory.db')
        df = pd.read_sql_query("SELECT * FROM products", conn)
        conn.close()
        file_path = filedialog.asksaveasfilename(defaultextension='.xlsx')
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Success", "Exported Successfully!")

    def toggle_theme():
        global is_dark_mode
        if is_dark_mode:
            root.config(bg="white")
            is_dark_mode = False
        else:
            root.config(bg="#2c3e50")
            is_dark_mode = True

    def fetch_data():
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        for item in tree.get_children(): tree.delete(item)
        for row in rows: tree.insert('', tk.END, values=row)
        conn.close()

    def add_item():
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, category, price, stock_count) VALUES (?, ?, ?, ?)",
                       (name_entry.get(), category_entry.get(), price_entry.get(), stock_entry.get()))
        conn.commit()
        conn.close()
        fetch_data()
        messagebox.showinfo("Success", "Product Added!")

    nav_bar = tk.Frame(root, bg="#34495e", height=50)
    nav_bar.pack(fill="x")
    
    tk.Button(nav_bar, text="📊 Analysis", command=show_analysis).pack(side="left", padx=10, pady=10)
    tk.Button(nav_bar, text="📥 Export Excel", command=export_excel).pack(side="left", padx=10, pady=10)
    tk.Button(nav_bar, text="🌓 Theme", command=toggle_theme).pack(side="right", padx=10, pady=10)

    input_frame = tk.LabelFrame(root, text=" Manage Inventory ", bg="#34495e", fg="white", padx=20, pady=10)
    input_frame.pack(pady=20, fill="x", padx=20)

    tk.Label(input_frame, text="Name:", bg="#34495e", fg="white").grid(row=0, column=0)
    name_entry = tk.Entry(input_frame); name_entry.grid(row=0, column=1, padx=10)

    tk.Label(input_frame, text="Stock:", bg="#34495e", fg="white").grid(row=0, column=2)
    stock_entry = tk.Entry(input_frame); stock_entry.grid(row=0, column=3, padx=10)

    tk.Label(input_frame, text="Price:", bg="#34495e", fg="white").grid(row=1, column=0, pady=10)
    price_entry = tk.Entry(input_frame); price_entry.grid(row=1, column=1)

    tk.Label(input_frame, text="Category:", bg="#34495e", fg="white").grid(row=1, column=2)
    category_entry = tk.Entry(input_frame); category_entry.grid(row=1, column=3)

    tk.Button(root, text="➕ Add Product", command=add_item, bg="#27ae60", fg="black", width=20).pack(pady=10)

    columns = ('ID', 'Name', 'Category', 'Price', 'Stock')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns: tree.heading(col, text=col); tree.column(col, width=100, anchor="center")
    tree.pack(pady=20, fill="both", expand=True, padx=20)

    fetch_data()
    root.mainloop()

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("350x250")
tk.Label(login_window, text="RESTRICTED ACCESS", fg="red", font=("Arial", 12, "bold")).pack(pady=10)
tk.Label(login_window, text="Username:").pack()
user_entry = tk.Entry(login_window); user_entry.pack(pady=5)
tk.Label(login_window, text="Password:").pack()
pass_entry = tk.Entry(login_window, show="*"); pass_entry.pack(pady=5)
tk.Button(login_window, text="Login", command=login, bg="#3498db", width=15).pack(pady=20)
login_window.mainloop()