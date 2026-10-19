# Real-Time Fraud Detection ML Pipeline

A real-time transaction anomaly detection system built using **Python, Apache Kafka, Isolation Forest, PostgreSQL, and Docker**.

## Project Overview

This project demonstrates how streaming transactions can be analyzed using machine learning to identify unusual transaction patterns.

A Python producer generates simulated financial transactions and publishes them to Apache Kafka. A consumer processes incoming transactions, applies a trained Isolation Forest model, and stores suspicious transaction alerts in PostgreSQL.

**Note:** This is a demonstration prototype trained on synthetic data. Anomaly detection does not necessarily mean a transaction is fraudulent.

## Architecture

```text
Python Transaction Producer
           |
           v
      Apache Kafka
           |
           v
     Python Consumer
           |
           v
 Isolation Forest Model
           |
     +-----+------+
     |            |
   Normal      Suspicious
     |            |
  Console      PostgreSQL
  Output       Fraud Alerts
```

## Technologies Used

- Python — transaction generation and stream processing
- Apache Kafka — transaction streaming
- Scikit-learn — Isolation Forest anomaly detection
- PostgreSQL — suspicious transaction alert storage
- Docker Compose — Kafka and PostgreSQL services
- Pandas and NumPy — data generation and feature processing

## Machine Learning Model

The project uses **Isolation Forest**, an unsupervised anomaly detection algorithm.

The model is trained on 5,000 synthetically generated transactions using three features:

- Transaction amount
- Hour of transaction
- Merchant risk score

The model classifies transactions as normal (`1`) or anomalous (`-1`).

## Project Files

| File | Description |
|---|---|
| `producer.py` | Generates transactions and sends them to Kafka |
| `ml_consumer.py` | Consumes Kafka messages, runs predictions, and stores alerts |
| `train_model.py` | Trains and saves the Isolation Forest model |
| `docker-compose.yml` | Defines Kafka, Kafka UI, and PostgreSQL services |
| `requirements.txt` | Python dependencies |
| `.env.example` | Example environment configuration |

The trained model file `fraud_model.pkl` is generated locally and excluded from Git.

## Running the Project

### 1. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 2. Configure environment variables

Copy `.env.example` to `.env` and set your local database credentials.

### 3. Start Docker services

```bash
docker compose up -d kafka postgres
```

### 4. Train the model

```bash
python train_model.py
```

### 5. Start the consumer

```bash
python ml_consumer.py
```

### 6. Start the producer in another terminal

```bash
python producer.py
```

The consumer prints normal and suspicious transaction results. Suspicious transaction alerts are inserted into PostgreSQL.

## Verify Fraud Alerts

```bash
docker exec fraud-postgres psql -U postgres -d postgres -c "SELECT * FROM fraud_alerts ORDER BY id DESC LIMIT 10;"
```

## Limitations and Future Improvements

- The model uses synthetic rather than real banking transaction data.
- Merchant risk scores are manually assigned.
- Anomalies are not confirmed fraudulent transactions.
- Kafka offset handling and database deduplication need improvement for reliable recovery.
- Future improvements could include a dashboard, real datasets, model evaluation, and automated tests.


## Real-World Dataset Evaluation

In addition to the synthetic transaction streaming prototype, this project includes a separate Isolation Forest evaluation using the Kaggle Credit Card Fraud Detection dataset.

**Dataset:** 284,807 transactions, including 492 labeled fraudulent transactions.

**Methodology:**
- Used a stratified 60% training, 20% validation, and 20% testing split.
- Trained Isolation Forest models using 30 input features.
- Compared contamination values of 0.002, 0.003, and 0.005.
- Selected contamination = 0.003 based on validation F1-score.
- Evaluated the selected model on the held-out test split.

**Test Results:**

| Metric | Result |
|---|---:|
| Accuracy | 99.67% |
| Fraud Precision | 20.26% |
| Fraud Recall | 31.31% |
| Fraud F1-score | 24.60% |
| True Positives | 31 |
| False Positives | 122 |
| False Negatives | 68 |
| True Negatives | 56,741 |

The results highlight the challenges of detecting rare fraudulent transactions in highly imbalanced datasets. High overall accuracy does not necessarily indicate strong fraud detection performance.

**Run the evaluation:**

```bash
python train_real_model.py
```

Download `creditcard.csv` from the Kaggle Credit Card Fraud Detection dataset and place it inside the `data/` directory before running.

**Note:** This real-data model is evaluated separately. The current Kafka streaming consumer continues to use the original three-feature synthetic-data model.

## Author

Prince Raj

Computer Science and Engineering — Artificial Intelligence and Machine Learning
