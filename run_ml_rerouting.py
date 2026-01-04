from ml_rerouting_module import ml_based_rerouting

streets = [
    {"street": "I-80", "avg_severity": 4.1, "vehicle_count": 180},
    {"street": "US-50", "avg_severity": 2.0, "vehicle_count": 60},
    {"street": "CA-99", "avg_severity": 1.6, "vehicle_count": 40}
]

result = ml_based_rerouting(streets)

print("\n🚦 ML-BASED REROUTING OUTPUT")
for k, v in result.items():
    print(f"{k}: {v}")
