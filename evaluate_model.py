import pandas as pd
from joblib import load
from sklearn.metrics import classification_report

# Load model and data
model = load("random_forest_model.joblib")
data = pd.read_csv("web_attacks_balanced.csv")
X = data.drop("Label", axis=1)
y = data["Label"]

# Evaluate model
y_pred = model.predict(X)
print("Classification Report:")
print(classification_report(y, y_pred))

# Feature importance
importances = model.feature_importances_
feature_importance = pd.Series(importances, index=X.columns).sort_values(ascending=False)
print("\nTop 10 Features:")
print(feature_importance.head(10))

# Demo data
demo_data = {
    "BENIGN": [
        62015, 1261, 51885.0, 1599, 53.0, 17.0, 181, 76978.0, 2.0, 2.0, 78.0, 206.0, 39.0, 39.0, 39.0, 0.0,
        103.0, 103.0, 103.0, 0.0, 3689.365793, 51.96289849, 25659.33333, 44436.34082, 76970.0, 4.0, 4.0, 4.0,
        0.0, 4.0, 4.0, 4.0, 4.0, 0.0, 4.0, 4.0, 0.0, 0.0, 0.0, 0.0, 64.0, 64.0, 25.98144925, 25.98144925,
        39.0, 103.0, 64.6, 35.05424368, 1228.8, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 80.75, 39.0,
        103.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 2.0, 78.0, 2.0, 206.0, -1.0, -1.0, 1.0, 32.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0
    ],
    "Web Attack – Brute Force": [
        4022, 845, 44380.0, 1601, 80.0, 6.0, 196, 5185118.0, 7.0, 7.0, 1022.0, 2321.0, 372.0, 0.0, 146.0,
        184.0787875, 1047.0, 0.0, 331.5714286, 439.6592837, 644.7297824, 2.700034985, 398855.2308, 1372180.71,
        4963956.0, 4.0, 221162.0, 36860.33333, 56141.02125, 141434.0, 4.0, 5185004.0, 864167.3333, 2027593.314,
        5001548.0, 879.0, 0.0, 0.0, 0.0, 0.0, 232.0, 232.0, 1.350017492, 1.350017492, 0.0, 1047.0, 222.8666667,
        331.3239387, 109775.5524, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 238.7857143, 146.0, 331.5714286,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 7.0, 1022.0, 7.0, 2321.0, 29200.0, 252.0, 3.0, 32.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0
    ],
    "Web Attack – Sql Injection": [
        3698, 845, 36196.0, 1601, 80.0, 6.0, 40, 5006127.0, 4.0, 4.0, 447.0, 530.0, 447.0, 0.0, 111.75, 223.5,
        530.0, 0.0, 132.5, 265.0, 195.1608499, 1.59804176, 715161.0, 1889619.815, 5000415.0, 4.0, 5712.0, 1904.0,
        2168.235227, 4266.0, 4.0, 5005996.0, 1668665.333, 2885896.206, 5001011.0, 1407.0, 0.0, 0.0, 0.0, 0.0,
        136.0, 136.0, 0.79902088, 0.79902088, 0.0, 530.0, 108.5555556, 216.4053552, 46831.27778, 0.0, 0.0, 0.0,
        1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 122.125, 111.75, 132.5, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 4.0, 447.0, 4.0,
        530.0, 29200.0, 235.0, 1.0, 32.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ],
    "Web Attack – XSS": [
        4024, 845, 44382.0, 1601, 80.0, 6.0, 198, 1000000.0, 8.0, 6.0, 800.0, 600.0, 200.0, 0.0, 100.0,
        150.0, 300.0, 0.0, 100.0, 200.0, 1400.0, 14.0, 83333.3333, 300000.0, 900000.0, 4.0, 100000.0, 12500.0,
        20000.0, 40000.0, 4.0, 900000.0, 180000.0, 500000.0, 900000.0, 400.0, 0.0, 0.0, 0.0, 0.0, 256.0,
        192.0, 8.0, 6.0, 0.0, 300.0, 150.0, 200.0, 100000.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.75,
        200.0, 100.0, 100.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 8.0, 800.0, 6.0, 600.0, 29200.0, 252.0,
        4.0, 32.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ]
}

# Test demo data directly
for label, values in demo_data.items():
    input_data = pd.DataFrame([values], columns=X.columns)
    prediction = model.predict(input_data)[0]
    probs = model.predict_proba(input_data)[0]
    prob_dict = {cls: float(prob) for cls, prob in zip(model.classes_, probs)}
    print(f"\nLabel: {label}")
    print(f"Prediction: {prediction}")
    print(f"Probabilities: {prob_dict}")
    # Feature analysis for XSS
    if label == "Web Attack – XSS" and prediction != "Web Attack – XSS":
        xss_df = input_data
        bf_df = pd.DataFrame([demo_data["Web Attack – Brute Force"]], columns=X.columns)
        diff = (xss_df - bf_df).abs().mean()
        key_features = ['Flow Duration', 'Fwd Packet Length Max', 'Packet Length Variance', 'Flow Bytes/s']
        print(f"Feature differences for key features: {diff[key_features].to_dict()}")