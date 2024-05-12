import mysql.connector
from datetime import datetime
import math
from tabulate import tabulate

# create a connection to the mySQL database
connection = mysql.connector.connect(host='localhost',
                                     user='******',
                                     password='***********',
                                     database='Inventory_Management_System')

#create a cursor for the database
cursor = connection.cursor()

# create an SQL query to create a product table
cursor.execute("""
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    sku VARCHAR(20) UNIQUE,
    description VARCHAR(100),
    price INT,
    quantity INT
)""")

# create an SQL query to create a supplier table
cursor.execute("""
CREATE TABLE IF NOT EXISTS suppliers(
id INT AUTO_INCREMENT PRIMARY KEY,
name VARCHAR(50) UNIQUE,
address VARCHAR(100),
phone_number VARCHAR(20),
email VARCHAR(50)
)""")

# create an SQL query to create an order table
cursor.execute("""
CREATE TABLE IF NOT EXISTS orders(
id INT AUTO_INCREMENT PRIMARY KEY,
product_id INT,
product_name VARCHAR(50),
quantity INT,
date_ordered DATE,
FOREIGN KEY (product_id) REFERENCES products(id)
)""")

# commit changes in the system
connection.commit()


# create a class named Products
class Products:

    def __init__(self, name, sku, description, price, quantity):
        self.name = name
        self.sku = sku
        self.description = description
        self.price = price
        self.quantity = quantity


# Create a class name Suppliers for storing the details of the supplier
class Suppliers:

    def __init__(self, name, address, phone_number, email):
        self.name = name
        self.address = address
        self.phone_number = phone_number
        self.email = email


# Create a class name Orders for storing the details of the orders
class Orders:

    def __init__(self, product_id, product_name, quantity, date_ordered):
        self.product_id = product_id
        self.product_name = product_name
        self.quantity = quantity
        self.date_ordered = date_ordered


