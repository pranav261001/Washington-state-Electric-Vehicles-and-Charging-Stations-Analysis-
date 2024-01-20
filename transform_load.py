import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine

# MongoDB connection settings
mongo_connection_string = "mongodb://localhost:27017/"
mongo_db_name = "Charg_EV"
mongo_collection_name = "charg_stations"

mongo_db_pop = "EV_Population"
mongo_collection_pop = "ev_pop_data"

# PostgreSQL connection settings
postgres_connection_string = "postgresql://postgres:panu2610@localhost:5432/electricvehicles"

# Connect to MongoDB
mongo_client = MongoClient(mongo_connection_string)
mongo_db = mongo_client[mongo_db_name]
mongo_collection = mongo_db[mongo_collection_name]

mongo_db_1 = mongo_client[mongo_db_pop]
mongo_collection_1 = mongo_db_1[mongo_collection_pop]

# Read data from MongoDB into a pandas DataFrame
mongo_df = pd.DataFrame(list(mongo_collection.find()))

mongo_df_1 = pd.DataFrame(list(mongo_collection_1.find()))

# Transform the data if needed
# Example: Drop unwanted columns
mongo_df = mongo_df.drop(columns=["_id"])

mongo_df_1 = mongo_df_1.drop(columns=["_id"])


# Connect to PostgreSQL
engine = create_engine(postgres_connection_string)

# Write the DataFrame to PostgreSQL
mongo_df.to_sql("Charging_table", engine, if_exists="replace", index=False)

mongo_df_1.to_sql("EVpopulation_table", engine, if_exists="replace", index=False)


# Close MongoDB connection
mongo_client.close()

# -------------------------------------------X--------------------------------------------------------


# MongoDB connection settings
mongo_connection_string = "mongodb://localhost:27017/"
mongo_db_pop = "EV_Population"
mongo_collection_pop = "ev_pop_data"

# PostgreSQL connection settings
postgres_connection_string = "postgresql://postgres:panu2610@localhost:5432/electricvehicles"

# Connect to MongoDB
mongo_client = MongoClient(mongo_connection_string)
mongo_db_1 = mongo_client[mongo_db_pop]
mongo_collection_1 = mongo_db_1[mongo_collection_pop]

# Read data from MongoDB into a pandas DataFrame
mongo_df_1 = pd.DataFrame(list(mongo_collection_1.find()))

# Transform the data if needed
# Example: Drop unwanted columns
mongo_df_1 = mongo_df_1.drop(columns=["_id"])

# Connect to PostgreSQL
engine = create_engine(postgres_connection_string)

# Write the DataFrame to PostgreSQL
mongo_df_1.to_sql("population_table", engine, if_exists="replace", index=False)

# Close MongoDB connection
mongo_client.close()