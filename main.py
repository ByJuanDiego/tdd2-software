import uvicorn
from fastapi import FastAPI, HTTPException
from typing import List, Tuple
import example as sensor

app = FastAPI()

airquality_sensor = sensor.Sensor()
ultraviolet_radiation_sensor = sensor.Sensor()
traffic_sensor = sensor.Sensor()

sensors_mapping = {
    "AIRQUALITY": airquality_sensor,
    "ULTRAVIOLETRADIATION": ultraviolet_radiation_sensor,
    "TRAFFIC": traffic_sensor
}

@app.post("/register_one/")
def register_one(timestamp: int, type_of_sensor: str, read: float):
    if type_of_sensor not in sensors_mapping:
        raise HTTPException(status_code=400, detail=f"Sensor type '{type_of_sensor}' not supported.")
    
    sensors_mapping[type_of_sensor].register_one(timestamp, read)
    
    return {
        "message": "Sensor reading registered successfully",
        "sensor_type": type_of_sensor,
        "timestamp": timestamp,
        "read": read
    }

@app.post("/register_many/")
def register_many(type_of_sensor: str, reads: List[dict]):
    if type_of_sensor not in sensors_mapping:
        raise HTTPException(status_code=400, detail=f"Sensor type '{type_of_sensor}' not supported.")
    
    formatted_reads = [(read["timestamp"], float(read["read"])) for read in reads]
    sensors_mapping[type_of_sensor].register_many(formatted_reads)
    
    return {
        "message": f"{len(reads)} readings registered successfully",
        "sensor_type": type_of_sensor,
        "readings": reads
    }

@app.get("/highest_accumulated/")
def highest_accumulated(type_of_sensor: str):
    if type_of_sensor not in sensors_mapping:
        raise HTTPException(status_code=400, detail=f"Sensor type '{type_of_sensor}' not supported.")
    
    result: Tuple[int, int, float] = sensors_mapping[type_of_sensor].highest_accumulated()
    if result == (-1, -1):
        return {
            "highest_accumulated_value": -1,
            "from": -1,
            "to": -1,
            "error": f"No data available for sensor type '{type_of_sensor}'.",
            "status": 404
        }
    
    return {
        "highest_accumulated_value": result[2],
        "from": result[0],
        "to": result[1],
        "error": None,
        "status": 200
    }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