class InventoryManagementSystem:

    # function for adding product details to the inventory
    def add_product(self, product):
        try:
            sql = """
            INSERT INTO products (name, sku, description, price, quantity)
            VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(sql,
                           (product.name, product.sku, product.description,
                            product.price, product.quantity))
            connection.commit()
            print("\nProduct details registered successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # to generate the product list stored in the inventory system
    def products_report(self):
        try:
            sql = """SELECT name, sku, description, price, quantity FROM products"""
            cursor.execute(sql)
            rows = cursor.fetchall()
            if rows:
                headers = [
                    "Product Name", "SKU", "Description", "Price per Quantity",
                    "Quantity"
                ]
                print(tabulate(rows, headers=headers, tablefmt="grid"))
            else:
                print("No products found in inventory.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # to get the details of the individual product
    def product_details(self, name):
        try:
            sql = """SELECT name, sku, description, price, quantity 
                     FROM products 
                     WHERE name = %s"""
            cursor.execute(sql, (name, ))
            row = cursor.fetchone()
            if row:
                product = Products(row[0], row[1], row[2], row[3], row[4])
                print(f"\nProduct Name: {product.name}")
                print(f"\nSKU: {product.sku}")
                print(f"\nDescription: {product.description}")
                print(f"\nPrice per Quantity: {product.price}")
                print(f"\nQuantity: {product.quantity}")
            else:
                print(f"\nNo product found with name '{name}.'")
        except:
            print("Error: Unable to retrieve product details.")

    # to add more quantity of the product in the stock
    def update_product_quantity(self, name, quantity):
        try:
            sql_select = """SELECT name, sku, description, price, quantity
                            FROM products
                            WHERE name = %s"""
            cursor.execute(sql_select, (name, ))
            row = cursor.fetchone()
            if row:
                product = Products(row[0], row[1], row[2], row[3], row[4])
                product.quantity = product.quantity + quantity
                sql_update = """UPDATE products
                                SET quantity = %s
                                WHERE name = %s"""
                cursor.execute(sql_update, (product.quantity, name))
                connection.commit()
                print(
                    f"\nUpdated quantity of {product.name} to {product.quantity}."
                )
            else:
                print(f"\nNo product found with name '{name}'.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_product(self, name):
        try:
            sql_select = """SELECT name, sku, description, price, quantity
                        FROM products
                        WHERE name = %s"""
            cursor.execute(sql_select, (name, ))
            row = cursor.fetchone()  # Fetch a single row
            if row:
                sql_delete = """DELETE FROM products WHERE name = %s"""
                cursor.execute(sql_delete, (name, ))
                connection.commit()
                print(
                    f"\nProduct '{name}' has been deleted from the inventory.")
            else:
                print(f"\nNo product found with name '{name}'.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # adding supplier details to the inventory system
    def add_supplier(self, supplier):
        try:
            sql = """
                  INSERT INTO suppliers (name, address, phone_number, email)
                  VALUES (%s, %s, %s, %s)"""
            cursor.execute(sql, (supplier.name, supplier.address,
                                 supplier.phone_number, supplier.email))
            connection.commit()
            print("\nSupplier details registered successfully.")
        except mysql.connector.Error as err:
            if err.errno == 1062:  # Check for duplicate entry error
                print("\nSupplier with the same name already exists.")
            else:
                print(f"Error: {err}")

    # function to find the supplier detail
    def supplier_details(self, name):
        try:
            sql = """SELECT name, address, phone_number, email
                     FROM suppliers 
                     WHERE name = %s"""
            cursor.execute(sql, (name, ))
            row = cursor.fetchone()
            if row:
                supplier = Suppliers(row[0], row[1], row[2], row[3])
                print(f"\nSupplier Name: {supplier.name}")
                print(f"\nAddress: {supplier.address}")
                print(f"\nPhone Number: {supplier.phone_number}")
                print(f"\nEmail ID: {supplier.email}")
            else:
                print("\nNo supplier found with the given name.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # function for generating the supplier report
    def supplier_report(self):
        try:
            sql = """SELECT name, address, phone_number, email
                     FROM suppliers """
            cursor.execute(sql)
            rows = cursor.fetchall()
            if rows:
                headers = [
                    "Supplier Name", "Address", "Phone Number", "Email ID"
                ]
                print(tabulate(rows, headers=headers, tablefmt="grid"))
            else:
                print("No products found in inventory.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # update supplier details to the inventory
    def update_supplier(self, name, new_address, new_phone_number, new_email):
        try:
            sql_select = """SELECT name, address, phone_number, email
                        FROM suppliers
                        WHERE name = %s"""
            cursor.execute(sql_select, (name, ))
            rows = cursor.fetchall()  # Fetch all rows
            for row in rows:
                supplier = Suppliers(row[0], row[1], row[2], row[3])
                supplier.address = new_address
                supplier.phone_number = new_phone_number
                supplier.email = new_email
                sql_update = """UPDATE suppliers
                                SET address = %s,
                                    phone_number = %s,
                                    email = %s
                                WHERE name = %s"""
                cursor.execute(sql_update,
                               (supplier.address, supplier.phone_number,
                                supplier.email, name))
                connection.commit()
                print(f"\nUpdated supplier details for {supplier.name}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_supplier(self, name):
        try:
            sql_select = """SELECT name, address, phone_number, email
                        FROM suppliers
                        WHERE name = %s"""
            cursor.execute(sql_select, (name, ))
            row = cursor.fetchall()  # Fetch a single row
            if row:
                sql_delete = """DELETE FROM suppliers WHERE name = %s"""
                cursor.execute(sql_delete, (name, ))
                connection.commit()
                print(
                    f"\nProduct '{name}' has been deleted from the inventory.")
            else:
                print(f"\nNo product found with name '{name}'.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # function to check the availability of the product for order
    def check_product_availability(self, product_id, product_name, quantity):
        try:
            sql = """SELECT name, sku, description, price, quantity
                     FROM products
                     WHERE id = %s"""
            cursor.execute(sql, (product_id, ))
            row = cursor.fetchone()
            if row:
                product = Products(row[0], row[1], row[2], row[3], row[4])
                if product.quantity >= quantity:
                    return True
                else:
                    return False
            else:
                # Product with the given id not found
                print(f"No product found with id '{product_id}'.")
                return False
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return False  # Or raise an exception depending on your error handling strategy
        finally:
            cursor.fetchall()  # Consume any remaining results

    # function for adding order details in the inventory system
    def add_order(self, order):
        try:
            if self.check_product_availability(order.product_id,
                                               order.product_name,
                                               order.quantity):
                sql = """INSERT INTO orders(product_id, product_name, quantity, date_ordered)
                         VALUES (%s, %s, %s, %s)"""
                cursor.execute(sql, (order.product_id,
                                     order.product_name,
                                     order.quantity,
                                     order.date_ordered,))
                connection.commit()
                print("\nOrder details has been registered to the system")
            else:
                print("\nInsufficient quantity of the product in stock")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # to generate the product list stored in the inventory system
    def orders_report(self):
        try:
            sql = """SELECT product_id, product_name, quantity, date_ordered
                     FROM orders"""
            cursor.execute(sql)
            rows = cursor.fetchall()
            if rows:
                headers = [
                    "Product ID", "Product Name", "Quantity", "Date Ordered"
                ]
                print(tabulate(rows, headers=headers, tablefmt="grid"))
            else:
                print("No order found in inventory.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # to get the details of the individual product
    def order_details(self, name):
        try:
            sql = """SELECT product_id, product_name, quantity, date_ordered
                     FROM orders 
                     WHERE product_name = %s"""
            cursor.execute(sql, (name, ))
            row = cursor.fetchone()
            if row:
                order = Orders(row[0], row[1], row[2], row[3])
                print(f"\nProduct ID: {order.product_id}")
                print(f"\nProduct Name: {order.product_name}")
                print(f"\nQuantity: {order.quantity}")
                print(f"\nOrdered date: {order.date_ordered}")
            else:
                print(f"\nNo order found with name '{name}'.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # to update the quantity of the order either increase or decrease depending upon the user choice
    def update_order(self, name, quantity, choice):
        try:
            sql_select = """SELECT product_id, product_name, quantity, date_ordered
                            FROM orders
                            WHERE product_name = %s"""
            cursor.execute(sql_select, (name, ))
            rows = cursor.fetchall()  # Use fetchall to get all matching rows
            for row in rows:  # Iterate over each row fetched
                order = Orders(row[0], row[1], row[2], row[3])
                if choice == "1":
                    order.quantity += quantity
                else:
                    order.quantity -= quantity
                order.date_ordered = datetime.today().strftime("%Y-%m-%d")
                sql_update = """UPDATE orders
                                SET quantity = %s,
                                    date_ordered = %s
                                WHERE product_name = %s"""
                cursor.execute(sql_update, (order.quantity, 
                                            order.date_ordered, name))
                connection.commit()
                print(f"\nUpdated order details for {order.product_name}.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def delete_order(self, name):
        try:
            sql_select = """SELECT product_id, product_name, quantity, date_ordered
                            FROM orders
                            WHERE product_name = %s"""
            cursor.execute(sql_select, (name, ))
            rows = cursor.fetchall()  # Fetch all rows
            if rows:
                sql_delete = """DELETE FROM orders WHERE product_name = %s"""
                cursor.execute(sql_delete, (name, ))
                connection.commit()
                print(f"\nOrder for product '{name}' has been deleted from the inventory.")
            else:
                print(f"\nNo order found for product '{name}'.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


    # to delete the entire data from the database
    def empty_database(self):
        try:
            sql = "DELETE FROM products"
            cursor.execute(sql)
            connection.commit()
            self.reset_auto_increment()
            print("Database emptied successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    # to reset the auto-increement index of the thing
    def reset_auto_increment(self):
        try:
            sql = "ALTER TABLE products AUTO_INCREMENT = 1"
            cursor.execute(sql)
            connection.commit()
            print("Auto-increment serial number reset successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")

    def close_connection(self):
        try:
            # Fetch all remaining results to ensure the cursor is empty
            while cursor.fetchone() is not None:
                pass
            cursor.close()
            connection.close()
            print("\nConnection is closed successfully.")
        except mysql.connector.Error as err:
            print(f"Error: {err}")


# Example usage of the above code
if __name__ == "__main__":

    # Creating the instance of the class
    inventory = InventoryManagementSystem()
    while True:
        print("\nWelcome to the Inventory Management System")
        print("\n1. Product Management System")
        print("\n2. Supplier Management System")
        print("\n3. Order Management System")
        print("\n4. Exit the Inventory Management System")
        choice = input("\nEnter your choice: ")

        if choice == "1":
          while True:
            print("\n* * * Welcome to the Products Management System * * *")
            print("\n_____________________________________________________")
            print("\n1. Adding Product Details")
            print("\n2. Get Product Details")
            print("\n3. Generate Inventory Report")
            print("\n4. Update Product Quantity")
            print("\n5. Remove Product")
            print("\n6. Exit")
            choice2 = input("\nEnter your choice: ")

            if choice2 == "1":
              var = True
              while var:
                name = input("\nEnter the name of the product: ")
                sku = input("\nEnter the sku of the product: ")
                description = input("\nEnter the description of the product: ")
                price = float(input("\nEnter the price of the product: "))
                quantity = int(input("\nEnter the quantity of the product: "))
                product = Products(name, sku, description, price, quantity)
                inventory.add_product(product)
                variable = input("Do you want to add more products? (y/n)")
                if variable in ['Yes','y','yes','YES','Y']:
                  var = True
                else:
                  var = False
            
            elif choice2 == '2':
              name = input("\nEnter the name of the product: ")
              print("\nProduct Details are as follows:")
              inventory.product_details(name)

            elif choice2 == '3':
                print("\nInventory Report for the products are as follows:")
                inventory.products_report()

            elif choice2 == '4':
              name = input("\nEnter the name of the product: ")
              quantity = int(input("\nEnter the quantity to be updated: "))
              inventory.update_product_quantity(name, quantity)

            elif choice2 == '5':
              name = input("\nEnter the name of the product you want to remove: ")
              inventory.delete_product(name)

            elif choice2 == '6':
              break

        elif choice == "2":
          while True:
            print("\n* * * Welcome to the Supplier Management System * * *")
            print("\n_____________________________________________________")
            print("\n1. Add Supplier")
            print("\n2. Get Supplier Details")
            print("\n3. Update Supplier Details")
            print("\n4. Generate Supplier Report")
            print("\n5. Delete Supplier")
            print("\n6. Exit")
            choice2 = input("\nEnter your choice: ")

            if choice2 == "1":
              variable = True
              while variable:
                name = input("\nEnter the name of the supplier: ")
                address = input("\nEnter the address of the supplier: ")
                phone = input("\nEnter the phone number of the supplier: ")
                email = input("\nEnter the email of the supplier: ")  
                supplier = Suppliers(name, address, phone, email)
                inventory.add_supplier(supplier)
                var = input("Do you want to add more suppliers? (y/n)")
                if var in ['Yes','y','yes','YES','Y']:
                  variable = True
                else:
                  variable = False

            elif choice2 == '2':
              name = input("\nEnter the name of the supplier: ")
              print("\nSupplier Details are as follows:")
              inventory.supplier_details(name)

            elif choice2 == '3':
                name = input("\nEnter the name of the supplier: ")
                address = input("\nEnter the new address of the supplier: ")
                phone = input("\nEnter the new phone number of the supplier: ")
                email = input("\nEnter the new email of the supplier: ")
                inventory.update_supplier(name, address, phone, email)

            elif choice2 == '4':
              print("\nReport for the suppliers are as follows:")
              inventory.supplier_report()

            elif choice2 == '5':
              name = input("\nEnter the name of the supplier you want to remove: ")
              inventory.delete_supplier(name)

            elif choice2 == '6':
              break

        elif choice == '3':
          while True:
            print("\n* * * Welcome to the Order Management System * * *")
            print("\n__________________________________________________")
            print("\n1. Add Order")
            print("\n2. Get Order Details")
            print("\n3. Update Order Quantity")
            print("\n4. Order report")
            print("\n5. Cancel Order")
            print("\n6. Exit")
            choice2 = input("\nEnter your choice: ")

            if choice2 == "1":
              variable = True
              while variable:
                id = input("\nEnter the product ID: ")
                name = input("\nEnter the product name: ")
                quantity = input("\nEnter the ordered quantity of the product: ")
                ordered_date = datetime.today().strftime("%Y-%m-%d")
                order = Orders(id, name, quantity, ordered_date)
                inventory.add_order(order)
                var = input("Do you want to add more order? (y/n)")
                if var in ['Yes','y','yes','YES','Y']:
                  variable = True
                else:
                  variable = False

            elif choice2 == '2':
              name = input("\nEnter the name of the ordered product: ")
              print("\nOrder Details are as follows:")
              inventory.order_details(name)

            elif choice2 == '3':
                name = input("\nEnter the product name: ")
                quantity = input("\nEnter the ordered quantity of the product: ")
                choice = input("\nDo you want to increase or decrease the quantity? (1/2): ")
                inventory.update_order(name, quantity, "choice")

            elif choice2 == '4':
              print("\nReport for the orders are as follows:")
              inventory.orders_report()

            elif choice2 == '5':
              name = input("\nEnter the name of the supplier you want to remove: ")
              inventory.delete_order(name)

            elif choice2 == '6':
              break

        elif choice == '4':
          print("\nExiting the inventory system .......")
          break 

        else:
          print("\nInvalid choice. Please try again.")

    # Closing the connection
    inventory.close_connection()
