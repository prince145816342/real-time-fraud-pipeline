
import pandas as pd
import joblib

from sklearn.ensemble import IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# 1. Load dataset
df = pd.read_csv("data/creditcard.csv")

X = df.drop(columns=["Class"])
y = df["Class"]

print("Dataset shape:", df.shape)

# 2. Split into 60% training, 20% validation, 20% testing
X_train, X_temp, y_train, y_temp = train_test_split(
    X,
    y,
    test_size=0.4,
    random_state=42,
    stratify=y
)

X_val, X_test, y_val, y_test = train_test_split(
    X_temp,
    y_temp,
    test_size=0.5,
    random_state=42,
    stratify=y_temp
)

print("Training samples:", len(X_train))
print("Validation samples:", len(X_val))
print("Testing samples:", len(X_test))

# 3. Compare contamination settings on validation data
contamination_values = [0.002, 0.003, 0.005]

best_f1 = -1
best_contamination = None
best_model = None

for contamination in contamination_values:

    pipeline = Pipeline([
        ("scaler", StandardScaler()),
        ("model", IsolationForest(
            n_estimators=100,
            contamination=contamination,
            random_state=42,
            n_jobs=-1
        ))
    ])

    pipeline.fit(X_train)

    # Isolation Forest: -1 = anomaly, 1 = normal
    predictions = pipeline.predict(X_val)
    y_pred = (predictions == -1).astype(int)

    precision = precision_score(y_val, y_pred, zero_division=0)
    recall = recall_score(y_val, y_pred, zero_division=0)
    f1 = f1_score(y_val, y_pred, zero_division=0)

    print(f"\nContamination: {contamination}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-score: {f1:.4f}")

    if f1 > best_f1:
        best_f1 = f1
        best_contamination = contamination
        best_model = pipeline

# 4. Final evaluation on held-out test split
print("\n================================")
print("BEST VALIDATION MODEL")
print("================================")
print("Selected contamination:", best_contamination)
print("Validation F1-score:", round(best_f1, 4))

test_predictions = best_model.predict(X_test)
y_test_pred = (test_predictions == -1).astype(int)

print("\nFINAL TEST CONFUSION MATRIX:")
print(confusion_matrix(y_test, y_test_pred))

print("\nFINAL TEST CLASSIFICATION REPORT:")
print(classification_report(
    y_test,
    y_test_pred,
    digits=4,
    zero_division=0
))

# 5. Save the selected model
joblib.dump(best_model, "fraud_model_real.pkl")

print("\nSelected real-data model saved successfully!")
