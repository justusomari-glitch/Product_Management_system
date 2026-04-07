import mlflow
import mlflow.sklearn
import joblib
from sklearn.metrics import mean_squared_error,f1_score,accuracy_score,recall_score,precision_score,r2_score,mean_absolute_error
from sklearn.model_selection import train_test_split
from logger import setup_mlflow

def load_models():
    
    defect_probability = joblib.load('models/defect_probability_model.pkl')
    defect_type_model = joblib.load('models/defect_type_model.pkl')
    quality_prediction = joblib.load('models/quality_prediction_model1.pkl')

    return defect_probability,defect_type_model,quality_prediction


def run_mlflow_logging(
    test_y_type,
    type_preds,
    test_y_quality,
    quality_preds,
    test_y_defect,
    defect_preds,
    threshold,
    defect_probability,
    defect_type_model,
    quality_prediction
):
    print("Setting up MLflow and logging model evaluation metrics...")
    setup_mlflow()
    with mlflow.start_run(run_name="main_run"):
        print("Logging model evaluation metrics and parameters to MLflow...")

        with mlflow.start_run(run_name="defect_type",nested=True):
            mlflow.log_param("model_type","Classification")
            mlflow.log_metric("f1_score",f1_score(test_y_type,type_preds,average='weighted'))
            mlflow.log_metric("precision_score",precision_score(test_y_type,type_preds,average='weighted'))
            mlflow.log_metric("recall_score",recall_score(test_y_type,type_preds,average='weighted'))
            mlflow.sklearn.log_model(defect_type_model,name="defect_type")
        with mlflow.start_run(run_name="defect_probability",nested=True):
            mlflow.log_param("model_type","Classification")
            mlflow.log_param("threshold",threshold)
            mlflow.log_metric("f1_score",f1_score(test_y_defect,defect_preds))
            mlflow.log_metric("precision_score",precision_score(test_y_defect,defect_preds))
            mlflow.log_metric("recall_score",recall_score(test_y_defect,defect_preds))
            mlflow.sklearn.log_model(defect_probability,name="defect_probability")

        with mlflow.start_run(run_name="product_quality",nested=True):
            mlflow.log_param("model_type","RandomForestRegression")
            mlflow.log_metric("r2_score",r2_score(test_y_quality,quality_preds))
            mlflow.log_metric("MAE",mean_absolute_error(test_y_quality,quality_preds))
            mlflow.log_metric("MSE",mean_squared_error(test_y_quality,quality_preds))
            mlflow.sklearn.log_model(quality_prediction,name="product_quality")
if __name__ == "__main__":
    import pandas as pd
    import joblib

    df=pd.read_csv(r"C:\Users\user\Desktop\Product_Management_system\cleaned_data.csv")

    x=df[['temperature', 'vibration', 'pressure', 'tool_wear', 'machine_speed', 'cooling_rate', 'cycle_time', 'stress_index',
       'product_type', 'product_sensitivity', 'material_quality', 'operator_skill_level']]
    y_type=df['defect_type']
    y_quality=df['quality_score']
    y_probability=df['is_defect']
    x_train_quality,x_test_quality,y_quality_train,y_quality_test=train_test_split(x,y_quality,test_size=0.3,random_state=42)
    x1_train,x1_test,y_type_train,y_type_test=train_test_split(x,y_type,test_size=0.3,random_state=42)
    x2_train,x2_test,y_probability_train,y_probability_test=train_test_split(x,y_probability,test_size=0.3,random_state=42)
    
    defect_probability = joblib.load('models/defect_probability_model.pkl')
    defect_type_model = joblib.load('models/defect_type_model.pkl')
    quality_prediction = joblib.load('models/quality_prediction_model1.pkl')
    threshold = joblib.load('models/threshold.pkl')

    type_preds=defect_type_model.predict(x1_test)
    quality_preds=quality_prediction.predict(x_test_quality)
    defect_proba=defect_probability.predict_proba(x2_test)[:,1]
    defect_preds=(defect_proba>=threshold).astype(int)

    run_mlflow_logging(
        y_type_test,
        type_preds,
        y_quality_test,
        quality_preds,
        y_probability_test,
        defect_preds,
        threshold,
        defect_probability,
        defect_type_model,
        quality_prediction
    )

    

