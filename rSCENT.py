import sqlite3 as sql
from datetime import datetime

def data():
    con = sql.connect("bilee.db")
    cursor = con.cursor()

    cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   brand TEXT,
                   name TEXT,
                   quantity INTEGER,
                   purchase_price REAL,
                   selling_price REAL,
                   stock INTEGER
                   )
        """)
        
    cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   perfume_id INTEGER,
                   quantity INTEGER,
                   actual_selling_price REAL,
                   payment_method TEXT,
                   sale_date TEXT,
                   FOREIGN KEY (perfume_id) REFERENCES inventory(id)
                   )
            """)
    con.commit()
    con.close()

data()

def add():
    brand = input("\n   Enter perfume brand:   ")
    name = input("\n   Enter perfume name:   ")
    purchase_price = float(input("\n   Enter purchase price:   "))
    quantity = int(input("\n   How many items to add to stock?   "))
    
    con = sql.connect("bilee.db")
    cursor = con.cursor()

    cursor.execute("SELECT id, stock FROM inventory WHERE brand = ? AND name = ? ", (brand, name))
    rezultat = cursor.fetchone()

    if resultado := rezultat:
        perfume_id, old_stock = resultado

        if old_stock is None:
            old_stock = 0
        
        new_stock = old_stock + quantity

        cursor.execute("""
            UPDATE inventory 
            SET stock = ?, purchase_price = ? 
            WHERE id = ?
        """, (new_stock, purchase_price, perfume_id))
        print(f"\n [STOCK UPDATED] {name.upper()} already exists. Added {quantity} items. Total stock: {new_stock}")
    else:
        cursor.execute("""  
        INSERT INTO inventory (brand, name, purchase_price, stock)
        VALUES (?, ?, ?, ?)
    """, (brand, name, purchase_price, quantity))
        
        print(f"\n [NEW PRODUCT] Successfully added {name.upper()} with an initial stock of {quantity} items.")

    con.commit()
    con.close()


def view_stock():
    con = sql.connect("bilee.db")
    cursor = con.cursor()

    cursor.execute("SELECT id, brand, name, stock FROM inventory")
    perfumes = cursor.fetchall()
    con.close()

    if not perfumes:
        print("\n   [Empty Stock] No perfumes found in the database.")
        return
    
    print("\n       --- rSCENT CURRENT STOCK ---")
    print("   ------------------------------------------------")
    print("   ID  |  BRAND       |  NAME             |  STOCK")
    print("   ------------------------------------------------")

    for p in perfumes:
        id_p, brand, name, stock = p

        if stock is None:
            stock = 0
        print(f"   {id_p:<3} |  {brand:<10} |  {name:<16} |  {stock} pcs")
    print("   ------------------------------------------------")

def add_sale():
    con = sql.connect("bilee.db")
    cursor = con.cursor()

    perfume_id = input("\n   Enter sold perfume ID:   ")
    cursor.execute("SELECT name, stock FROM inventory WHERE id = ?", (perfume_id,))
    rezultat = cursor.fetchone()

    if not rezultat:
        print("\n   [ERROR] This perfume does not exist in the database!")
        con.close()
        return
        
    name_perfume, current_stock = rezultat
    quantity_sold = int(input(f"\n   How many bottles of {name_perfume} were sold?   "))

    if current_stock is None or current_stock < quantity_sold:
        print("\n   [INSUFFICIENT STOCK] Not enough items in stock!")
        con.close()
        return
    
    actual_selling_price = float(input("\n   Enter the final selling price:   "))
    payment_method = input("\n   Select payment method (Cash/Card):   ").strip().capitalize()
    sale_date = datetime.now().strftime("%Y-%m-%d  %H:%M")
    
    cursor.execute("""
        INSERT INTO sales (perfume_id, quantity, actual_selling_price, payment_method, sale_date)
                   VALUES(?,?,?,?,?)
    """, (perfume_id, quantity_sold, actual_selling_price, payment_method, sale_date))

    new_stock = current_stock - quantity_sold
    cursor.execute("UPDATE inventory SET stock = ? WHERE id = ?", (new_stock, perfume_id))

    print("\n   [SUCCESS] Sale recorded successfully!")

    con.commit()
    con.close()
    
def profit():   
    con = sql.connect("bilee.db")
    cursor = con.cursor()

    cursor.execute("""
        SELECT
                   SUM(v.quantity * v.actual_selling_price) AS total_revenue,
                   SUM(v.quantity * v.actual_selling_price - v.quantity * i.purchase_price) AS net_profit
                   FROM sales v
                   INNER JOIN inventory i ON v.perfume_id = i.id 
    """)

    rezultat = cursor.fetchone()
    con.close()

    revenue, net_profit = rezultat

    if revenue is None:
        revenue = 0
    if net_profit is None:
        net_profit = 0

    print("\n   --- rSCENT FINANCIAL REPORT ---")
    print("   --------------------------------")
    print(f"   Total Revenue  : {revenue:.2f} lei")
    print(f"   Net Profit     : {net_profit:.2f} lei")
    print("   --------------------------------")

def menu():
    while True:
        print("\n       ---  Welcome to rSCENT ---\n")
        print("   1. Add perfumes to stock")
        print("   2. View stock")
        print("   3. Record a sale")
        print("   4. View profit")
        print("   5. Exit")

        option = input("\n   Choose an option (1-5):  ")

        if option == "1":
            add()
        elif option == "2":
            view_stock()
        elif option == "3":
            add_sale()
        elif option == "4":
            profit()
        elif option == "5":
            print("   Goodbye!\n")
            break
        else:
            print("\n   Invalid option")

menu()