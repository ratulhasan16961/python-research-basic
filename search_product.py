import sqlite3

def search_product():
    conn = sqlite3.connect('general_inventory.db')
    cursor = conn.cursor()

    name = input("Enter product name to search: ")

    cursor.execute("SELECT * FROM products WHERE name LIKE ?", ('%' + name + '%',))
    results = cursor.fetchall()

    if results:
        print(f"\n--- Results for '{name}' ---")
        print(f"{'ID':<5} {'Name':<15} {'Category':<15} {'Price':<10} {'Stock':<5}")
        print("-" * 50)
        for row in results:
            print(f"{row[0]:<5} {row[1]:<15} {row[2]:<15} {row[3]:<10} {row[4]:<5}")
    else:
        print(f"\nNo product found with the name '{name}'.")

    conn.close()

if __name__ == "__main__":
    search_product()