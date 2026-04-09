from src.schema import ProductionSystem
from fastapi import FastAPI
import joblib
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from src.logger import log_prediction, setup_mlflow
import dagshub



app=FastAPI(title="Manufacturing Defect Prediction API", description="API for predicting manufacturing defects and quality issues", version="1.0")
@app.on_event("startup")
def startup_event():
    setup_mlflow()
models_loaded = False
def load_models():
    global anomaly_model, defect_probability, defect_type_model, quality_prediction, threshold,models_loaded
    if models_loaded:
        return
    anomaly_model = joblib.load('models/anomaly_model.pkl')
    defect_probability = joblib.load('models/defect_probability_model.pkl')
    defect_type_model = joblib.load('models/defect_type_model.pkl')
    quality_prediction = joblib.load('models/quality_prediction_model1.pkl')
    threshold = joblib.load('models/threshold.pkl')
    models_loaded = True

scaler=MinMaxScaler()

DEFCT_WEIGHTS={
    "Deformation":0.9,
    "Misalignment":0.6,
    "No defect":0.1,
    "Porosity":0.5,
    "Surface_Defect":0.7,
    "Warping":0.8
}

@app.get("/")
def home():
    return {"message": "Welcome to the Manufacturing Defect Prediction API. Use the /predict endpoint to get predictions."}

@app.post("/predict")
def predict(data: ProductionSystem):

    load_models()
    input_dict=data.model_dump()
    df=pd.DataFrame([input_dict])

    anomaly_flag=anomaly_model.predict(df)
    defect_proba=defect_probability.predict_proba(df)[:,1]
    defect_type_pred=defect_type_model.predict(df)
    quality=quality_prediction.predict(df)

    quality_risk=1-(quality/100)
    anomaly_binary=np.where(anomaly_flag==-1,1,0)
    defect_score=np.array([DEFCT_WEIGHTS[d] for d in defect_type_pred])
    criteria=np.column_stack([anomaly_binary,defect_proba,defect_score,quality_risk])
    weights=np.array([0.35,0.3,0.20,0.15])
    final_score=np.dot(criteria,weights)[0]

    def product_decision(row):
        quality=row['quality']
        probability=row['defect_proba']
        if probability>0.6 or quality<60:
            return "PRODUCT NOT ACCEPTABLE"
        elif probability>0.4 or quality<70:
            return "DO SECOND INSPECTION"
        else:
            return "ACCEPT PRODUCT"
    def machine_decision(row):
        score=row['final_score']
        anomaly=row['anomaly_binary'] == "ANOMALY DETECTED"
        if anomaly==1 and score>0.7:
            return "STOP MACHINE IMMEDIATELY"
        elif anomaly==1 or score>0.4:
            return "MONITOR MACHINE"
        else:
            if score>=0.7:
                return "STOP MACHINE IMMEDIATELY"
            elif score>=0.4:
                return "MONITOR MACHINE"
            else:
                return "MACHINE STABLE"
    def final_decision(row):
        product=product_decision(row)
        machine=machine_decision(row)
        if product=="PRODUCT NOT ACCEPTABLE" and machine == "STOP MACHINE IMMEDIATELY":
            return "STOP OPERATIONS IMMEDIATELY"
        elif product=="DO SECOND INSPECTION" or machine == "MONITOR MACHINE":
            return "INSPECT PROCESS"
        else:
            return "NORMAL OPERATIONS"
    machines=pd.DataFrame({
        "anomaly_binary":anomaly_binary,
        "defect_proba":defect_proba,
        "defect_type":defect_type_pred,
        "quality":quality,
        "final_score":final_score
    })
    machines["anomaly_binary"]=machines["anomaly_binary"].apply(
            lambda x: "ANOMALY DETECTED" if x==1 else "OKAY")
    machines['product_decision']=machines.apply(product_decision,axis=1)
    machines['machine_decision']=machines.apply(machine_decision,axis=1)    
    machines['final_decision']=machines.apply(final_decision,axis=1)
    log_prediction(
        product_type=input_dict['product_type'],
        product_sensitivity=input_dict['product_sensitivity'],  
        material_quality=input_dict['material_quality'],
        operator_skill_level=input_dict['operator_skill_level'],
        temperature=input_dict['temperature'],
        vibration=input_dict['vibration'],
        pressure=input_dict['pressure'],
        machine_speed=input_dict['machine_speed'],
        cooling_rate=input_dict['cooling_rate'],
        cycle_time=input_dict['cycle_time'],
        tool_wear=input_dict['tool_wear'],
        stress_index=input_dict['stress_index'],
        anomaly_binary=anomaly_binary[0],
        defect_proba=defect_proba[0],
        defect_type_pred=defect_type_pred[0],
        quality=quality[0],
        final_score=final_score,
        product_decision=machines['product_decision'].iloc[0],
        machine_decision=machines['machine_decision'].iloc[0],
        final_decision=machines['final_decision'].iloc[0]
    )

    return machines.to_dict(orient="records")


    

