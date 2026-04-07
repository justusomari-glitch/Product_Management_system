import mlflow
from datetime import datetime

TRACKING_URI = "file:./mlruns"
EXPERIMENT_NAME = "Product Management System"

def setup_mlflow():
    mlflow.set_tracking_uri(TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)


def log_prediction(
        product_type,
        product_sensitivity,
        material_quality,
        operator_skill_level,
        temperature,
        vibration,
        pressure,
        machine_speed,
        cooling_rate,
        cycle_time,
        tool_wear,
        stress_index,
        anomaly_binary,
        defect_proba,
        defect_type_pred,
        quality,
        final_score,
        product_decision,
        machine_decision,
        final_decision
):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_name = f"inference_{product_type}_{timestamp}"
    with mlflow.start_run(run_name=run_name):
        mlflow.log_param("product_type", product_type)
        mlflow.log_param("product_sensitivity", product_sensitivity)
        mlflow.log_param("material_quality", material_quality)
        mlflow.log_param("operator_skill_level", operator_skill_level)
        mlflow.log_metric("temperature", temperature)
        mlflow.log_metric("vibration", vibration)
        mlflow.log_metric("pressure", pressure)
        mlflow.log_metric("machine_speed", machine_speed)
        mlflow.log_metric("cooling_rate", cooling_rate)
        mlflow.log_metric("cycle_time", cycle_time)
        mlflow.log_metric("tool_wear", tool_wear)
        mlflow.log_metric("stress_index", stress_index)

        mlflow.log_metric("anomaly_binary", anomaly_binary)
        mlflow.log_metric("defect_proba", defect_proba)
        mlflow.log_param("defect_type_pred", defect_type_pred)
        mlflow.log_metric("quality", quality)
        mlflow.log_metric("final_score", final_score)

        mlflow.set_tag("product_decision", product_decision)
        mlflow.set_tag("machine_decision", machine_decision)
        mlflow.set_tag("final_decision", final_decision)
        mlflow.set_tag("run_type", "inference")
        mlflow.set_tag("source", "fastapi")
        
    