from flask import Flask
from products.products import products_bp

app = Flask(__name__)
app.register_blueprint(products_bp)
if(__name__ == '__main__'):
    app.run(debug=True)
    