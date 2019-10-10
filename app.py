from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

# local deployment
client = MongoClient()
# db = client.Playlister # replace Playlister with database name
# playlists = db.playlists # replace playlists with collection name
db = client.Store
users = db.users
products = db.products

# dummy products
db_products = [
    {
        'name': '1',
        'description': 'desc1',
        'category': 'cat1',
        'picture': '/static/placeholder-img.png',
        'price': 30.00
    },
    {
        'name': '2',
        'description': 'desc2',
        'category': 'cat2',
        'picture': '/static/placeholder-img.png',
        'price': 25.00
    },
    {
        'name': '3',
        'description': 'desc3',
        'category': 'cat3',
        'picture': '/static/placeholder-img.png',
        'price': 40.00
    },
    {
        'name': '4',
        'description': 'desc4',
        'category': 'cat4',
        'picture': '/static/placeholder-img.png',
        'price': 15.00
    }
]

# db.products.delete_many({})
# db.products.insert_many(db_products)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html', products=products.find({}))

@app.route('/product/<product_id>', methods=['GET'])
def product_page(product_id):
    product = products.find_one({'_id': ObjectId(product_id)})
    return render_template('product.html', product=product)

@app.route('/product/<product_id>', methods=['POST'])
def add_product(product_id):
    return redirect(url_for('show_shopping_cart'))

@app.route('/shopping-cart', methods=["GET"])
def show_shopping_cart():
    return render_template('shopping-cart.html', msg="hi")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))