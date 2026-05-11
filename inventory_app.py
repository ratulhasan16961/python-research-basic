import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from reportlab.pdfgen import canvas
from datetime import datetime

def create_table():
    conn = sqlite3.connect('general_inventory.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS products
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       name TEXT, category TEXT, price REAL, stock_count INTEGER)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS suppliers
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                       s_name TEXT, s_contact TEXT, s_product TEXT)''')
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
    global tree, s_tree, root, name_entry, category_entry, price_entry, stock_entry
    root = tk.Tk()
    root.title("Ratul's Enterprise Inventory v6.0")
    root.geometry("1100x900")
    root.config(bg="#2c3e50")

    def generate_bill_pdf():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product from the table first!")
            return
        
        item = tree.item(selected)['values']
        p_name, p_price = item[1], item[3]
     
        bill_win = tk.Toplevel(root)
        bill_win.title("Generate Receipt")
        tk.Label(bill_win, text=f"Product: {p_name}").pack(pady=5)
        tk.Label(bill_win, text="Customer Name:").pack()
        c_entry = tk.Entry(bill_win); c_entry.pack()
        tk.Label(bill_win, text="Quantity:").pack()
        q_entry = tk.Entry(bill_win); q_entry.pack()

        def save_pdf():
            c_name = c_entry.get()
            qty = int(q_entry.get())
            total = p_price * qty
            filename = f"Receipt_{c_name}_{datetime.now().strftime('%H%M%S')}.pdf"
            
            c = canvas.Canvas(filename)
            c.setFont("Helvetica-Bold", 20); c.drawString(100, 750, "RATUL'S SMART INVENTORY")
            c.setFont("Helvetica", 12); c.drawString(100, 730, f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            c.line(100, 720, 500, 720)
            c.drawString(100, 700, f"Customer: {c_name}")
            c.drawString(100, 680, f"Product: {p_name}")
            c.drawString(100, 660, f"Quantity: {qty}")
            c.drawString(100, 640, f"Unit Price: ${p_price}")
            c.setFont("Helvetica-Bold", 14); c.drawString(100, 610, f"Total Amount: ${total}")
            c.save()
            messagebox.showinfo("Success", f"Bill Saved: {filename}")
            bill_win.destroy()

        tk.Button(bill_win, text="Print PDF", command=save_pdf, bg="#e67e22").pack(pady=10)

    def open_suppliers():
        s_win = tk.Toplevel(root)
        s_win.title("Supplier Database")
        s_win.geometry("600x500")

        tk.Label(s_win, text="Supplier Name:").pack()
        sn_entry = tk.Entry(s_win); sn_entry.pack()
        tk.Label(s_win, text="Contact No:").pack()
        sc_entry = tk.Entry(s_win); sc_entry.pack()

        def add_supplier():
            conn = sqlite3.connect('general_inventory.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO suppliers (s_name, s_contact) VALUES (?, ?)", (sn_entry.get(), sc_entry.get()))
            conn.commit(); conn.close()
            fetch_suppliers()

        def fetch_suppliers():
            conn = sqlite3.connect('general_inventory.db')
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM suppliers")
            rows = cursor.fetchall()
            for item in s_tree.get_children(): s_tree.delete(item)
            for row in rows: s_tree.insert('', tk.END, values=row)
            conn.close()

        tk.Button(s_win, text="Add Supplier", command=add_supplier, bg="#27ae60").pack(pady=5)
        
        cols = ('ID', 'Name', 'Contact')
        global s_tree
        s_tree = ttk.Treeview(s_win, columns=cols, show='headings')
        for col in cols: s_tree.heading(col, text=col)
        s_tree.pack(fill="both", expand=True)
        fetch_suppliers()

    def show_analysis():
        conn = sqlite3.connect('general_inventory.db')
        df = pd.read_sql_query("SELECT name, stock_count FROM products", conn)
        conn.close()
        if df.empty: return
        
        graph_win = tk.Toplevel(root)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.bar(df['name'], df['stock_count'], color='#3498db')
        canvas_plot = FigureCanvasTkAgg(fig, master=graph_win)
        canvas_plot.draw(); canvas_plot.get_tk_widget().pack()

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
        conn.commit(); conn.close()
        fetch_data()

    nav_bar = tk.Frame(root, bg="#34495e", height=50)
    nav_bar.pack(fill="x")
    
    tk.Button(nav_bar, text="📊 Analysis", command=show_analysis).pack(side="left", padx=10)
    tk.Button(nav_bar, text="🚚 Suppliers", command=open_suppliers).pack(side="left", padx=10)
    tk.Button(nav_bar, text="🧾 Create Bill", command=generate_bill_pdf, bg="#e67e22").pack(side="left", padx=10)

    input_frame = tk.LabelFrame(root, text=" Product Management ", bg="#34495e", fg="white", padx=20, pady=10)
    input_frame.pack(pady=20, fill="x", padx=20)

    tk.Label(input_frame, text="Name:", bg="#34495e", fg="white").grid(row=0, column=0)
    name_entry = tk.Entry(input_frame); name_entry.grid(row=0, column=1)
    tk.Label(input_frame, text="Stock:", bg="#34495e", fg="white").grid(row=0, column=2)
    stock_entry = tk.Entry(input_frame); stock_entry.grid(row=0, column=3)
    tk.Label(input_frame, text="Price:", bg="#34495e", fg="white").grid(row=1, column=0)
    price_entry = tk.Entry(input_frame); price_entry.grid(row=1, column=1)
    tk.Label(input_frame, text="Category:", bg="#34495e", fg="white").grid(row=1, column=2)
    category_entry = tk.Entry(input_frame); category_entry.grid(row=1, column=3)

    tk.Button(root, text="➕ Add Product", command=add_item, bg="#27ae60", width=20).pack(pady=10)

    columns = ('ID', 'Name', 'Category', 'Price', 'Stock')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns: tree.heading(col, text=col); tree.column(col, width=100, anchor="center")
    tree.pack(pady=20, fill="both", expand=True, padx=20)

    fetch_data()
    root.mainloop()

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x250")
tk.Label(login_window, text="Username:").pack()
user_entry = tk.Entry(login_window); user_entry.pack()
tk.Label(login_window, text="Password:").pack()
pass_entry = tk.Entry(login_window, show="*"); pass_entry.pack()
tk.Button(login_window, text="Login", command=login, bg="#3498db").pack(pady=20)
login_window.mainloop()