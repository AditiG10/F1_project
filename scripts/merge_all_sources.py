import pandas as pd
import os

base_path = os.path.dirname(os.path.abspath(__file__))
raw_path = os.path.join(base_path, '..', 'data', 'raw')
processed_path = os.path.join(base_path, '..', 'data', 'processed')
os.makedirs(processed_path, exist_ok=True)

# Load raw datasets
results = pd.read_csv(os.path.join(raw_path, 'results.csv'))
races = pd.read_csv(os.path.join(raw_path, 'races.csv'))

# Merge races into results to bring in year and circuitId
df = results.merge(races[['raceId', 'year', 'circuitId']], on='raceId', how='left')

# Save the merged data
df.to_csv(os.path.join(processed_path, 'cleaned_data.csv'), index=False)
print("cleaned_data.csv created successfully with circuitId and year.")
