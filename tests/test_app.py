import sys
import os

# Add the root directory of the project to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app  # Import your Flask app

def test_home_page():
    client = app.test_client()  # Create a test client
    response = client.get('/')  # Make a GET request to the home page
    assert response.status_code == 200  # Check that the status code is 200
