import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sqlite3
import csv

def fetch_data():
    try:
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        
        for item in tree.get_children():
            tree.delete(item)
            
        for row in rows:
            tree.insert('', tk.END, values=row)
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", f"Could not load data: {str(e)}")

def add_product_gui():
    name = name_entry.get()
    category = category_entry.get()
    price = price_entry.get()
    stock = stock_entry.get()

    if name == "" or price == "" or stock == "":
        messagebox.showwarning("Input Error", "Please fill Name, Price, and Stock!")
        return

    try:
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO products (name, category, price, stock_count) VALUES (?, ?, ?, ?)",
                       (name, category, float(price), int(stock)))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"{name} added successfully!")
       
        name_entry.delete(0, tk.END)
        category_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        stock_entry.delete(0, tk.END)
        fetch_data()
    except Exception as e:
        messagebox.showerror("Error", str(e))

def delete_selected():
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showwarning("Selection Error", "Please select an item from the table first!")
        return
    
    item_values = tree.item(selected_item)['values']
    p_id = item_values[0]
    p_name = item_values[1]

    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {p_name}?")
    if confirm:
        try:
            conn = sqlite3.connect('general_inventory.db')
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id = ?", (p_id,))
            conn.commit()
            conn.close()
            fetch_data()
            messagebox.showinfo("Deleted", f"{p_name} has been removed.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

def export_to_csv():
    try:
        conn = sqlite3.connect('general_inventory.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM products")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            messagebox.showwarning("No Data", "Nothing to export!")
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", 
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['ID', 'Name', 'Category', 'Price', 'Stock'])
                writer.writerows(rows)
            messagebox.showinfo("Success", f"Report saved at: {file_path}")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to export: {str(e)}")

root = tk.Tk()
root.title("Ratul's Smart Inventory System")
root.geometry("900x700")

label = tk.Label(root, text="Inventory Dashboard", font=("Arial", 22, "bold"), fg="#2c3e50")
label.pack(pady=20)

input_frame = tk.LabelFrame(root, text=" Product Management ", padx=20, pady=10)
input_frame.pack(pady=10, padx=20, fill="x")

tk.Label(input_frame, text="Name:").grid(row=0, column=0, padx=5, pady=5)
name_entry = tk.Entry(input_frame); name_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Category:").grid(row=0, column=2, padx=5, pady=5)
category_entry = tk.Entry(input_frame); category_entry.grid(row=0, column=3)

tk.Label(input_frame, text="Price:").grid(row=1, column=0, padx=5, pady=5)
price_entry = tk.Entry(input_frame); price_entry.grid(row=1, column=1)

tk.Label(input_frame, text="Stock:").grid(row=1, column=2, padx=5, pady=5)
stock_entry = tk.Entry(input_frame); stock_entry.grid(row=1, column=3)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

btn_add = tk.Button(btn_frame, text="➕ Add Product", command=add_product_gui, width=15, bg="#27ae60")
btn_add.grid(row=0, column=0, padx=10)

btn_delete = tk.Button(btn_frame, text="🗑️ Delete Selected", command=delete_selected, width=15, bg="#c0392b")
btn_delete.grid(row=0, column=1, padx=10)

btn_export = tk.Button(btn_frame, text="📊 Export CSV", command=export_to_csv, width=15, bg="#2980b9")
btn_export.grid(row=0, column=2, padx=10)

columns = ('ID', 'Name', 'Category', 'Price', 'Stock')
tree = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, width=120, anchor="center")
tree.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

fetch_data()

root.mainloop()