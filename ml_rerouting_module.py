import joblib

kmeans = joblib.load("models/rerouting_kmeans.pkl")

def ml_based_rerouting(street_data):
    """
    street_data = list of dicts:
    [
      {"street": "A", "avg_severity": 4.0, "vehicle_count": 160},
      {"street": "B", "avg_severity": 1.8, "vehicle_count": 50}
    ]
    """

    # Compute traffic load
    for s in street_data:
        s["traffic_load"] = s["avg_severity"] * s["vehicle_count"]

    loads = [[s["traffic_load"]] for s in street_data]
    clusters = kmeans.predict(loads)

    for i, s in enumerate(street_data):
        s["cluster"] = clusters[i]

    # Identify high & low load streets
    high_load = max(street_data, key=lambda x: x["traffic_load"])
    low_load = min(street_data, key=lambda x: x["traffic_load"])

    # Simulate rerouting
    reroute_fraction = 0.25
    reduced_vehicles = high_load["vehicle_count"] * reroute_fraction

    # Metrics
    density_reduction = reroute_fraction * 100
    co2_reduction = reroute_fraction * 100
    free_flow_index = round(1 - (high_load["traffic_load"] / 1000), 2)

    return {
        "Divert_From": high_load["street"],
        "Divert_To": low_load["street"],
        "Vehicles_Diverted": int(reduced_vehicles),
        "Free_Flow_Index": free_flow_index,
        "Density_Reduction_%": density_reduction,
        "CO2_Reduction_%": co2_reduction
    }
