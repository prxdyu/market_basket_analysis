import pytest
from app import app # importing the app from app.py



# creating a resuable client  for testing using pytest fixture
@pytest.fixture
def client():
    return app.test_client()


# creating a test function to check the ping endpoint
def test_ping(client):
    # sending a GET request to ping endpoint using the client
    response=client.get('/ping')
    # asserting the status of the request
    assert response.status=="200"+" OK"
    # asserting the content of the request
    assert response.text=="Success"


# Creating a test function to check the predict endpoint
def test_predict(client):
    # Construct a sample query point
    sample_data = {'selected_products':['Quick Extra Lean Hamburger']}    
    # Sending a POST request to the /predict endpoint with sample data
    response = client.post('/recommend', data=sample_data)

    print("The resposne is ",response.status_code)

    # Asserting the status of the request
    assert response.status_code == 200

    