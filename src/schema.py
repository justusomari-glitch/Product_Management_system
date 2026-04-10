from pydantic import BaseModel
import joblib

class AnomalyDetectionRequest(BaseModel):
    temperature: float
    vibration: float
    pressure: float
    tool_wear: float
    machine_speed: float
    cooling_rate: float
    cycle_time: float
    stress_index: float

class DefectProbabilityRequest(BaseModel):
    product_type: str
    product_sensitivity: str
    material_quality: str
    operator_skill_level: str
    temperature: float
    vibration: float
    pressure: float
    machine_speed: float
    cooling_rate: float
    cycle_time: float

class DefectTypeRequest(BaseModel):
    product_type: str
    product_sensitivity: str
    material_quality: str
    operator_skill_level: str
    temperature: float
    vibration: float
    pressure: float
    machine_speed: float
    cooling_rate: float
    cycle_time: float

class QualityPredictionRequest(BaseModel):
    product_type: str
    product_sensitivity: str
    material_quality: str
    operator_skill_level: str
    temperature: float
    vibration: float
    pressure: float
    machine_speed: float
    cooling_rate: float
    cycle_time: float

class ProductionSystem(BaseModel):
    product_type: str
    product_sensitivity: str
    material_quality: str
    operator_skill_level: str
    temperature: float
    vibration: float
    pressure: float
    machine_speed: float
    cooling_rate: float
    cycle_time: float
    tool_wear: float
    stress_index: float
    