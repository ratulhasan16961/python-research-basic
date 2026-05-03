import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv


def fetch_data(query="SELECT * FROM products"):
    try:
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert('', tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Load failed: {str(e)}")

def search_product():
    search_term = search_entry.get()
    if search_term == "":
        fetch_data()
    else:
        query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%' OR category LIKE '%{search_term}%'"
        fetch_data(query)

def check_low_stock():
    conn = sqlite3.connect('general_inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, stock_count FROM products WHERE stock_count < 10")
    low_stock_items = cursor.fetchall()
    conn.close()
    
    if low_stock_items:
        items_list = "\n".join([f"- {item[0]} (Stock: {item[1]})" for item in low_stock_items])
        messagebox.showwarning("Low Stock Alert", f"The following items are running low:\n\n{items_list}")

def add_product_gui():
    name, cat, price, stock = name_entry.get(), category_entry.get(), price_entry.get(), stock_entry.get()
    if not (name and price and stock):
        messagebox.showwarning("Input Error", "Fill all fields!")
        return
    try:
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, category, price, stock_count) VALUES (?, ?, ?, ?)",
                       (name, cat, float(price), int(stock)))
        conn.commit()
        conn.close()
        for entry in (name_entry, category_entry, price_entry, stock_entry): entry.delete(0, tk.END)
        fetch_data()
        messagebox.showinfo("Success", "Product added!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_selected():
    selected = tree.selection()
    if not selected:
        messagebox.showwarning("Error", "Select an item first!")
        return
    item = tree.item(selected)['values']
    if messagebox.askyesno("Confirm", f"Delete {item[1]}?"):
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM products WHERE id = ?", (item[0],))
        conn.commit()
        conn.close()
        fetch_data()

def export_to_csv():
    conn = sqlite3.connect('general_inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM products")
    rows = cursor.fetchall()
    conn.close()
    if not rows: return
    path = filedialog.asksaveasfilename(defaultextension=".csv")
    if path:
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['ID', 'Name', 'Category', 'Price', 'Stock'])
            writer.writerows(rows)
        messagebox.showinfo("Success", "Saved!")

root = tk.Tk()
root.title("Ratul's Smart Inventory v2.0")
root.geometry("900x750")

search_frame = tk.Frame(root)
search_frame.pack(pady=10)

tk.Label(search_frame, text="Search:").pack(side="left", padx=5)
search_entry = tk.Entry(search_frame, width=30)
search_entry.pack(side="left", padx=5)
tk.Button(search_frame, text="🔍 Search", command=search_product).pack(side="left", padx=5)
tk.Button(search_frame, text="🔄 Reset", command=fetch_data).pack(side="left", padx=5)

input_frame = tk.LabelFrame(root, text=" Product Management ", padx=10, pady=10)
input_frame.pack(pady=10, padx=20, fill="x")

tk.Label(input_frame, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(input_frame); name_entry.grid(row=0, column=1)
tk.Label(input_frame, text="Stock:").grid(row=0, column=2)
stock_entry = tk.Entry(input_frame); stock_entry.grid(row=0, column=3)
tk.Label(input_frame, text="Price:").grid(row=1, column=0)
price_entry = tk.Entry(input_frame); price_entry.grid(row=1, column=1)
tk.Label(input_frame, text="Category:").grid(row=1, column=2)
category_entry = tk.Entry(input_frame); category_entry.grid(row=1, column=3)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Add", command=add_product_gui, width=12, bg="green").pack(side="left", padx=5)
tk.Button(btn_frame, text="Delete", command=delete_selected, width=12, bg="red").pack(side="left", padx=5)
tk.Button(btn_frame, text="Export CSV", command=export_to_csv, width=12, bg="blue").pack(side="left", padx=5)

columns = ('ID', 'Name', 'Category', 'Price', 'Stock')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns: tree.heading(col, text=col); tree.column(col, width=100, anchor="center")
tree.pack(pady=10, fill="both", expand=True)

fetch_data()
root.after(1000, check_low_stock) 

root.mainloop()