"""
Phone Inventory Backend
A REST API for tracking phone inventory: brand, model, condition,
purchase price, sale price, and status.
"""
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///phones.db" #database configuration
load_dotenv()
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db = SQLAlchemy(app) #database object
login_manager = LoginManager()
login_manager.init_app(app)

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

#this is a user class to define the users in my app.
#
class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    email = db.Column(db.Text, nullable=False, unique=True)
    hash_password = db.Column(db.Text, nullable=False)

    #Serialization; Why do this? maybe I might need this when trying to match the hash pasword.
    def to_dict(self):
        return{
            "id": self.id,
            "name": self.name,
            "email": self.email,
        }    

#this gets the User object for every request.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['POST'])
def user_register():
    data = request.get_json()

    #Validating that the users enters the name, email, and password.
    if not data or not data.get('name') or not data.get('email') or not data.get('hash_password'):
        return jsonify({"error": "Name, email and password are required."}), 400

    #validating the user entered a unique email.
    if User.query.filter_by(email = data.get('email')).first():
        return jsonify({"error": "emaill already used please login"}), 409
    #The password needs to be hashed.
    hashed_pass = generate_password_hash(data.get("hash_password"), method="pbkdf2:sha256")

    #Create a user object from the incoming data
    new_user = User(
        name = data.get("name"),
        email = data.get("email"),
        hash_password = hashed_pass,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify(new_user.to_dict()), 201

#@app.route('/login') #This is where the users logs in it will ask for an email and password

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

#me trying to write the delete route

@app.route('/phones/<int:id>', methods=["DELETE"])
def erase_phone(id):
    phone = Phone.query.get(id)

    db.session.delete(phone)
    db.session.commit()
    return "Phone has been successfully deleted"