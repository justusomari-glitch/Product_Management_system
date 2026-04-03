from fastapi.testclient import TestClient
from src.predict import app

client=TestClient(app)

def test_home_route():
    response=client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()

def test_predict_route_valid_input():
    payload={
        "product_type": "Aluminium Plate",
        "product_sensitivity": "High",
        "material_quality": "Low",
        "operator_skill_level": "Expert",
        "temperature": 50.3,
        "vibration": 20.2,
        "pressure": 101.3,
        "machine_speed": 1000.0,
        "cooling_rate": 50.0,
        "cycle_time": 120.0,
        "tool_wear": 4.5,
        "stress_index": 75.0
    }

    response=client.post("/predict",json=payload)
    assert response.status_code == 200
    data=response.json


def test_predict_route_invalid_input(): 
    payload={
        'machine_age_days': 200,
        'temperature': 50.3,
        'vibration': 20.2,
    }

    response=client.post("/predict",json=payload)
    assert response.status_code == 422