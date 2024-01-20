import pandas as pd
from sqlalchemy import create_engine
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import seaborn as sns

# PostgreSQL connection strings
postgres_connection_string = "postgresql://postgres:panu2610@localhost:5432/electricvehicles"
engine = create_engine(postgres_connection_string)

# SQL queries to retrieve data
query_string_charging = """SELECT * FROM public."Charging_table";"""
query_string_ev = """SELECT * FROM public."EVpopulation_table";"""

# Reading data into Pandas DataFrames
charging_dataframe = pd.read_sql_query(query_string_charging, engine)
EV_dataframe = pd.read_sql_query(query_string_ev, engine)

# Display the first few rows of each dataset
print("Charging Stations Data:")
print(charging_dataframe.head())

print("\nElectric Vehicle Population Data:")
print(EV_dataframe.head())

# Summary statistics for numerical columns
print("\nSummary Statistics for Charging Stations:")
print(charging_dataframe.describe())

print("\nSummary Statistics for Electric Vehicle Population:")
print(EV_dataframe.describe())

# Pie chart for CAFV Eligibility
plt.figure(figsize=(8, 8))
EV_dataframe['Clean Alternative Fuel Vehicle (CAFV) Eligibility'].value_counts().plot.pie(autopct='%1.1f%%', startangle=90)
plt.title("CAFV Eligibility Distribution")
plt.show()

# Bar chart for Owner Types
plt.figure(figsize=(12, 6))
sns.countplot(x="owner_type_code", data=charging_dataframe)
plt.title("Distribution of Owner Types")
plt.xlabel("Owner Type")
plt.ylabel("Count")
plt.show()

# Bar chart for Access Codes
plt.figure(figsize=(12, 6))
sns.countplot(x="access_code", data=charging_dataframe)
plt.title("Distribution of Access Codes")
plt.xlabel("Access Code")
plt.ylabel("Count")
plt.show()

# Exclude non-numeric columns from the correlation matrix
numeric_columns_charging = charging_dataframe.select_dtypes(include=[float, int]).columns
correlation_matrix_charging = charging_dataframe[numeric_columns_charging].corr()

# Correlation heatmap for numerical variables
plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix_charging, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap - Charging Stations Data")
plt.show()

# Count plots for categorical variables
plt.figure(figsize=(12, 6))
sns.countplot(x="Electric Vehicle Type", data=EV_dataframe)
plt.title("Distribution of Electric Vehicle Types")
plt.xlabel("Electric Vehicle Type")
plt.ylabel("Count")
plt.show()

# Scatter plot for electric vehicle range and base MSRP
plt.figure(figsize=(10, 6))
sns.scatterplot(x="Electric Range", y="Base MSRP", data=EV_dataframe)
plt.title("Scatter Plot - Electric Range vs. Base MSRP")
plt.xlabel("Electric Range")
plt.ylabel("Base MSRP")
plt.show()

# Bar chart for Access Codes
plt.figure(figsize=(12, 6))
sns.countplot(x="Make", data=EV_dataframe)
plt.title("Distribution of Electric vehicle companies")
plt.xlabel("Access Code")
plt.ylabel("Count")
plt.xticks(rotation=90)

plt.show()

plt.figure(figsize=(12, 6))
sns.countplot(x="County", data=EV_dataframe)
plt.title("Distribution of Electric vehicle counties")
plt.xlabel("Access Code")
plt.ylabel("Count")
plt.xticks(rotation=90)

plt.show()

# Count the number of electric vehicles in each city
ev_counts = EV_dataframe['City'].value_counts().reset_index()
ev_counts.columns = ['City', 'ElectricVehicleCount']

# Count the number of charging stations in each city
charging_counts = charging_dataframe['city'].value_counts().reset_index()
charging_counts.columns = ['City', 'ChargingStationCount']

# Merge the two counts dataframes on the 'City' column
city_counts = pd.merge(ev_counts, charging_counts, on='City', how='outer').fillna(0)

# Selecting relevant features for regression
features = city_counts[['ElectricVehicleCount', 'ChargingStationCount']]

# Target variable
target = city_counts['ChargingStationCount']

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

# Initialize and train a Random Forest Regressor
rf_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
rf_regressor.fit(X_train, y_train)

# Make predictions on the testing set
predictions = rf_regressor.predict(X_test)

mse = mean_squared_error(y_test, predictions)
print(f'Mean Squared Error: {mse}')

# Create a new dataframe with actual and predicted values
result_df = pd.DataFrame({'City': X_test.index, 'ActualChargingStationCount': y_test, 'PredictedChargingStationCount': predictions})

# Identify cities with the highest predicted demand for charging stations
top_cities = result_df.sort_values(by='PredictedChargingStationCount', ascending=False).head(5)

# Map city index to actual city names
top_cities['City'] = top_cities['City'].map(dict(zip(ev_counts.index, ev_counts['City'])))

# Print the top cities with names
print("Top 5 Cities with the Highest Predicted Demand for Charging Stations:")
print(top_cities[['City', 'ActualChargingStationCount', 'PredictedChargingStationCount']])
