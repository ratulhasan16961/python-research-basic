import sqlite3

def update_product():
    conn = sqlite3.connect('general_inventory.db')
    cursor = conn.cursor()

    p_id = input("Enter Product ID to update: ")
    new_price = input("Enter new price (leave blank to skip): ")
    new_stock = input("Enter new stock count (leave blank to skip): ")

    if new_price:
        cursor.execute("UPDATE products SET price = ? WHERE id = ?", (new_price, p_id))
    if new_stock:
        cursor.execute("UPDATE products SET stock_count = ? WHERE id = ?", (new_stock, p_id))

    conn.commit()
    if cursor.rowcount > 0:
        print("Successfully updated!")
    else:
        print("Product ID not found.")
    
    conn.close()

if __name__ == "__main__":
    update_product()