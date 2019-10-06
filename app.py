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

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ.get('PORT', 5000))