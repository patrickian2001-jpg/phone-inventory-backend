"""
Phone Inventory Backend
A REST API for tracking phone inventory: brand, model, condition,
purchase price, sale price, and status.
"""

from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/phones')
def get_phones():

    # In-memory data store. Will be replaced with a real database later.
    phones = [
        {
            "id": 1,
            "brand": "Apple",
            "Model": "iPhone 13",
            "condition": "good",
            "purchase_price": 250,
            "sale_price": 400,
            "status": "in_stock"
        },
        {
            "id": 2,
            "brand": "Samsung",
            "model": "Galaxy S22",
            "condition": "excellent",
            "purchase_price": 200,
            "sale_price": 380,
            "status": "in_stock"
        }
    ]
    return jsonify(phones)
    