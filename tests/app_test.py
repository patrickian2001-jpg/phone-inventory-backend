#I have not used parametization for the whole test but after I might come back and clean it up.


from app import User, Phone

#This tests theat a user can register and their info will be stored in the database.
def test_post_register(client, app):
    register_response = client.post(
        "/register",
        json = {"name": "test", "email": "test@test.com", "password": "test123"}
    )
    with app.app_context():
        user = User.query.filter_by(email="test@test.com").first()

    assert user is not None
    assert register_response.status_code == 201

#Tests that the same email cannot be registered twice.
def test_register_duplicate_email(client):
    register_response = client.post(
        "/register",
        json = {"name": "test", "email": "test@test.com", "password": "test123"}
    )
    dublicate_response = client.post(
        "/register",
        json = {"name": "test", "email": "test@test.com", "password": "test123"}
    )

    assert register_response.status_code == 201
    assert dublicate_response.status_code == 409
    assert dublicate_response.get_json() == {"error": "email already used please login"}

#Test that the user cant register without an email or name or password.
def test_register_missing_requirements(client):
    #No registration data
    empty_response = client.post(
        "/register",
        json = {}
    )
    #Test no name
    missing_name_response = client.post(
        "/register",
        json = {"email": "test@test.com", "password": "test123"}
    )
    #test no email
    missing_email_response  = client.post(
        "/register",
        json = {"name": "test", "password": "test123"}
    )
    #test no password
    missing_password_response = client.post(
        "/register",
        json = {"name": "test", "email": "test@test.com"}
    )

    assert empty_response.status_code == 400
    assert missing_name_response .status_code == 400
    assert missing_email_response.status_code == 400
    assert missing_password_response.status_code == 400

#Test that the user can login.
def test_login_successful(client, user):
    response = client.post(
        "/login",
        json = {"email":"test@test.com", "password": "Test123!"}
    )

    assert response.status_code == 200

#Test that the user cant login using the wrong password
def test_login_wrong_password(client, user):
    response = client.post(
        "/login",
        json = {"email":"test@test.com", "password": "Cake123"}
    )

    assert response.status_code == 401

#Tests that login fails when the email does not exist in the database.
def test_login_no_user_found(client, user):
    response = client.post(
        "/login",
        json = {"email":"ian@gmail.com", "password": "Test123!"}
    )

    assert response.status_code == 401

#Tests that login fails when email or password is missing.
def test_login_missing_requirements(client, user):
    missing_email_response = client.post(
        "/login",
        json = {"password": "Test123!"}
    )

    assert missing_email_response.status_code == 400

    missing_password_response = client.post(
        "/login",
        json = {"email": "test@test.com"}
    )

    assert missing_password_response.status_code == 400

#This will test the get phones route without logging in
#We wanna see the the route not respond to anyone that is not authenticated and logged in.
def test_get_phones_logged_out(client):
    response = client.get("/phones")

    assert response.status_code == 401

#This will test that the client is actually logged in and can access the get phones route.
def test_get_phones_logged_in(client, user):
    login_response = client.post(
        "/login",
        json = {"email": "test@test.com", "password": "Test123!"}
    )
    assert login_response.status_code == 200
    #Using the same client why?
    #because Flask test client preserves the session cookie between requests
    phone_response = client.get("/phones")

    assert phone_response.status_code == 200
    assert phone_response.get_json() == []

#this will test that we cant add to the inventory if the client is logged out.
def test_post_phones_logged_out(client):
    phone = {
        "imei": "123456789123456",
        "brand": "Apple",
        "model": "iPhone 15",
        "storage": 256,
        "colour": "Black",
        "battery_percentage": 83,
        "condition": "Good",
        "notes": "Sim locked to bell",
        "purchase_price": 800,
        "sell_price": 900,
        "status": "in_stock"
    }
    response = client.post(
        "/phones",
        json = phone
    )

    assert response.status_code == 401

#This  would test if we can add a phone to the inventory after logging in.
def test_post_phones_logged_in(client, user, app):
    login_response = client.post(
        "/login",
        json = {"email": "test@test.com", "password": "Test123!"}
    )
    assert login_response.status_code == 200

    phone = {
        "imei": "123456789123456",
        "brand": "Apple",
        "model": "iPhone 15",
        "storage": 256,
        "colour": "Black",
        "battery_percentage": 83,
        "condition": "Good",
        "notes": "Sim locked to bell",
        "purchase_price": 800,
        "sell_price": 900,
        "status": "in_stock"
    }
    phone_response = client.post(
        "/phones",
        json = phone
    )
    assert phone_response.status_code == 201

    with app.app_context():
        phone_in_db = Phone.query.filter_by(imei="123456789123456").first()

    assert phone_in_db is not None


#The application should not let you add a phone to the inventory if the imei or model or brand is missing.
#expected status code is 400, and the application should return json saying brand and model required
def test_post_phones_missing_requirements(client, user):
    login_response = client.post(
        "/login",
        json = {"email": "test@test.com", "password": "Test123!"}
    )

    assert login_response.status_code == 200 #This just makes sure that the client logged in successfully.

    #imei missing
    missing_imei_response = client.post(
        "/phones",
        json = {"brand": "Apple", "model": "iPhone 15"}
    )

    assert missing_imei_response.status_code == 400
    assert missing_imei_response.get_json() == {"error": "imei is required"}

    #brand missing
    missing_brand_response = client.post(
        "/phones",
        json = {"imei": "123456789123456", "model": "iPhone 15"}
    )
    assert missing_brand_response.status_code == 400
    assert missing_brand_response.get_json() == {"Error": "brand and model are required"}

    #model missing
    missing_model_response = client.post(
        "/phones",
        json = {"imei": "123456789123456", "brand": "Apple"}
    )
    assert missing_model_response.status_code == 400
    assert missing_model_response.get_json() == {"Error": "brand and model are required"}

    #The application only take set status type. allowed_status = ["in_stock", "sold", "on_hold"]
    #this will test that the application does not let the client add a different status other that the ones set.
    allowed_status = ["in_stock", "sold", "on_hold"]
    wrong_status_response = client.post(
        "/phones",
        json = {"imei": "123456789123456", "brand": "Apple", "model": "iPhone 15", "status": "held for customer"}
    )
    assert wrong_status_response.status_code == 400
    assert wrong_status_response.get_json() == {"error": f"status must be one of {allowed_status}"}

#what if I try adding the same imei..
#This will test that I cant add the same imei twice
def test_post_phones_dublicate_imei(client, user):
    login_response = client.post(
        "/login",
        json = {"email": "test@test.com", "password": "Test123!"}
    )
    assert login_response.status_code == 200 #This just makes sure the user logged in successfully

    #This adds the first device with the imei 123456789123456
    imei_response = client.post(
        "/phones",
        json = {"imei": "123456789123456", "brand": "Apple", "model": "iPhone 17"}
    )
    assert imei_response.status_code == 201 #Expected outcome is that the test will pass cause this is the first time we are adding the imei

    #Try adding the same phone the second time.
    dublicate_imei_response = client.post(
        "/phones",
        json = {"imei": "123456789123456", "brand": "Apple", "model": "iPhone 17"}
    )

    assert dublicate_imei_response.status_code == 409
    assert dublicate_imei_response.get_json() == {"error": "imei already exists"}