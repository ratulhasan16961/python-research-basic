import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
connection = sqlite3.connect('general_inventory.db')
df = pd.read_sql_query("SELECT name, stock_count FROM products", connection)
connection.close()
plt.bar(df['name'], df['stock_count'], color='skyblue')
plt.xlabel('Product Name')
plt.ylabel('Stock Quantity')
plt.title('Current Inventory Stock Levels')
plt.savefig('inventory_graph.png')
print("Graph saved as inventory_graph.png!")