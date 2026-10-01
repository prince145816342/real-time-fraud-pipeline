import psycopg2
import json
from kafka import KafkaConsumer

# 1. Connect to your PostgreSQL database running in Docker
try:
    conn = psycopg2.connect(
        host="localhost",
        database="postgres", # Change if you named your DB differently
        user="postgres",     # Change if your DB user is different
        password="password", # Change to your DB password
        port="5432"
    )
    cursor = conn.cursor()
    
    # Create the table if it doesn't exist yet
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fraud_alerts (
            id SERIAL PRIMARY KEY,
            transaction_id VARCHAR(255),
            amount FLOAT,
            merchant_risk INT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    print("Database connected and table ready!")

except Exception as e:
    print(f"Database connection failed: {e}")

# 2. Your existing Kafka Consumer setup goes here
# consumer = KafkaConsumer(...)

# 3. Inside your message loop, save the fraud alerts to the database
# for message in consumer:
#     data = json.loads(message.value)
#     prediction = model.predict([features])
#     
#     if prediction == -1:  # Assuming -1 means Fraud in Isolation Forest
#         print(f"FRAUD DETECTED: {data['transaction_id']}")
#         
#         # Insert into PostgreSQL
#         cursor.execute('''
#             INSERT INTO fraud_alerts (transaction_id, amount, merchant_risk)
#             VALUES (%s, %s, %s)
#         ''', (data['transaction_id'], data['amount'], data['merchant_risk']))
#         conn.commit()