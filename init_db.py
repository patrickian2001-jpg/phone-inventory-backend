#I have to import app and db from my app.py
from app import app, db
#Got this from SQLAchemy documentation.
with app.app_context(): #What is app_context?
    db.create_all()
    print("Database initialized")