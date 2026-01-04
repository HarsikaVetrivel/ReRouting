import pandas as pd
import joblib
import os

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import r2_score, accuracy_score, mean_absolute_error

# ---------------- CONFIG ----------------
DATASET_PATH = "traffic_sample.csv"
MODEL_DIR = "models"
os.makedirs(MODEL_DIR, exist_ok=True)

print("📂 Loading dataset...")

# ---------------- LOAD DATA ----------------
df = pd.read_csv(DATASET_PATH)
df = df.dropna()

print(f"✅ Dataset loaded with {len(df)} rows")

# ---------------- FEATURE ENGINEERING ----------------
print("⚙️ Feature engineering...")

df["Weather_Condition"] = df["Weather_Condition"].astype("category").cat.codes

# Traffic density proxy
df["Traffic_Density"] = df["Severity"] * (1 / df["Visibility(mi)"])

# Free flow label
df["Free_Flow"] = df["Traffic_Density"].apply(lambda x: 1 if x < 1.5 else 0)

# CO2 proxy
df["Vehicle_Count"] = df["Severity"] * 10
df["CO2"] = df["Vehicle_Count"] * df["Severity"] * 0.12

# =====================================================
# MODEL 1: TRAFFIC DENSITY PREDICTION (Random Forest)
# =====================================================
print("\n🤖 Training Traffic Density Model (Random Forest)...")

X1 = df[["Severity", "Visibility(mi)", "Weather_Condition"]]
y1 = df["Traffic_Density"]

X1_train, X1_test, y1_train, y1_test = train_test_split(
    X1, y1, test_size=0.2, random_state=42
)

density_model = RandomForestRegressor(
    n_estimators=50,
    random_state=42
)
density_model.fit(X1_train, y1_train)

# Evaluation
y1_pred = density_model.predict(X1_test)
r2 = r2_score(y1_test, y1_pred)

print(f"📊 Traffic Density R² Score: {round(r2, 3)}")

joblib.dump(density_model, os.path.join(MODEL_DIR, "density_model.pkl"))
print("✅ Density model saved")

# =====================================================
# MODEL 2: FREE FLOW PREDICTION (Logistic Regression)
# =====================================================
print("\n🤖 Training Free Flow Model (Logistic Regression)...")

X2 = df[["Severity", "Visibility(mi)"]]
y2 = df["Free_Flow"]

flow_model = LogisticRegression(max_iter=1000)
flow_model.fit(X2, y2)

# Evaluation
y2_pred = flow_model.predict(X2)
accuracy = accuracy_score(y2, y2_pred)

print(f"📊 Free Flow Classification Accuracy: {round(accuracy * 100, 2)}%")

joblib.dump(flow_model, os.path.join(MODEL_DIR, "flow_model.pkl"))
print("✅ Free flow model saved")

# =====================================================
# MODEL 3: CO2 EMISSION ESTIMATION (Linear Regression)
# =====================================================
print("\n🤖 Training CO₂ Emission Model (Linear Regression)...")

X3 = df[["Vehicle_Count", "Severity"]]
y3 = df["CO2"]

co2_model = LinearRegression()
co2_model.fit(X3, y3)

# Evaluation
y3_pred = co2_model.predict(X3)
mae = mean_absolute_error(y3, y3_pred)

print(f"📊 CO₂ Estimation MAE: {round(mae, 4)}")

joblib.dump(co2_model, os.path.join(MODEL_DIR, "co2_model.pkl"))
print("✅ CO₂ model saved")

print("\n🎉 ALL MODELS TRAINED & EVALUATED SUCCESSFULLY 🎉")
