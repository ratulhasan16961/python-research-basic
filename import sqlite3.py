import sqlite3

connection = sqlite3.connect('general_inventory.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        category TEXT,
        price REAL,
        stock_count INTEGER
    )
''')

cursor.execute("SELECT count(*) FROM products")
if cursor.fetchone()[0] == 0:
    items = [
        ('Laptop', 'Electronics', 5000.0, 10),
        ('Keyboard', 'Electronics', 150.0, 25),
        ('Coffee Mug', 'Kitchenware', 25.0, 50),
        ('Desk Lamp', 'Home Office', 45.0, 15)
    ]
    cursor.executemany("INSERT INTO products (item_name, category, price, stock_count) VALUES (?, ?, ?, ?)", items)
    connection.commit()
    print("General products added to system!")

print("\n--- Current Inventory System ---")
cursor.execute("SELECT * FROM products")
for row in cursor.fetchall():
    print(f"ID: {row[0]} | Item: {row[1]} | Category: {row[2]} | Stock: {row[4]}")

connection.close()