import sqlite3

def delete_product():
    conn = sqlite3.connect('general_inventory.db')
    cursor = conn.cursor()

    p_id = input("Enter Product ID to delete: ")
    
    confirm = input(f"Are you sure you want to delete ID {p_id}? (yes/no): ")
    
    if confirm.lower() == 'yes':
        cursor.execute("DELETE FROM products WHERE id = ?", (p_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print("Product deleted successfully.")
        else:
            print("Product ID not found.")
    else:
        print("Deletion cancelled.")

    conn.close()

if __name__ == "__main__":
    delete_product()