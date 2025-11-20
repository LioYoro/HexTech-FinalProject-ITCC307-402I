# Train and save the ML model for SUSTAINALYZE
import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import GradientBoostingRegressor
import os

# Create output directory
os.makedirs('models', exist_ok=True)

# Load dataset
df = pd.read_csv('data/ENERGY_DATA_CLEANED.csv')

# Features and target
X = df.drop(columns=["Co2_emission"])
y_reg = df["Co2_emission"]

# Convert string numbers to numeric
for col in X.columns:
    if X[col].dtype == 'object':
        X[col] = X[col].str.replace(",", "", regex=False)
        X[col] = pd.to_numeric(X[col], errors='coerce')

# Fill missing values
X = X.fillna(X.median(numeric_only=True))

# Scale features
scaler = StandardScaler()
X_scaled = pd.DataFrame(scaler.fit_transform(X), columns=X.columns)

# Split data
X_train, X_test, y_train_reg, y_test_reg = train_test_split(
    X_scaled, y_reg, test_size=0.2, random_state=42
)

# Train Gradient Boosting model
gb_reg = GradientBoostingRegressor(
    n_estimators=400,
    learning_rate=0.05,
    subsample=0.9,
    max_depth=10,
    min_samples_split=4,
    min_samples_leaf=2,
    random_state=42
)

gb_reg.fit(X_train, y_train_reg)

# Define thresholds based on training set
low_thresh = np.percentile(y_train_reg, 33)
high_thresh = np.percentile(y_train_reg, 66)

# Save model, scaler, and thresholds
with open('models/gb_reg_model.pkl', 'wb') as f:
    pickle.dump(gb_reg, f)

with open('models/scaler.pkl', 'wb') as f:
    pickle.dump(scaler, f)

thresholds = {"low": low_thresh, "high": high_thresh}
with open('models/co2_thresholds.pkl', 'wb') as f:
    pickle.dump(thresholds, f)

print("✅ Model training complete! Model, scaler, and thresholds saved.")
