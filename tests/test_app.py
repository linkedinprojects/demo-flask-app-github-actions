# tests/test_app.py
from app import app  # Import your Flask app

def test_home_page():
    client = app.test_client()  # Create a test client
    response = client.get('/')  # Make a GET request to the home page
    assert response.status_code == 200  # Check that the status code is 200
