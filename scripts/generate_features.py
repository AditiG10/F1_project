import pandas as pd
import os

base_path = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_path, '..', 'data', 'processed')
out_path = os.path.join(base_path, '..', 'data', 'features')
os.makedirs(out_path, exist_ok=True)

in_path = os.path.join(data_path, 'features_input_ready.csv')
df = pd.read_csv(in_path)

# Driver performance features
df['podium'] = df['positionOrder'].apply(lambda x: 1 if x <= 3 else 0)
df['avg_finish_season'] = df.groupby(['year', 'driverId'])['positionOrder'].transform('mean')
df['points_per_race'] = df.groupby('driverId')['points'].transform(lambda x: x.rolling(3, min_periods=1).mean())
df['podium_count'] = df.groupby('driverId')['podium'].cumsum() - df['podium']

# Constructor insights
df['dnf_flag'] = df['positionOrder'].isna() | (df['positionOrder'] > 30)
df['constructor_dnf_rate'] = df.groupby(['year', 'constructorId'])['dnf_flag'].transform('mean')
df['constructor_avg_points'] = df.groupby(['year', 'constructorId'])['points'].transform('mean')
df['synergy'] = df.groupby(['driverId', 'constructorId'])['points'].transform('mean')

# Race outcome prediction features
df['rolling_points_driver'] = df.groupby('driverId')['points'].transform(lambda x: x.rolling(3, min_periods=1).mean())
df['win'] = df['positionOrder'].apply(lambda x: 1 if x == 1 else 0)

# Circuit win ratio (if circuitId exists)
if 'circuitId' in df.columns:
    df['circuit_win_ratio'] = df.groupby(['driverId', 'circuitId'])['win'].transform(
        lambda x: x.cumsum() / (x.index.to_series().groupby([df['driverId'], df['circuitId']]).cumcount() + 1)
    )

# NEW: Create position class for multi-class classification
def classify_position(pos):
    if pos == 1:
        return 1
    elif pos == 2:
        return 2
    elif pos == 3:
        return 3
    else:
        return 0

df['positionClass'] = df['positionOrder'].apply(classify_position)

# Save final feature set
feat_path = os.path.join(out_path, 'features_ready.csv')
df.to_csv(feat_path, index=False)
print("features_ready.csv saved with multi-class target column (positionClass).")
