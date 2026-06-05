"""
Test script for the House Price Prediction API
Run the Flask app first: python app.py
Then run this script: python test_api.py
"""

import requests
import json

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health endpoint."""
    print("Testing /health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_features():
    """Test features endpoint."""
    print("Testing /features endpoint...")
    response = requests.get(f"{BASE_URL}/features")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_single_prediction():
    """Test single prediction with array format."""
    print("Testing /predict endpoint (array format)...")
    data = {
        "features": [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23]
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_single_prediction_dict():
    """Test single prediction with dictionary format."""
    print("Testing /predict endpoint (dictionary format)...")
    data = {
        "MedInc": 8.3252,
        "HouseAge": 41.0,
        "AveRooms": 6.984127,
        "AveBedrms": 1.023810,
        "Population": 322.0,
        "AveOccup": 2.555556,
        "Latitude": 37.88,
        "Longitude": -122.23
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_batch_prediction():
    """Test batch prediction."""
    print("Testing /predict-batch endpoint...")
    data = {
        "data": [
            [8.3252, 41.0, 6.984127, 1.023810, 322.0, 2.555556, 37.88, -122.23],
            [8.3014, 21.0, 6.238137, 0.971880, 2401.0, 2.109842, 37.86, -122.22],
            [7.2574, 52.0, 8.288136, 1.081081, 1496.0, 2.802198, 37.85, -122.24]
        ]
    }
    response = requests.post(f"{BASE_URL}/predict-batch", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


def test_error_handling():
    """Test error handling."""
    print("Testing error handling (missing feature)...")
    data = {
        "features": [8.3252, 41.0]  # Only 2 features instead of 8
    }
    response = requests.post(f"{BASE_URL}/predict", json=data)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}\n")


if __name__ == "__main__":
    print("=" * 60)
    print("House Price Prediction API - Test Suite")
    print("=" * 60 + "\n")
    
    try:
        test_health()
        test_features()
        test_single_prediction()
        test_single_prediction_dict()
        test_batch_prediction()
        test_error_handling()
        
        print("=" * 60)
        print("All tests completed!")
        print("=" * 60)
    
    except requests.exceptions.ConnectionError:
        print("Error: Cannot connect to the Flask app at http://localhost:5000")
        print("Make sure to run 'python app.py' first!")
