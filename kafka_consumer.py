from confluent_kafka import Consumer
import json
import pandas as pd
from src.predict import predict,ProductionSystem
import os
from dotenv import load_dotenv

load_dotenv()


bootstrap_servers = os.getenv("KAFKA_BOOTSTRAP_SERVERS")
username = os.getenv("KAFKA_API_KEY")
password = os.getenv("KAFKA_API_SECRET")

conf= {
    'bootstrap.servers': bootstrap_servers,
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': username,
    'sasl.password': password,
    'group.id': 'production_data_consumers',
    'auto.offset.reset': 'earliest'
}
consumer=Consumer(conf)
consumer.subscribe(['raw_data'])
print("Listening bruh")
try:
    while True:
        msg=consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print(f"Consumer error: {msg.error()}")
            continue
        data=json.loads(msg.value().decode('utf-8'))
        print("Received:", data)
        Valid_skills=["Expert", "Intermediate"]
        if data["operator_skill_level"] not in Valid_skills:
            print("Invalid operator skill level:", data["operator_skill_level"])
            data["operator_skill_level"]="Intermediate"
        input_data= ProductionSystem(**data)
        result=predict(input_data)
        if isinstance(result, list):
            result=result[0]
         
        print("Prediction Result:", result)
        record={
            #features
            "product_type": data.get("product_type"),
            "product_sensitivity": data.get("product_sensitivity"),
            "material_quality": data.get("material_quality"),
            "operator_skill_level": data.get("operator_skill_level"),
            "temperature": data.get("temperature"),
            "vibration": data.get("vibration"),
            "pressure": data.get("pressure"),
            "machine_speed": data.get("machine_speed"),
            "cooling_rate": data.get("cooling_rate"),
            "cycle_time": data.get("cycle_time"),
            "tool_wear": data.get("tool_wear"),
            "stress_index": data.get("stress_index"),
            # predictions
            "anomaly_binary": result.get("anomaly_binary"),
            "defect_proba": round(result.get("defect_proba",0), 2),
            "defect_type": result.get("defect_type"),
            "quality": round(result.get("quality",0), 2),
            "final_score": round(result.get("final_score",0), 2),
            # production decisions
            "product_decision": result.get("product_decision"),
            "machine_decision": result.get("machine_decision"),
            "final_decision": result.get("final_decision")
        }
        df=pd.DataFrame([record])
        file_path="predictions.csv"
        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, mode='a', header=False, index=False)


except KeyboardInterrupt:
    print("Consumer stopped")
finally:
    consumer.close()