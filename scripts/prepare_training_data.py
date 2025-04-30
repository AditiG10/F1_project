import pandas as pd
import os
from sklearn.model_selection import train_test_split

base_path = os.path.dirname(os.path.abspath(__file__))
features_path = os.path.join(base_path, '..', 'data', 'features')
output_path = os.path.join(base_path, '..', 'data', 'model_input')
os.makedirs(output_path, exist_ok=True)

# Load engineered features
df = pd.read_csv(os.path.join(features_path, 'features_ready.csv'))

# Drop rows with missing values in important columns
df = df.dropna(subset=[
    'rolling_points_driver', 'constructor_dnf_rate',
    'avg_finish_season', 'synergy', 'positionClass'
])

# Select input features
features = [
    'rolling_points_driver',
    'constructor_dnf_rate',
    'avg_finish_season',
    'synergy',
    'grid',
    'constructor_avg_points'
]

# Multi-class target: 0 (non-podium), 1 (1st), 2 (2nd), 3 (3rd)
target = 'positionClass'

X = df[features]
y = df[target]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Save to disk
X_train.to_csv(os.path.join(output_path, 'X_train.csv'), index=False)
X_test.to_csv(os.path.join(output_path, 'X_test.csv'), index=False)
y_train.to_csv(os.path.join(output_path, 'y_train.csv'), index=False)
y_test.to_csv(os.path.join(output_path, 'y_test.csv'), index=False)

print("Training and test sets saved with multi-class target.")
