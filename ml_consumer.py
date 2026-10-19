import os
import json
import joblib
import pandas as pd
import psycopg2
from kafka import KafkaConsumer
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Load trained Isolation Forest model
model = joblib.load("fraud_model.pkl")
print("ML model loaded successfully!")

# Connect to PostgreSQL
conn = psycopg2.connect(
    host=os.getenv("DB_HOST", "localhost"),
    database=os.getenv("DB_NAME", "postgres"),
    user=os.getenv("DB_USER", "postgres"),
    password=os.environ["DB_PASSWORD"],
    port=int(os.getenv("DB_PORT", "5432"))
)

cursor = conn.cursor()

# Create fraud alerts table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS fraud_alerts (
        id SERIAL PRIMARY KEY,
        transaction_id VARCHAR(255),
        amount DOUBLE PRECISION,
        merchant_risk INT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")
conn.commit()

print("PostgreSQL connected successfully!")

# Connect to Kafka
consumer = KafkaConsumer(
    "financial_transactions",
    bootstrap_servers=["localhost:9092"],
    auto_offset_reset="latest",
    group_id="fraud-detection-v1",
    enable_auto_commit=True,
    value_deserializer=lambda x: json.loads(x.decode("utf-8"))
)

print("Kafka consumer connected!")
print("Waiting for live transactions...\n")

try:
    for message in consumer:
        data = message.value

        # Extract ML features
        features = pd.DataFrame([{
            "amount": float(data["amount"]),
            "hour": int(data["hour"]),
            "merchant_risk": int(data["merchant_risk"])
        }])

        # Predict anomaly
        prediction = model.predict(features)[0]

        if prediction == -1:
            print(f"SUSPICIOUS TRANSACTION: {data}")

            # Producer has user_id, not transaction_id
            transaction_id = (
                f"{data['user_id']}-{message.partition}-{message.offset}"
            )

            cursor.execute("""
                INSERT INTO fraud_alerts
                (transaction_id, amount, merchant_risk)
                VALUES (%s, %s, %s)
            """, (
                transaction_id,
                float(data["amount"]),
                int(data["merchant_risk"])
            ))

            conn.commit()
            print("Alert saved to PostgreSQL!\n")

        else:
            print(
                f"NORMAL TRANSACTION: "
                f"Amount = {data['amount']}"
            )

except KeyboardInterrupt:
    print("\nConsumer stopped.")

finally:
    consumer.close()
    cursor.close()
    conn.close()
