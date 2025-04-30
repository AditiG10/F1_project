import pandas as pd
import os

base_path = os.path.dirname(os.path.abspath(__file__))
processed_path = os.path.join(base_path, '..', 'data', 'processed')
raw_path = os.path.join(base_path, '..', 'data', 'raw')
os.makedirs(processed_path, exist_ok=True)

# Load cleaned data from merge step
df = pd.read_csv(os.path.join(processed_path, 'cleaned_data.csv'))

# Load supporting data
drivers = pd.read_csv(os.path.join(raw_path, 'drivers.csv'))
constructors = pd.read_csv(os.path.join(raw_path, 'constructors.csv'))

# Merge driver name
drivers['driver_name'] = drivers['forename'] + ' ' + drivers['surname']
df = df.merge(drivers[['driverId', 'driver_name']], on='driverId', how='left')

# Merge constructor name
df = df.merge(constructors[['constructorId', 'name']], on='constructorId', how='left')
df = df.rename(columns={'name': 'constructor_name'})

# Optional: remove rows missing key data
df = df.dropna(subset=['positionOrder', 'points'])

# Reorder columns for clarity
cols = [
    'raceId', 'year', 'circuitId', 'driverId', 'driver_name',
    'constructorId', 'constructor_name', 'grid', 'positionOrder', 'points'
] + [c for c in df.columns if c not in [
    'raceId', 'year', 'circuitId', 'driverId', 'driver_name',
    'constructorId', 'constructor_name', 'grid', 'positionOrder', 'points'
]]
df = df[cols]

# Save cleaned and enriched dataset
df.to_csv(os.path.join(processed_path, 'features_input_ready.csv'), index=False)
print("features_input_ready.csv saved for feature generation and modeling.")
