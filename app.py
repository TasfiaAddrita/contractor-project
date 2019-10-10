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
checkout = db.checkout

# dummy products
db_products = [
    {
        'name': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit',
        'description': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam lacinia tincidunt sem quis interdum. Suspendisse risus dolor, tempor non tellus id, porta iaculis tortor. Integer volutpat facilisis sem non pretium. In lobortis porttitor auctor. Ut placerat leo ut lectus scelerisque sodales. Suspendisse egestas eros in vehicula pulvinar. Mauris quis diam dignissim, pharetra lorem et, porta metus. Fusce fermentum diam ac auctor laoreet. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Proin vitae ultrices est. Donec quis scelerisque ligula.',
        'category': 'cat1',
        'picture': '/static/placeholder-img.png',
        'price': 30.00
    },
    {
        'name': 'ut tellus elementum sagittis vitae',
        'description': 'Diam quis enim lobortis scelerisque fermentum. Viverra nam libero justo laoreet sit amet cursus sit amet. Tempus egestas sed sed risus pretium quam vulputate dignissim suspendisse. Diam in arcu cursus euismod quis viverra nibh. Fringilla phasellus faucibus scelerisque eleifend donec pretium vulputate sapien. ',
        'category': 'cat2',
        'picture': '/static/placeholder-img.png',
        'price': 25.00
    },
    {
        'name': 'Eros donec ac odio tempor orci dapibus ultrices',
        'description': 'desc3',
        'category': 'cat3',
        'picture': '/static/placeholder-img.png',
        'price': 40.00
    },
    {
        'name': 'Vel turpis nunc eget lorem',
        'description': 'Faucibus et molestie ac feugiat sed lectus vestibulum mattis. Vel turpis nunc eget lorem dolor sed viverra ipsum nunc.',
        'category': 'cat4',
        'picture': '/static/placeholder-img.png',
        'price': 15.00
    }
]

# db.products.delete_many({})
# db.shopping_cart.delete_many({})
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
    product_id =  products.find_one({'_id': ObjectId(product_id)})
    subtotal = int(quantity) * int(product_id['price'])
    product_item = {
        'product_id': product_id,
        'quantity': quantity,
        'subtotal': subtotal
    }
    product_item_id = shopping_cart.insert_one(product_item).inserted_id
    return redirect(url_for('show_shopping_cart'))

@app.route('/shopping-cart', methods=["GET"])
def show_shopping_cart():
    total = 0
    for item in shopping_cart.find({}):
        total += item['product_id']['price'] * int(item['quantity'])
    return render_template('shopping_cart.html', shopping_cart=shopping_cart.find({}), total=total)

@app.route('/shopping-cart/<product_id>/<change_quantity>', methods=["POST"])
# @app.route('/shopping-cart/<product_id>/', methods=["POST"])
def update_quantity(product_id, change_quantity):
    # change_quantity = request.form.get('quantity')
    # print(change_quantity)
    product_id_update = products.find_one({'_id': ObjectId(product_id)})
    shopping_cart.update_one(
        {'product_id': product_id_update},
        {'$set': 
            {
                'quantity': change_quantity,
                'subtotal': int(product_id_update['price']) * int(change_quantity)
            }
        }
    )
    return redirect(url_for('show_shopping_cart'))

@app.route('/shopping-cart/<product_id>/delete', methods=['POST'])
def delete_cart_item(product_id):
    delete_product = products.find_one({'_id': ObjectId(product_id)})
    shopping_cart.delete_one({'product_id': delete_product})
    return redirect(url_for('show_shopping_cart'))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))
    db.products.delete_many({})
    db.shopping_cart.delete_many({})
    db.products.insert_many(db_products)
