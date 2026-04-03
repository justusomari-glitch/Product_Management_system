from fastapi.testclient import TestClient
from src.predict import app


client = TestClient(app)

def test_extreme_case_conditions():
    
    payload = {
        "product_type": "Aluminium Plate",
        "product_sensitivity": "Low",
        "material_quality": "High",
        "operator_skill_level": "Expert",
        "temperature": 1000.0,  # Extreme temperature
        "vibration": 1000.0,     # Extreme vibration
        "pressure": 1000.0,    # Extreme pressure
        "machine_speed": 5000.0,  # Extreme machine speed
        "cooling_rate": 1000.0,     # Extremely low cooling rate
        "cycle_time": 0.1,      # Extremely long cycle time
        "tool_wear": 1000.0,       # Extreme tool wear
        "stress_index": 90.0     # High stress index
    }

    response = client.post("/predict", json=payload)
    assert response.status_code == 200
    data = response.json()[0]
    assert "defect_proba" in data
    assert data["defect_proba"] > 0.6 