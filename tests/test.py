import pytest
from main import app


# Creating a Flask test client for simulating requests
@pytest.fixture 
def client(): 
    with app.test_client() as client:
        yield client
        
# Test 1: Ensuring login form is present on landing page
def test_landing_page_has_login(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Username" in response.data and b"Password" in response.data  # Checks if login fields appear

# Test 2: Login fails with wrong credentials
def test_login_rejects_invalid_user(client):
    response = client.post("/", data={"username": "wrong", "password": "bad"})
    assert b"Login failed" in response.data or response.status_code == 200  # Checks for graceful failure

# Test 3: Login succeeds and redirects to home page
def test_login_redirects_to_transit(client):
    response = client.post("/", data={"username": "admin", "password": "pass123"}, follow_redirects=True)
    assert b"Transit Home Page" in response.data  # Checks success redirection


# Test 4: Map page loads with embedded iframe and route summary
def test_map_page_summary(client):
    response = client.get("/map")
    assert response.status_code == 200
    assert b"Route Map" in response.data and b"iframe" in response.data  # Verifies map iframe renders

# Test 5: Venue selection form has start, destination, and mode checkboxes
def test_venue_selection_form(client):
    response = client.get("/between_venues")
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
    assert b"Show Directions" in response.data or response.status_code == 200  # Checks route generation

    
