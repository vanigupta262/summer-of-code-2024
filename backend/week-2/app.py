import os
#os for reading env variables 
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()

app = Flask(__name__)
url = os.getenv("DATABASE_URL")
connection = psycopg2.connect(url) 


app = Flask(__name__)

@app.get('/')
def home():
    return "Hello World!"
    
@app.route('/products/add', methods=['POST'])
def add_product():
    #connection = None
    data = request.get_json()
    # connection = get_db_connection()
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    INSERT INTO InventoryItem (Item_Name, Item_Description, Item_Price, Item_Qty, parent_sku)
                    VALUES (%s, %s, %s, %s, %s) RETURNING Item_SKU;
                    ''',
                    (
                        data['Item_Name'],
                        data['Item_Description'],
                        data['Item_Price'],
                        data['Item_Qty'],
                        data.get('parent_sku')
                    )
                )
                item_id = cursor.fetchone()[0]
                return jsonify({'Item_SKU': item_id}), 201
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({'error': str(e)}), 500
    finally:
        if connection is not None and not connection.closed:
            connection.close()
        

@app.route('/products/get', methods=['GET'])
def get_all_products():
    #connection = None
    try:
        with connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    '''
                    SELECT * FROM InventoryItem;
                    '''
                )
                products = cursor.fetchall()
                result = [
                    {
                        'Item_SKU': product[0],
                        'Item_Name': product[1],
                        'Item_Description': product[2],
                        'Item_Price': float(product[3]),
                        'Item_Qty': product[4],
                        'parent_sku': product[5]
                    } for product in products  # Iterating over each individual product
                ]
                return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if connection is not None and not connection.closed:
            connection.close()
                
   
