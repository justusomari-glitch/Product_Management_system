
from confluent_kafka import Producer
import json
import random
import time

conf= {
    'bootstrap.servers': 'pkc-921jm.us-east-2.aws.confluent.cloud:9092',
    'sasl.mechanisms': 'PLAIN',
    'security.protocol': 'SASL_SSL',
    'sasl.username': 'WCI53EE263UVQOQT',
    'sasl.password': 'cflt6qRZKAdsdXAfJ3mOQoK7MpuY1Zs2EHiYY+3EqYm0lz5YNVPQgcIZ82HCHNEQ'
}

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

producer=Producer(conf)

def generate_random_data():
    data={
        "product_type": random.choice(["Aluminium Plate", "High Strength Steel","Plastic Component"]),
        "product_sensitivity": random.choice(["Low", "Medium", "High"]),
        "material_quality": random.choice(["Low", "Medium", "High"]),
        "operator_skill_level": random.choice(["Expert", "Intermediate"]),
        "temperature": round(random.uniform(20.0, 500.0), 2),
        "vibration": round(random.uniform(0.0, 100.0), 2),
        "pressure": round(random.uniform(1.0, 200.0), 2),
        "machine_speed": round(random.uniform(50.0, 2500.0), 1),
        "cooling_rate": round(random.uniform(3.0, 50.0), 1),
        "cycle_time": round(random.uniform(4.0, 100.0), 1),
        "tool_wear": round(random.uniform(2.0, 100.0), 1),
        "stress_index": round(random.uniform(0.0, 60.0), 1)
    }
    return data
print('Producer started')
while True:
    data=generate_random_data()
    producer.produce('raw_data', json.dumps(data).encode('utf-8'))
    producer.poll(10)
    print(f"Sent: {data}")
    time.sleep(3)
