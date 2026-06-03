"""
Phone Inventory Backend
A REST API for tracking phone inventory: brand, model, condition,
purchase price, sale price, and status.
"""

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///phones.db" #database configuration
db = SQLAlchemy(app) #database object

class Phone(db.Model):
    __tablename__ = "phones"

    id = db.Column(db.Integer, primary_key=True)
    imei = db.Column(db.String(20), nullable=False, unique=True)
    brand = db.Column(db.String(100), nullable=False)
    model = db.Column(db.String(100), nullable=False)
    storage = db.Column(db.Integer, nullable=True)
    colour = db.Column(db.String(50), nullable=True)
    battery_percentage = db.Column(db.Integer, nullable=True)
    condition = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    incoming_date = db.Column(db.Date, nullable=True)
    purchase_price = db.Column(db.Integer, nullable=True) #Stored in cents
    sell_price = db.Column(db.Integer, nullable=True) #Stored in cents
    status = db.Column(db.String(20), nullable=False, default="in_stock")


#In memory data store. Lives at module level so all routes share it.
#will be replaced with a real database later.
#phones = [
#    {"id": 1, "brand": "Apple", "model": "iPhone 13", "condition": "good", "purchase_price": 250, "sale_price": 400, "status": "in_stock"},
#    {"id": 2, "brand": "Samsung", "model": "Galaxy S22", "condition": "excellent", "purchase_price": 200, "sale_price": 380, "status": "in_stock"},
#]

@app.route('/phones')
def get_phones():

    return jsonify(phones)

#Post endpoint
@app.route('/phones', methods=['POST'])
def post_phones():
    new_phone = request.get_json()

    #validation: To add a phone we need a Brand and Model atleast.
    if not new_phone or not new_phone.get('brand') or not new_phone.get('model'):
        return jsonify({"error": "brand and model are required"}), 400

    phones.append(new_phone)
    return jsonify(new_phone), 201