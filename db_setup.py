import sqlite3

connection = sqlite3.connect('general_inventory.db')
cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        price REAL NOT NULL,
        stock_count INTEGER NOT NULL
    )
''')

connection.commit()
connection.close()
print("Database and table 'products' created successfully!")