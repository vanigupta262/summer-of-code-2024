import psycopg2
from psycopg2 import sql

# Define your database connection parameters
DB_NAME = "POS"
DB_USER = "postgres"
DB_PASSWORD = "tiger"
DB_HOST = "localhost"
DB_PORT = "5432"

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
def create_tables(connection):
    try:
        cursor = connection.cursor()

        # Create InventoryItem table
        create_inventory_item_table = '''
        CREATE TABLE IF NOT EXISTS InventoryItem (
            Item_SKU SERIAL PRIMARY KEY,
            Item_Name VARCHAR(100) NOT NULL,
            Item_Description TEXT,
            Item_Price DECIMAL(10, 2) NOT NULL,
            Item_Qty INT NOT NULL
        );
        '''

        # Create Customer table
        create_customer_table = '''
        CREATE TABLE IF NOT EXISTS Customer (
            c_ID SERIAL PRIMARY KEY,
            c_name VARCHAR(100) NOT NULL,
            c_email VARCHAR(100) UNIQUE NOT NULL,
            c_contact VARCHAR(15)
        );
        '''

        # Create Staff table
        create_staff_table = '''
        CREATE TABLE IF NOT EXISTS Staff (
            s_ID SERIAL PRIMARY KEY,
            s_name VARCHAR(100) NOT NULL,
            s_email VARCHAR(100) UNIQUE NOT NULL,
            s_isAdmin BOOLEAN NOT NULL,
            s_contact VARCHAR(15)
        );
        '''

        # Create Transaction table
        create_transaction_table = '''
        CREATE TABLE IF NOT EXISTS Transaction (
            t_ID SERIAL PRIMARY KEY,
            c_ID INT NOT NULL,
            s_ID INT NOT NULL,
            t_date TIMESTAMP NOT NULL,
            t_amount DECIMAL(10, 2) NOT NULL,
            t_category VARCHAR(100),
            FOREIGN KEY (c_ID) REFERENCES Customer(c_ID),
            FOREIGN KEY (s_ID) REFERENCES Staff(s_ID),
            FOREIGN KEY (t_ID) REFERENCES InventoryItem(ITEM_SKU)

        );
        '''

        cursor.execute(create_inventory_item_table)
        cursor.execute(create_customer_table)
        cursor.execute(create_staff_table)
        cursor.execute(create_transaction_table)
        connection.commit()
        print("Tables created successfully")

        # Create indexes
        create_index_queries = [
            'CREATE INDEX IF NOT EXISTS idx_inventory_item_sku ON InventoryItem (Item_SKU);',
            'CREATE INDEX IF NOT EXISTS idx_customer_email ON Customer (c_email);'
        ]

        for query in create_index_queries:
            cursor.execute(query)
        
        connection.commit()
        print("Tables and indexes created successfully")

    except Exception as error:
        print(f"Error: Could not create the tables and indexes")
        print(error)
    finally:
        cursor.close()
    

def main():
    connection = connect_to_db()
    if connection:
        create_tables(connection)
        # Always close the connection when done
        connection.close()

if __name__ == "__main__":
    main()