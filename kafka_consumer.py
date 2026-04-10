from confluent_kafka import Consumer
import json
import pandas as pd
from src.predict import predict,ProductionSystem
import os

conf= {
    'bootstrap.servers': 'pkc-921jm.us-east-2.aws.confluent.cloud:9092',
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'WCI53EE263UVQOQT',
    'sasl.password': 'cflt6qRZKAdsdXAfJ3mOQoK7MpuY1Zs2EHiYY+3EqYm0lz5YNVPQgcIZ82HCHNEQ',
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
        data=json.loads(msg.value().decode('utf-8'))
        print("Received:", data)
        Valid_skills=["Expert", "Intermediate"]
        if data["operator_skill_level"] not in Valid_skills:
            print("Invalid operator skill level:", data["operator_skill_level"])
            data["operator_skill_level"]="Intermediate"
        input_data= ProductionSystem(**data)
        result=predict(input_data)
         
        print("Prediction Result:", result)
        df=pd.DataFrame(result, index=[0])
        file_path="predictions.csv"
        if not os.path.exists(file_path):
            df.to_csv(file_path, index=False)
        else:
            df.to_csv(file_path, mode='a', header=False, index=False)


except KeyboardInterrupt:
    print("Consumer stopped")
finally:
    consumer.close()