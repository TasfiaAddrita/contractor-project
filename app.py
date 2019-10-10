from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import os
from datetime import datetime

# local deployment
client = MongoClient()
db = client.Store
users = db.users
products = db.products
shopping_cart = db.shopping_cart

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
    quantity = request.form.get('quantity')
    product_item = {
        'product_id': products.find_one({'_id': ObjectId(product_id)}),
        'quantity': quantity
    }
    product_item_id = shopping_cart.insert_one(product_item).inserted_id
    return redirect(url_for('show_shopping_cart'))


@app.route('/shopping-cart', methods=["GET"])
def show_shopping_cart():
    return render_template('shopping_cart.html', shopping_list=shopping_cart.find({}))


@app.route('/shopping-cart/<product_id>/<change_quantity>', methods=["POST"])
def update_quantity(product_id, change_quantity):
    print(change_quantity)
    print(product_id)
    shopping_cart.update_one(
        {'product_id': products.find_one({'_id': ObjectId(product_id)})},
        {'$set': {'quantity': change_quantity}}
    )

    return redirect(url_for('show_shopping_cart'))


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
