import sqlite3
import pandas as pd

connection = sqlite3.connect('general_inventory.db')

query = "SELECT * FROM products"
df = pd.read_sql_query(query, connection)

print("--- Data Table using Pandas ---")
print(df)

print(f"\nTotal items in stock: {df['stock_count'].sum()}")

avg_price = df.groupby('category')['price'].mean()
print("\nAverage Price per Category:")
print(avg_price)

connection.close()