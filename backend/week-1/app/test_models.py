import psycopg2
import re

# Define your database connection parameters
DB_NAME = "POS"
DB_USER = "postgres"  # Default user
DB_PASSWORD = "tiger"  # Ensure you replace this with your actual password
DB_HOST = "localhost"  # Default host
DB_PORT = "5432"  # Default port

def connect_to_db():
    try:
        # Establish the connection
        connection = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("Connection to PostgreSQL DB successful")
        
        return connection
    except Exception as error:
        print(f"Error: Could not connect to the PostgreSQL DB")
        print(error)
        return None

def validate_email(email):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if re.match(email_regex, email):
        return True
    else:
        return False

def validate_price(price):
    if price >= 0:
        return True
    else:
        return False

def validate_contact(contact):
    contact_regex = r'^\d{10}$'  # Assuming a 10-digit contact number
    if re.match(contact_regex, contact):
        return True
    else:
        return False

def insert_customer(connection, name, email, contact):
    if not validate_email(email):
        raise ValueError("Invalid email format")
    if not validate_contact(contact):
        raise ValueError("Invalid contact number")
    
    try:
        cursor = connection.cursor()
        insert_customer_query = '''
        INSERT INTO Customer (c_name, c_email, c_contact)
        VALUES (%s, %s, %s)
        RETURNING c_ID;
        '''
        cursor.execute(insert_customer_query, (name, email, contact))
        connection.commit()
        print("Customer inserted successfully")
    except Exception as error:
        print(f"Error: Could not insert customer")
        print(error)
    finally:
        cursor.close()

def insert_inventory_item(connection, name, description, price, qty):
    if not validate_price(price):
        raise ValueError("Item price must be non-negative")
    
    try:
        cursor = connection.cursor()
        insert_inventory_item_query = '''
        INSERT INTO InventoryItem (Item_Name, Item_Description, Item_Price, Item_Qty)
        VALUES (%s, %s, %s, %s)
        RETURNING Item_SKU;
        '''
        cursor.execute(insert_inventory_item_query, (name, description, price, qty))
        connection.commit()
        print("Inventory item inserted successfully")
    except Exception as error:
        print(f"Error: Could not insert inventory item")
        print(error)
    finally:
        cursor.close()

def test_insert_data(connection):
    try:
        # Insert data into Customer
        insert_customer(connection, "John Doe", "john.doe@example.com", "1234567890")
        
        # Insert data into Staff
        insert_staff_query = '''
        INSERT INTO Staff (s_name, s_email, s_isAdmin, s_contact)
        VALUES (%s, %s, %s, %s)
        RETURNING s_ID;
        '''
        staff_email = "jane.smith@example.com"
        if not validate_email(staff_email):
            raise ValueError("Invalid email format")
        cursor = connection.cursor()
        cursor.execute(insert_staff_query, ("Jane Smith", staff_email, True, "0987654321"))
        staff_id = cursor.fetchone()[0]
        
        # Insert data into InventoryItem
        insert_inventory_item(connection, "Laptop", "A powerful laptop", 999.99, 10)
        
        # Insert data into Transaction
        insert_transaction_query = '''
        INSERT INTO Transaction (c_ID, s_ID, Item_SKU, t_date, t_amount, t_category)
        VALUES (%s, %s, %s, NOW(), %s, %s);
        '''
        cursor.execute(insert_transaction_query, (1, staff_id, 1, 999.99, "Electronics"))
        
        connection.commit()
        print("Test data inserted successfully")
    except Exception as error:
        print(f"Error: Could not insert test data")
        print(error)
    finally:
        cursor.close()

def main():
    connection = connect_to_db()
    if connection:
        test_insert_data(connection)
        # Always close the connection when done
        connection.close()

if __name__ == "__main__":
    main()
