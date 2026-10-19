
import time
import json
import random
from datetime import datetime
from kafka import KafkaProducer

# Simulated merchant risk scores (1 = low, 5 = high)
merchant_risks = {
    "Amazon": 2,
    "Uber": 3,
    "Starbucks": 1,
    "Target": 2,
    "Local Grocery": 1
}

producer = KafkaProducer(
    bootstrap_servers=["localhost:9092"],
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("Starting real-time transaction streaming...")

try:
    while True:
        merchant = random.choice(list(merchant_risks.keys()))

        # Occasionally generate unusually large transactions
        amount = (
            random.uniform(10000, 50000)
            if random.random() < 0.10
            else random.uniform(5, 500)
        )

        transaction = {
            "user_id": random.randint(1000, 9999),
            "amount": round(amount, 2),
            "merchant": merchant,
            "merchant_risk": merchant_risks[merchant],
            "hour": datetime.now().hour,
            "timestamp": time.time()
        }

        future = producer.send(
            "financial_transactions",
            value=transaction
        )

        # Wait for Kafka to acknowledge the message
        future.get(timeout=10)

        print(f"Sent: {transaction}")
        time.sleep(1)

except KeyboardInterrupt:
    print("\nProducer stopped.")

finally:
    producer.close()
