# InventoryItem
Description: Represents an item in the inventory with a potential hierarchical relationship for categorization.

Fields:
Item_SKU: SERIAL PRIMARY KEY - Unique identifier for each item.
Item_Name: VARCHAR(100) NOT NULL - Name of the item.
Item_Description: TEXT - Description of the item.
Item_Price: DECIMAL(10, 2) NOT NULL - Price of the item.
Item_Qty: INT NOT NULL - Quantity of the item in stock.
parent_sku: INT - References Item_SKU in the same table to establish a parent-child hierarchy.
Relationships:

Self-referential: parent_sku references Item_SKU in the same table, allowing for hierarchical categorization.

# Customer
Description: Represents a customer with their contact information.

Fields:
c_ID: SERIAL PRIMARY KEY - Unique identifier for each customer.
c_name: VARCHAR(100) NOT NULL - Name of the customer.
c_email: VARCHAR(100) UNIQUE NOT NULL - Email address of the customer.
c_contact: VARCHAR(15) - Contact number of the customer.
Relationships:

Referenced by: Transaction.c_ID to link transactions to customers.

# Staff
Description: Represents a staff member, indicating if they are an admin.

Fields:
s_ID: SERIAL PRIMARY KEY - Unique identifier for each staff member.
s_name: VARCHAR(100) NOT NULL - Name of the staff member.
s_email: VARCHAR(100) UNIQUE NOT NULL - Email address of the staff member.
s_isAdmin: BOOLEAN NOT NULL - Indicates if the staff member is an admin.
s_contact: VARCHAR(15) - Contact number of the staff member.
Relationships:

Referenced by: Transaction.s_ID to link transactions to staff members.

# Transaction
Description: Represents a transaction involving a customer, a staff member, and an inventory item.

Fields:
t_ID: SERIAL PRIMARY KEY - Unique identifier for each transaction.
c_ID: INT NOT NULL - References Customer.c_ID to link to a customer.
s_ID: INT NOT NULL - References Staff.s_ID to link to a staff member.
Item_SKU: INT NOT NULL - References InventoryItem.Item_SKU to link to an inventory item.
t_date: TIMESTAMP NOT NULL - Date and time of the transaction.
t_amount: DECIMAL(10, 2) NOT NULL - Amount of the transaction.
t_category: VARCHAR(100) - Category of the transaction.

# Relationships:

References:
Customer.c_ID
Staff.s_ID
InventoryItem.Item_SKU

## Database Schema Visualization: 
https://dbdiagram.io/d/Models-py-667f04b69939893dae8fdbe8