"""
SAQA 114048 – Practical Assessment
Python console application that connects to SQL Server (SQLEXPRESS)
to perform CRUD operations on the Products table inside MiniStore.
Author: Senzo
"""

import pyodbc

# -----------------------------------------------------------
# 1) Connection string used by every database function
# -----------------------------------------------------------
CONN = (
    "Driver={ODBC Driver 17 for SQL Server};"
    "Server=localhost\\SQLEXPRESS;"
    "Database=MiniStore;"
    "Trusted_Connection=yes;"
)

# -----------------------------------------------------------
# 2) Helper: open & return a live SQL Server connection
# -----------------------------------------------------------
def conn():
    """Return an open pyodbc connection to MiniStore."""
    return pyodbc.connect(CONN)


# -----------------------------------------------------------
# 3) Main menu loop – keeps running until user chooses 0
# -----------------------------------------------------------
def menu():
    """Display menu and dispatch to the correct CRUD function."""
    while True:
        print("\n1 List products  2 Add  3 Edit  4 Delete  0 Exit")
        ch = input("> ")
        if ch == "1":
            list_products()
        elif ch == "2":
            add_product()
        elif ch == "3":
            edit_product()
        elif ch == "4":
            delete_product()
        elif ch == "0":
            break
        else:
            print("Invalid option")


# -----------------------------------------------------------
# 4) READ – list all products rows
# -----------------------------------------------------------
def list_products():
    """Fetch and display every row from Products table."""
    sql = "SELECT ProductID, Name, Price FROM Products"
    with conn() as c:
        rows = c.cursor().execute(sql).fetchall()
        for pid, name, price in rows:
            print(f"{pid} | {name:<10} | R{price}")


# -----------------------------------------------------------
# 5) CREATE – insert a new product
# -----------------------------------------------------------
def add_product():
    """Prompt user for product details and insert new record."""
    name = input("Name: ")
    price = float(input("Price: "))
    sql = "INSERT INTO Products (Name, Price) VALUES (?,?)"
    with conn() as c:
        c.cursor().execute(sql, name, price)
        c.commit()
    print("Product added.")


# -----------------------------------------------------------
# 6) UPDATE – modify an existing product
# -----------------------------------------------------------
def edit_product():
    """Prompt for ProductID, new name & price, then update."""
    pid = int(input("ProductID to edit: "))
    name = input("New name: ")
    price = float(input("New price: "))
    sql = "UPDATE Products SET Name=?, Price=? WHERE ProductID=?"
    with conn() as c:
        rows = c.cursor().execute(sql, name, price, pid).rowcount
        c.commit()
    print("Updated." if rows else "ID not found.")


# -----------------------------------------------------------
# 7) DELETE – remove a product
# -----------------------------------------------------------
def delete_product():
    """Prompt for ProductID and delete the matching row."""
    pid = int(input("ProductID to delete: "))
    sql = "DELETE FROM Products WHERE ProductID=?"
    with conn() as c:
        rows = c.cursor().execute(sql, pid).rowcount
        c.commit()
    print("Deleted." if rows else "ID not found.")


# -----------------------------------------------------------
# 8) Entry point – start the interactive menu
# -----------------------------------------------------------
if __name__ == "__main__":
    menu()