🚦 How to Run the ML-Based Rerouting Project (Step-by-Step)
Repository

👉 https://github.com/HarsikaVetrivel/ReRouting

✅ PREREQUISITES (IMPORTANT)

Your system must have:

Python 3.10 or 3.11

Git

Kafka running

Flink running

👉 Kafka & Flink setup is already done (assumed).

🟢 STEP 1: CLONE THE REPOSITORY

Open terminal / VS Code terminal and run:

git clone https://github.com/HarsikaVetrivel/ReRouting.git
cd ReRouting

🟢 STEP 2: CHECK PYTHON VERSION
python --version


✔ Must be Python 3.10 / 3.11

If multiple versions exist, use:

py -3.11 --version

🟢 STEP 3: INSTALL REQUIRED PYTHON LIBRARIES

Run once:

pip install pandas numpy scikit-learn joblib


If pip fails:

python -m pip install pandas numpy scikit-learn joblib

🟢 STEP 4: TRAIN THE ML MODELS (ONE-TIME STEP)

This creates the ML model files used by rerouting.

python train_models.py

Expected output:
Traffic Density R² Score: ...
Free Flow Classification Accuracy: ...
CO₂ Estimation MAE: ...
ALL MODELS TRAINED & EVALUATED SUCCESSFULLY

🟢 STEP 5: TRAIN THE ML REROUTING MODEL (ONE-TIME STEP)
python train_rerouting_model.py

Expected output:
Rerouting ML model trained and saved


📌 This creates:

models/rerouting_kmeans.pkl

🟢 STEP 6: TEST ML-BASED REROUTING (STANDALONE)

This step verifies rerouting logic without Kafka/Flink.

python run_ml_rerouting.py

Sample output:
Divert_From: I-80
Divert_To: CA-99
Vehicles_Diverted: 45
Free_Flow_Index: 0.78
Density_Reduction_%: 25.0
CO2_Reduction_%: 25.0


✅ If this works → ML rerouting is correct.

🟢 STEP 7: START KAFKA (IF NOT RUNNING)
zookeeper-server-start.sh config/zookeeper.properties
kafka-server-start.sh config/server.properties


Ensure Kafka topic exists (example):

kafka-topics.sh --create --topic traffic-data --bootstrap-server localhost:9092

🟢 STEP 8: START FLINK
start-cluster.sh


Verify Flink UI:
👉 http://localhost:8081

🟢 STEP 9: INTEGRATE WITH FLINK CONSUMER

In the Flink consumer code, import rerouting module:

from ml_rerouting_module import ml_based_rerouting


Use it after aggregation:

result = ml_based_rerouting(street_data)
print(result)


📌 street_data comes from Flink window output.

🟢 STEP 10: RUN FLINK JOB
flink run -py traffic_consumer.py


(Or whatever your Flink consumer file is called.)

🎯 FINAL OUTPUT (WHAT YOU SHOULD SEE)

For each traffic window:

✔ Free Flow Index

✔ Density Reduction %

✔ CO₂ Reduction %

✔ Divert From → Divert To street

Example:

FreeFlowIndex: 0.81
DensityReduction: 22%
CO2Reduction: 18%
Divert I-80 → CA-99

🧠 HOW TO EXPLAIN THIS TO REVIEW PANEL

“The system uses machine learning models to predict traffic conditions and a clustering-based rerouting module to recommend street-level diversions. The rerouting effectiveness is evaluated using Free Flow Index, traffic density reduction, and CO₂ emission reduction metrics.”

❗ COMMON ERRORS & FIXES
❌ ModuleNotFoundError

Run:

pip install pandas numpy scikit-learn joblib

❌ rerouting_kmeans.pkl not found

Run:

python train_rerouting_model.py

❌ Kafka connection error

Ensure Kafka broker is running on port 9092.

✅ QUICK CHECKLIST FOR TEAMMATE

✔ Repo cloned
✔ Python libraries installed
✔ train_models.py executed
✔ train_rerouting_model.py executed
✔ run_ml_rerouting.py works
✔ Kafka + Flink running