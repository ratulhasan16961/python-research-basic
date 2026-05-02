import sqlite3

def check_low_stock(threshold=10):
    conn = sqlite3.connect('general_inventory.db')
    cursor = conn.cursor()
    cursor.execute("SELECT name, stock_count FROM products WHERE stock_count < ?", (threshold,))
    low_stock_items = cursor.fetchall()

    print("\n=== LOW STOCK ALERT ===")
    if low_stock_items:
        for item in low_stock_items:
            print(f"⚠️  WARNING: {item[0]} is low on stock! Only {item[1]} left.")
    else:
        print("✅ All items are sufficiently stocked.")

    conn.close()

if __name__ == "__main__":
    check_low_stock(threshold=10)