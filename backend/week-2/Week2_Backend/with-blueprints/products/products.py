import psycopg2
from flask import Blueprint, jsonify, request, render_template,json,redirect,url_for

DB_NAME = "POS"
DB_USER = "postgres"
DB_PASSWORD = "tiger"
DB_HOST = "localhost"
DB_PORT = "5432"

def connect_to_db():
    try:
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

def read_all():
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
        return render_template('index.html', products=result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

def create_new_product():
    if request.method == 'POST':
        data = request.form
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
            return redirect(url_for('products.read_all'))
        except Exception as e:
            return jsonify({'error': str(e)}), 500
        finally:
            cursor.close()
            connection.close()
    return render_template('create.html')

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

def update_by_id(id):
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
        cursor.execute('SELECT Item_SKU, Item_Name, Item_Description, Item_Price, Item_Qty, parent_sku FROM InventoryItem WHERE Item_SKU = %s;', (id,))
        product = cursor.fetchone()
        if product:
            result = {
                'message': 'Product updated successfully',
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

def delete_by_id(id):
    connection = connect_to_db()
    if not connection:
        return jsonify({'error': 'Database connection failed'}), 500

    try:
        cursor = connection.cursor()
        cursor.execute('DELETE FROM InventoryItem WHERE Item_SKU = %s;', (id,))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'error': 'Product not found'}), 404
        return jsonify({'message': 'Product deleted successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()

# Create a Blueprint
products_bp = Blueprint('products', __name__, template_folder='templates')

# @products_bp.route('/')
# def index():
    # return render_template('admin_dashboard.html')

@products_bp.route('/api/products', methods=['GET'])
def get_products():
    return read_all()

@products_bp.route('/api/products', methods=['POST'])
def add_product():
    return create_new_product()

@products_bp.route('/api/products/<int:id>', methods=['GET'])
def get_product(id):
    return get_product_by_id(id)

@products_bp.route('/api/products/<int:id>', methods=['PUT'])
def update_product(id):
    return update_by_id(id)

@products_bp.route('/api/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    return delete_by_id(id)
