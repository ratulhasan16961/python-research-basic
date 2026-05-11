import tkinter as tk
from tkinter import ttk, messagebox
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
                       s_name TEXT, s_contact TEXT)''')
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
    global root, nav_bar, input_frame, tree, name_entry, category_entry, price_entry, stock_entry, add_btn
    
    root = tk.Tk()
    root.title("Ratul's Enterprise Inventory v6.0")
    root.geometry("1100x850")
    root.config(bg="#2c3e50")

    def toggle_theme():
        current_bg = root.cget("bg")
        if current_bg == "#2c3e50": 
            root.config(bg="#ecf0f1")
            nav_bar.config(bg="#bdc3c7")
            input_frame.config(bg="#ecf0f1", fg="black")
            add_btn.config(fg="black") 
        else: 
            root.config(bg="#2c3e50")
            nav_bar.config(bg="#34495e")
            input_frame.config(bg="#34495e", fg="white")
            add_btn.config(fg="black") 

    def generate_bill_pdf():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a product first!")
            return
        
        item = tree.item(selected)['values']
        p_name, p_price = item[1], item[3]
        
        bill_win = tk.Toplevel(root)
        bill_win.title("Receipt Details")
        tk.Label(bill_win, text=f"Product: {p_name}").pack(pady=5)
        tk.Label(bill_win, text="Customer Name:").pack()
        c_entry = tk.Entry(bill_win); c_entry.pack()
        tk.Label(bill_win, text="Quantity:").pack()
        q_entry = tk.Entry(bill_win); q_entry.pack()

        def save_pdf():
            try:
                c_name = c_entry.get()
                qty = int(q_entry.get())
                total = p_price * qty
                filename = f"Receipt_{c_name}.pdf"
                
                c = canvas.Canvas(filename)
                c.setFont("Helvetica-Bold", 20); c.drawString(100, 750, "RATUL'S SMART INVENTORY")
                c.setFont("Helvetica", 12); c.drawString(100, 720, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
                c.drawString(100, 680, f"Customer: {c_name}")
                c.drawString(100, 660, f"Product: {p_name} x {qty}")
                c.drawString(100, 640, f"Total Amount: ${total}")
                c.save()
                messagebox.showinfo("Success", f"Bill Saved as {filename}")
                bill_win.destroy()
            except:
                messagebox.showerror("Error", "Invalid quantity!")

        tk.Button(bill_win, text="Generate", command=save_pdf, bg="#e67e22").pack(pady=10)

    def open_suppliers():
        s_win = tk.Toplevel(root)
        s_win.title("Suppliers")
        s_win.geometry("500x400")
        tk.Label(s_win, text="Supplier Name:").pack()
        sn = tk.Entry(s_win); sn.pack()
        tk.Label(s_win, text="Contact:").pack()
        sc = tk.Entry(s_win); sc.pack()

        def add_s():
            conn = sqlite3.connect('general_inventory.db')
            conn.execute("INSERT INTO suppliers (s_name, s_contact) VALUES (?,?)", (sn.get(), sc.get()))
            conn.commit(); conn.close()
            messagebox.showinfo("Success", "Supplier Added")
            s_win.destroy()

        tk.Button(s_win, text="Add", command=add_s).pack(pady=5)

    def show_analysis():
        conn = sqlite3.connect('general_inventory.db')
        df = pd.read_sql_query("SELECT name, stock_count FROM products", conn)
        conn.close()
        if not df.empty:
            graph_win = tk.Toplevel(root)
            fig, ax = plt.subplots(figsize=(5, 4))
            ax.bar(df['name'], df['stock_count'], color='#3498db')
            canvas_plot = FigureCanvasTkAgg(fig, master=graph_win)
            canvas_plot.draw(); canvas_plot.get_tk_widget().pack()

    nav_bar = tk.Frame(root, bg="#34495e", height=50)
    nav_bar.pack(fill="x")
    
    tk.Button(nav_bar, text="📊 Analysis", command=show_analysis).pack(side="left", padx=10, pady=10)
    tk.Button(nav_bar, text="🚚 Suppliers", command=open_suppliers).pack(side="left", padx=10)
    tk.Button(nav_bar, text="🧾 Create Bill", command=generate_bill_pdf).pack(side="left", padx=10)
    tk.Button(nav_bar, text="🌓 Theme", command=toggle_theme).pack(side="right", padx=10)

    input_frame = tk.LabelFrame(root, text=" Manage Inventory ", bg="#34495e", fg="white", padx=20, pady=10)
    input_frame.pack(pady=20, fill="x", padx=20)

    tk.Label(input_frame, text="Name:", bg="#34495e", fg="white").grid(row=0, column=0)
    name_entry = tk.Entry(input_frame); name_entry.grid(row=0, column=1, padx=5)
    tk.Label(input_frame, text="Stock:", bg="#34495e", fg="white").grid(row=0, column=2)
    stock_entry = tk.Entry(input_frame); stock_entry.grid(row=0, column=3, padx=5)
    tk.Label(input_frame, text="Price:", bg="#34495e", fg="white").grid(row=1, column=0)
    price_entry = tk.Entry(input_frame); price_entry.grid(row=1, column=1, padx=5)
    tk.Label(input_frame, text="Category:", bg="#34495e", fg="white").grid(row=1, column=2)
    category_entry = tk.Entry(input_frame); category_entry.grid(row=1, column=3, padx=5)

    def add_product():
        conn = sqlite3.connect('general_inventory.db')
        conn.execute("INSERT INTO products (name, category, price, stock_count) VALUES (?,?,?,?)",
                     (name_entry.get(), category_entry.get(), price_entry.get(), stock_entry.get()))
        conn.commit(); conn.close()
        refresh_table()

    add_btn = tk.Button(root, text="➕ Add Product", command=add_product, bg="#27ae60", fg="black", width=20)
    add_btn.pack(pady=10)

    columns = ('ID', 'Name', 'Category', 'Price', 'Stock')
    tree = ttk.Treeview(root, columns=columns, show='headings')
    for col in columns: tree.heading(col, text=col); tree.column(col, width=100, anchor="center")
    tree.pack(pady=10, fill="both", expand=True, padx=20)

    def refresh_table():
        for i in tree.get_children(): tree.delete(i)
        conn = sqlite3.connect('general_inventory.db')
        for row in conn.execute("SELECT * FROM products"): tree.insert('', tk.END, values=row)
        conn.close()

    refresh_table()
    root.mainloop()

login_window = tk.Tk()
login_window.title("Login")
login_window.geometry("300x250")
login_window.config(bg="#2c3e50") 

tk.Label(login_window, text="Username:", bg="#2c3e50", fg="white").pack(pady=5)
user_entry = tk.Entry(login_window)
user_entry.pack(pady=5)

tk.Label(login_window, text="Password:", bg="#2c3e50", fg="white").pack(pady=5)
pass_entry = tk.Entry(login_window, show="*")
pass_entry.pack(pady=5)

tk.Button(login_window, text="Login", command=login, bg="#3498db", fg="black", width=15).pack(pady=20)

login_window.mainloop()