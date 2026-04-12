from confluent_kafka import Consumer
import json
import pandas as pd
from src.predict import predict,ProductionSystem
import os
from dotenv import load_dotenv
import pymysql

#load environment variables from .env file
load_dotenv()

#kafka consumer configuration
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


# mysql configuration
db=pymysql.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    port=int(os.getenv("DB_PORT")),
    ssl={"ssl": {"mode": os.getenv("SSL_MODE")}}
)
cursor=db.cursor()

#create mysql table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_type VARCHAR(255),
    product_sensitivity VARCHAR(255),
    material_quality VARCHAR(255),
    operator_skill_level VARCHAR(255),
    temperature FLOAT,
    vibration FLOAT,
    pressure FLOAT,
    machine_speed FLOAT,
    cooling_rate FLOAT,
    cycle_time FLOAT,
    tool_wear FLOAT,
    stress_index FLOAT,
    anomaly_binary BOOLEAN,
    defect_proba FLOAT,
    defect_type VARCHAR(255),
    quality FLOAT,
    final_score FLOAT,
    product_decision VARCHAR(255),
    machine_decision VARCHAR(255),
    final_decision VARCHAR(255)
)
""")
db.commit()
#consume loop
try:
    while True:
        msg=consumer.poll(1.0)
        if msg is None:
            continue
        if msg.error():
            print("Consumer error:", msg.error())
            continue
        data=json.loads(msg.value().decode('utf-8'))
        print("Received:", data)

        #validation  of operator skill level
        Valid_skills=["Expert", "Intermediate"]
        if data["operator_skill_level"] not in Valid_skills:
            print("Invalid operator skill level:", data["operator_skill_level"])
            data["operator_skill_level"]="Intermediate"

        # run prediction and save to mysql
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

        anomaly_value=1 if record['anomaly_binary']== "ANOMALY DETECTED" else 0

        #insert into mysql
        sql = """
        INSERT INTO predictions (
            product_type, product_sensitivity, material_quality, operator_skill_level,
            temperature, vibration, pressure, machine_speed, cooling_rate, cycle_time,
            tool_wear, stress_index, anomaly_binary, defect_proba, defect_type,
            quality, final_score, product_decision, machine_decision, final_decision
        ) VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
        )
        """
        values=(
            record['product_type'],
            record['product_sensitivity'],
            record['material_quality'],
            record['operator_skill_level'],
            record['temperature'],
            record['vibration'],
            record['pressure'],
            record['machine_speed'],
            record['cooling_rate'],
            record['cycle_time'],
            record['tool_wear'],
            record['stress_index'],
            anomaly_value,
            record['defect_proba'],
            record['defect_type'],
            record['quality'], 
            record['final_score'], 
            record['product_decision'], 
            record['machine_decision'], 
            record['final_decision']
        )
        cursor.execute(sql, values)
        db.commit()

        print("Record saved to database")

        # save to CSV
except KeyboardInterrupt:
    print("Consumer stopped")
finally:
    consumer.close()
    cursor.close()
    db.close()
