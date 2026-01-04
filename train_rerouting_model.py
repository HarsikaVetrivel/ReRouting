import pandas as pd
import joblib
import os
from sklearn.cluster import KMeans
from sklearn.metrics import r2_score, accuracy_score, mean_absolute_error


# Ensure models folder exists
os.makedirs("models", exist_ok=True)

# Sample training data (represents historical traffic states)
data = {
    "street": ["I-80", "US-50", "CA-99", "I-5", "SR-91"],
    "avg_severity": [4.2, 3.6, 2.1, 1.4, 2.0],
    "vehicle_count": [180, 150, 70, 40, 60]
}

df = pd.DataFrame(data)

# Traffic load feature
df["traffic_load"] = df["avg_severity"] * df["vehicle_count"]

X = df[["traffic_load"]]

# Train KMeans model
kmeans = KMeans(n_clusters=2, random_state=42)
kmeans.fit(X)

# Save model
joblib.dump(kmeans, "models/rerouting_kmeans.pkl")

print("✅ Rerouting ML model trained and saved")
