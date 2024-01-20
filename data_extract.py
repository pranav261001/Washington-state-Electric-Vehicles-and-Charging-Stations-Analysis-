import json
import pandas as pd
from pymongo import MongoClient

# Step 1: Read Data from JSON File
json_file_path = "C:/Users/pranav/Downloads/Alternative_Fueling_Stations (1).geojson"

with open(json_file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

# Extract only the columns related to electric vehicles
ev_data = []
for feature in data.get("features", []):
    if "properties" in feature and "geometry" in feature:
        properties = feature["properties"]
        geometry = feature["geometry"]

        ev_info = {
            "station_name": properties.get("station_name", None),
            "access_code": properties.get("access_code", None),
            "access_days_time": properties.get("access_days_time", None),
            "fuel_type_code": properties.get("fuel_type_code", None),
            "owner_type_code": properties.get("owner_type_code", None),
            "city": properties.get("city", None),
            "state": properties.get("state", None),
            "street_address": properties.get("street_address", None),
            "zip": properties.get("zip", None),
            "ev_connector_types": properties.get("ev_connector_types", None),
            "ev_level1_evse_num": properties.get("ev_level1_evse_num", None),
            "ev_level2_evse_num": properties.get("ev_level2_evse_num", None),
            "ev_pricing": properties.get("ev_pricing", None),
            "latitude": geometry.get("coordinates", [None, None])[1],
            "longitude": geometry.get("coordinates", [None, None])[0]
        }
        ev_data.append(ev_info)

        
# Step 2: Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["Charg_EV"]
collection = db["charg_stations"]

# Step 3: Store Data in MongoDB
if ev_data:
    collection.insert_many(ev_data)
    print("Electric vehicle data inserted successfully.")
else:
    print("No electric vehicle data to insert.")
# print(ev_data)

# ---------------------------X---------------------------------------------------

# Read the electric vehicle population data from CSV
csv_file_path = "C:/Users/pranav/Desktop/EV_Project(DAP)/Electric_Vehicle_Population_Data (1).csv"
ev_population_data = pd.read_csv(csv_file_path)

# Drop unnecessary columns
columns_to_drop = ['Vehicle Location', '2020 Census Tract', 'DOL Vehicle ID', 'VIN (1-10)']
ev_population_data = ev_population_data.drop(columns=columns_to_drop)

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["EV_Population"]
collection = db["ev_pop_data"]

# Convert DataFrame to a list of dictionaries
ev_population_list = ev_population_data.to_dict(orient='records')

# Insert data into MongoDB
collection.insert_many(ev_population_list)

print("Electric vehicle population data inserted into MongoDB.")
