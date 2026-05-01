import sqlite3

connection = sqlite3.connect('general_inventory.db')
cursor = connection.cursor()

print("--- Add New Product to Inventory ---")

name = input("Enter product name: ")
category = input("Enter category: ")
price = float(input("Enter price: "))
stock_count = int(input("Enter stock count: "))

try:
    cursor.execute('''
        INSERT INTO products (name, category, price, stock_count)
        VALUES (?, ?, ?, ?)
    ''', (name, category, price, stock_count))
 
    connection.commit()
    print(f"\n✅ Success! {name} has been added to the inventory.")

except Exception as e:
    print(f"❌ Error: {e}")

connection.close()