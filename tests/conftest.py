#This will have all my pytest fixtures that will be reusable while testing.
import pytest
from app import create_app, db

@pytest.fixture
def app(tmp_path):
    # Create path for a temporary SQLite file.
    #This does not create the database it just makes the path to where the database will be 
    db_path = tmp_path/"test.db"

    # Configuration override.
    # This will be used to override the default configs when creating the app
    test_config = {"TESTING": True, "SQLALCHEMY_DATABASE_URI": f"sqlite:///{db_path}"}

    #Creates test flask app 
    test_app = create_app(test_config)

    # Creates db tables
    with test_app.app_context():
        db.create_all()

    yield test_app  # Give the app to tests/other fixtures

    #Cleanup: drop tables and remove test db file
    with test_app.app_context():
        db.session.remove() #Cleans up the SQLAlchemy session associated with the test
        db.drop_all() #removes the tables we created

@pytest.fixture
def client(app):
    #app fixture run first to create the app.
    #Then we create a test client from it

    with app.test_client() as client:
        yield client #Give the client to the test

