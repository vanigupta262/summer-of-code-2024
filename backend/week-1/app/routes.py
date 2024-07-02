from flask import jsonify, request
from .models import connect_to_db

def get_all_products():
    connection = connect_to_db()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute('SELECT Item_SKU, Item_Name, Item_Description, Item_Price, Item_Qty, parent_sku FROM InventoryItem;')
        products = cursor.fetchall()
        result = [
            {
                'Item_SKU': product[0],
                'Item_Name': product[1],
                'Item_Description': product[2],
                'Item_Price': float(product[3]),
                'Item_Qty': product[4],
                'parent_sku': product[5]
            } for product in products
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def create_product():
    data = request.get_json()
    connection = connect_to_db()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute(
            '''
            INSERT INTO InventoryItem (Item_Name, Item_Description, Item_Price, Item_Qty, parent_sku)
            VALUES (%s, %s, %s, %s, %s) RETURNING Item_SKU;
            ''',
            (data['Item_Name'], data['Item_Description'], data['Item_Price'], data['Item_Qty'], data.get('parent_sku'))
        )
        item_id = cursor.fetchone()[0]
        connection.commit()
        return jsonify({'Item_SKU': item_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def get_product_by_id(id):
    connection = connect_to_db()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute('SELECT Item_SKU, Item_Name, Item_Description, Item_Price, Item_Qty, parent_sku FROM InventoryItem WHERE Item_SKU = %s;', (id,))
        product = cursor.fetchone()
        if product:
            result = {
                'Item_SKU': product[0],
                'Item_Name': product[1],
                'Item_Description': product[2],
                'Item_Price': float(product[3]),
                'Item_Qty': product[4],
                'parent_sku': product[5]
            }
            return jsonify(result), 200
        else:
            return jsonify({'error': 'Product not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def update_product(id):
    data = request.get_json()
    connection = connect_to_db()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute(
            '''
            UPDATE InventoryItem
            SET Item_Name = %s, Item_Description = %s, Item_Price = %s, Item_Qty = %s, parent_sku = %s
            WHERE Item_SKU = %s;
            ''',
            (data['Item_Name'], data['Item_Description'], data['Item_Price'], data['Item_Qty'], data.get('parent_sku'), id)
        )
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'message': 'Product updated successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def delete_product(id):
    connection = connect_to_db()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
