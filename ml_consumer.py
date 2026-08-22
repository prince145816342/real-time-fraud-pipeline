import json
import numpy as np
from datetime import datetime
from kafka import KafkaConsumer
from sklearn.ensemble import IsolationForest

# 1. Warm up the Advanced AI model
print("Booting up the Multi-Variable Anomaly Detection model...")
model = IsolationForest(contamination=0.05, random_state=42)

# 2. Risk weights for Categorical Data (Merchants)
merchant_risk = {
    "Amazon": 1.0,
    "Target": 1.2,
    "Local Grocery": 0.5,
    "Starbucks": 0.3,
    "Uber": 1.5
}

# Generate baseline 3D training data [amount, hour_of_day, merchant_risk]
# Normal amounts: $5-$150, Hours: 8 AM - 10 PM (8-22), Risk: 0.3-1.5
baseline_data = np.column_stack((
    np.random.uniform(5.0, 150.0, 500),
    np.random.uniform(8.0, 22.0, 500),
    np.random.uniform(0.3, 1.5, 500)
))
model.fit(baseline_data)
print("Model ready! Connecting to the data stream...")

# 3. Connect to the Kafka pipeline
consumer = KafkaConsumer(
    'financial_transactions',
    bootstrap_servers=['localhost:9092'],
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

# 4. Analyze the live stream
for message in consumer:
    transaction = message.value
    
    # Feature Engineering: Extract Hour from Timestamp
    dt_obj = datetime.fromtimestamp(transaction['timestamp'])
    hour_of_day = dt_obj.hour + (dt_obj.minute / 60.0)
    
    # Feature Engineering: Map Merchant to Risk Score
    risk_score = merchant_risk.get(transaction['merchant'], 1.0)
    
    # Format the 3D data array for the model
    features = np.array([[transaction['amount'], hour_of_day, risk_score]])
    
    # Predict (-1 means Anomaly/Fraud, 1 means Normal)
    prediction = model.predict(features)
    
    if prediction[0] == -1:
        print(f"🚨 FRAUD ALERT: Suspicious pattern detected! {transaction}")
    else:
        print(f"✅ CLEAR: Normal activity. {transaction}")