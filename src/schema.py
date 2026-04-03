from pydantic import BaseModel
import joblib

anomaly_model = joblib.load('models/anomaly_model.pkl')
defect_probability = joblib.load('models/defect_probability_model.pkl')
typte_model = joblib.load('models/defect_type_model.pkl')
quality_model = joblib.load('models/quality_prediction_model3.pkl')


print ("Models loaded successfully")
print("Anomaly Detection Model:", anomaly_model.feature_names_in_)
print("Defect Probability Model:", defect_probability.feature_names_in_)
print("Defect Type Model:", typte_model.feature_names_in_)
print("Quality Prediction Model:", quality_model.feature_names_in_)




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
    