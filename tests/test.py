import pytest
from la_olympics_route_app.app import app, db, User # Correct import
from werkzeug.security import generate_password_hash


# Flask test client setup
@pytest.fixture
def client():
    app.config['TESTING'] = True
    # Use in-memory SQLite DB for tests
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False # Disable CSRF for easier testing
    app.config['SECRET_KEY'] = 'test-secret-key' # Set a secret key for session testing

    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            # Add a test user directly to the test database
            test_user = User(username="testuser", password=generate_password_hash("testpass"))
            db.session.add(test_user)
            db.session.commit()
        yield client # Provide the client to the tests
        # Teardown: drop all tables after tests run
        with app.app_context():
            db.drop_all()

# --- Test Functions ---

# Test 1: Login form visibility on landing page (No changes needed)
def test_landing_page_has_login(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Username" in response.data
    assert b"Password" in response.data
    assert b"Login</button>" in response.data # Check for login button

# Test 2: Invalid login credentials (No changes needed)
def test_login_rejects_invalid_user(client):
    response = client.post("/login", data={"username": "wrong", "password": "bad"})
    # Should render login page again with error
    assert response.status_code == 200
    assert b"Invalid credentials" in response.data
    assert b"Login successful!" not in response.data

# Test 3: Successful login redirects to /start with flash message (UPDATED NAME)
def test_login_redirects_to_start(client): # Renamed function
    response = client.post("/login", data={"username": "testuser", "password": "testpass"}, follow_redirects=True)
    # After redirect to /start (which renders login.html again)
    assert response.status_code == 200
    # Check for the success flash message
    assert b"Login successful!" in response.data
    # Check we are on a page that likely contains login/signup again (since /start renders login.html)
    assert b"Username" in response.data


# Test 5: Form content check for venue selection (No changes needed)
def test_venue_selection_form(client):
    response = client.get("/between_venues")
    assert response.status_code == 200
    # Check for key form elements
    assert b"Select Start Venue" in response.data
    assert b"Select Destination Venue" in response.data
    assert b'name="mode" value="walking"' in response.data
    assert b'name="mode" value="transit"' in response.data
    assert b"Get Directions</button>" in response.data # Check for submit button

