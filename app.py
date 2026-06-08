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

    #Serialization.
    def to_dict(self):
        return{
            "id": self.id,
            "imei": self.imei,
            "brand": self.brand,
            "model": self.model,
            "storage": self.storage,
            "colour": self.colour,
            "battery_percentage": self.battery_percentage,
            "condition": self.condition,
            "notes": self.notes,
            "incoming_date": self.incoming_date.isoformat() if self.incoming_date else None,
            "purchase_price": self.purchase_price,
            "sell_price": self.sell_price,
            "status": self.status,
        }


@app.route('/phones')
def get_phones():
    phones = Phone.query.all()
    return jsonify([phone.to_dict() for phone in phones])

#Post endpoint
@app.route('/phones', methods=['POST'])
def post_phones():
    data = request.get_json()

    #validating that brand and model are required
    if not data or not data.get('brand') or not data.get('model'):
        return jsonify({"Error": "brand and model are required"}), 400

    #validation that imei is required
    if not data.get('imei'):
        return jsonify({"error": "imei is required"}), 400

    #Status must have one of the allowed values
    allowed_status = ["in_stock", "sold", "on_hold"]
    status = data.get('status', 'in_stock')
    if status not in allowed_status:
        return jsonify({"error": f"status must be one of {allowed_status}"}), 400

    #Build a Phone object from incoming data
    new_phone = Phone(
        imei=data.get('imei'),
        brand=data.get('brand'),
        model=data.get('model'),
        storage=data.get('storage'),
        colour=data.get('colour'),
        battery_percentage=data.get('battery_percentage'),
        condition=data.get('condition'),
        notes=data.get('notes'),
        purchase_price=data.get('purchase_price'),
        sell_price=data.get('sell_price'),
        status=status,
    )

    db.session.add(new_phone)
    db.session.commit()

    return jsonify(new_phone.to_dict()), 201
