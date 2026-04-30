import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

connection = sqlite3.connect('general_inventory.db')
df = pd.read_sql_query("SELECT * FROM products", connection)

plt.figure(figsize=(10, 6))
plt.bar(df['item_name'], df['stock_count'], color='skyblue')

plt.title('Inventory Stock Levels', fontsize=15)
plt.xlabel('Product Name', fontsize=12)
plt.ylabel('Stock Quantity', fontsize=12)

plt.savefig('inventory_graph.png')
print("Graph has been saved as 'inventory_graph.png'")

plt.show()

connection.close()