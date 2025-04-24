import pytest
from app import app, db, User
from werkzeug.security import generate_password_hash

# Creating a Flask test client for simulating requests
@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Create a test user
            test_user = User(username="testuser", password=generate_password_hash("testpass"))
            db.session.add(test_user)
            db.session.commit()
        yield client
        with app.app_context():
            db.drop_all()

# Test 1: Ensuring login form is present on landing page
def test_landing_page_has_login(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Username" in response.data and b"Password" in response.data  # Checks if login fields appear

# Test 2: Login fails with wrong credentials
def test_login_rejects_invalid_user(client):
    response = client.post("/login", data={"username": "wrong", "password": "bad"})
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data  # Checks for graceful failure

# Test 3: Login succeeds and redirects to home page
def test_login_redirects_to_transit(client):
    response = client.post("/login", data={"username": "testuser", "password": "testpass"}, follow_redirects=True)
    assert response.status_code == 200
    assert b"Login successful!" in response.data  # Checks success redirection

# Test 4: Map page loads with embedded iframe and route summary
def test_map_page_summary(client):
    with client.session_transaction() as session:
        session["start"] = "123 Olympic Blvd"
        session["destination"] = "456 Stadium Way"
        session["mode"] = ["walking"]
    response = client.get("/map")
    assert response.status_code == 200
    assert b"Route Map" in response.data and b"iframe" in response.data  # Verifies map iframe renders

# Test 5: Venue selection form has start, destination, and mode checkboxes
def test_venue_selection_form(client):
    response = client.get("/between_venues")
    assert response.status_code == 200
    assert b"Select Start Venue" in response.data
    assert b"Select Destination Venue" in response.data
    assert b"Walking" in response.data and b"Public Transit" in response.data  # Verifies form options

# Test 6: Submitting venue form returns results or redirect page
def test_venue_routing_submission(client):
    form_data = {
        "start_venue": "123 Olympic Blvd",
        "end_venue": "456 Stadium Way",
        "mode": "walking"
    }
    response = client.post("/between_venues", data=form_data, follow_redirects=True)
    assert response.status_code == 200
    assert b"Show Directions" in response.data  # Checks route generation
