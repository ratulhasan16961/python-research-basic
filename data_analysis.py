import sqlite3
import pandas as pd

connection = sqlite3.connect('general_inventory.db')

query = "SELECT * FROM products"
df = pd.read_sql_query(query, connection)

print("--- Inventory Analysis Table ---")
print(df)

print(f"\nTotal Stock Quantity: {df['stock_count'].sum()}")
print("\nAverage Price per Category:")
print(df.groupby('category')['price'].mean())

connection.close()