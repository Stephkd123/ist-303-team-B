import pytest
from main import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_recommend_transport_fastest(client):
    response = client.get('/recommend?preference=fastest')
    assert response.status_code == 200
    assert response.json['mode'] == 'ride_share'

def test_recommend_transport_cheapest(client):
    response = client.get('/recommend?preference=cheapest')
    assert response.status_code == 200
    assert response.json['mode'] == 'bike'

def test_recommend_transport_eco_friendly(client):
    response = client.get('/recommend')
    assert response.status_code == 200
    assert response.json['eco_friendly'] == True
