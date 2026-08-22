import time
import json
import random
from kafka import KafkaProducer

# Connect to our local Kafka engine
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

print("Starting to stream simulated credit card transactions...")

# Infinite loop to generate live data
while True:
    transaction = {
        "user_id": random.randint(1000, 9999),
        "amount": round(random.uniform(5.0, 500.0), 2),
        "merchant": random.choice(["Amazon", "Uber", "Starbucks", "Target", "Local Grocery"]),
        "timestamp": time.time()
    }

    # Send the transaction to the topic you just created
    producer.send('financial_transactions', value=transaction)
    print(f"Sent: {transaction}")

    # Pause for 1 second before swiping another card
    time.sleep(1)