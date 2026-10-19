
import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import IsolationForest

# Generate reproducible simulated transactions
rng = np.random.default_rng(42)

n = 5000

data = pd.DataFrame({
    "amount": rng.exponential(scale=1000, size=n),
    "hour": rng.integers(0, 24, size=n),
    "merchant_risk": rng.integers(1, 6, size=n)
})

# Train an anomaly detection model
model = IsolationForest(
    n_estimators=100,
    contamination=0.05,
    random_state=42,
    n_jobs=1
)

features = ["amount", "hour", "merchant_risk"]

model.fit(data[features])

# Save the trained model
joblib.dump(model, "fraud_model.pkl")

# Test using sample transactions
test_transactions = pd.DataFrame([
    {"amount": 100, "hour": 14, "merchant_risk": 1},
    {"amount": 50000, "hour": 3, "merchant_risk": 5}
])

predictions = model.predict(test_transactions[features])

for i, prediction in enumerate(predictions):
    status = "SUSPICIOUS" if prediction == -1 else "NORMAL"
    print(f"Transaction {i + 1}: {status}")

print("Model saved successfully as fraud_model.pkl")
