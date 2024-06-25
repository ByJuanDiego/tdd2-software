import pytest
from fastapi.testclient import TestClient
from main import app
import time

client = TestClient(app)

#######################################################################################
#                            Tests for register_one endpoint
#######################################################################################

def test_register_one_valid():
    current_timestamp = int(time.time())
    type_of_sensor = "AIRQUALITY"
    read = 10.5
    response = client.post("/register_one/", json={"timestamp": current_timestamp, "type_of_sensor": type_of_sensor, "read": read})
    assert response.status_code == 200
    assert response.json()["message"] == "Sensor reading registered successfully"
    assert response.json()["sensor_type"] == type_of_sensor
    assert response.json()["timestamp"] == current_timestamp
    assert response.json()["read"] == read

def test_register_one_invalid_sensor_type():
    current_timestamp = int(time.time())
    type_of_sensor = "INVALID_SENSOR_TYPE"
    read = 10.5
    response = client.post("/register_one/", json={"timestamp": current_timestamp, "type_of_sensor": type_of_sensor, "read": read})
    assert response.status_code == 400
    assert "Sensor type" in response.json()["detail"]

#######################################################################################
#                            Tests for register_many endpoint
#######################################################################################

def test_register_many_valid():
    current_timestamp = int(time.time())
    type_of_sensor = "ULTRAVIOLETRADIATION"
    reads = [{"timestamp": current_timestamp, "read": "15.7"}, {"timestamp": current_timestamp + 1, "read": "16.2"}]
    response = client.post("/register_many/", json={"type_of_sensor": type_of_sensor, "reads": reads})
    assert response.status_code == 200
    assert response.json()["message"] == f"{len(reads)} readings registered successfully"
    assert response.json()["sensor_type"] == type_of_sensor
    assert response.json()["readings"] == reads

def test_register_many_invalid_sensor_type():
    current_timestamp = int(time.time())
    type_of_sensor = "INVALID_SENSOR_TYPE"
    reads = [{"timestamp": current_timestamp, "read": "15.7"}, {"timestamp": current_timestamp + 1, "read": "16.2"}]
    response = client.post("/register_many/", json={"type_of_sensor": type_of_sensor, "reads": reads})
    assert response.status_code == 400
    assert "Sensor type" in response.json()["detail"]

#######################################################################################
#                            Tests for highest_accumulated endpoint
#######################################################################################

def test_highest_accumulated_valid_with_records():
    type_of_sensor = "TRAFFIC"

    current_timestamp = int(time.time())
    reads = [{"timestamp": current_timestamp, "read": "100.0"},
             {"timestamp": current_timestamp + 1, "read": "150.0"},
             {"timestamp": current_timestamp + 2, "read": "120.0"},
             {"timestamp": current_timestamp + 3, "read": "200.0"}]
    
    response_register = client.post("/register_many/", json={"type_of_sensor": type_of_sensor, "reads": reads})
    assert response_register.status_code == 200

    response_get = client.get(f"/highest_accumulated/?type_of_sensor={type_of_sensor}")
    assert response_get.status_code == 200
    assert "highest_accumulated_value" in response_get.json()
    assert "from" in response_get.json()
    assert "to" in response_get.json()

def test_highest_accumulated_no_records():
    type_of_sensor = "TRAFFIC"

    response = client.get(f"/highest_accumulated/?type_of_sensor={type_of_sensor}")
    assert response.status_code == 404
    assert "No data available" in response.json()["error"]

def test_highest_accumulated_invalid_sensor_type():
    type_of_sensor = "INVALID_SENSOR_TYPE"

    response = client.get(f"/highest_accumulated/?type_of_sensor={type_of_sensor}")
    assert response.status_code == 400
    assert "Sensor type" in response.json()["detail"]
