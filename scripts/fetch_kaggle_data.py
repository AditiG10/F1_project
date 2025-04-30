# fetch_kaggle_data.py
# Load all Kaggle F1 CSVs and print summaries

import os
import pandas as pd

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, '..', 'data', 'raw')

files = [
    'circuits.csv',
    'constructor_results.csv',
    'constructor_standings.csv',
    'constructors.csv',
    'driver_standings.csv',
    'drivers.csv',
    'lap_times.csv',
    'pit_stops.csv',
    'qualifying.csv',
    'races.csv',
    'results.csv',
    'seasons.csv',
    'sprint_results.csv',
    'status.csv'
]

data = {}

for name in files:
    path = os.path.join(data_path, name)
    try:
        df = pd.read_csv(path)
        data[name.replace('.csv', '')] = df
        print(f"Loaded {name} with {df.shape[0]} rows and {df.shape[1]} columns")
    except FileNotFoundError:
        print(f"Missing file: {name}")

print("\nColumn names for each file:")
for k, df in data.items():
    print(f"\n{k}:")
    print(df.columns.tolist())
