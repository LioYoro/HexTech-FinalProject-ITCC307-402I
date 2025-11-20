"""
Verification script to test model training and prediction functionality.
Run this after training the model with train_model.py to verify everything works.
"""
import pickle
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler

def verify_model():
    print("=" * 60)
    print("SUSTAINALYZE MODEL VERIFICATION")
    print("=" * 60)
    
    try:
        # Load model components
        print("\n1. Loading model components...")
        with open('models/gb_reg_model.pkl', 'rb') as f:
            model = pickle.load(f)
        print("   ✓ Gradient Boosting model loaded")
        
        with open('models/scaler.pkl', 'rb') as f:
            scaler = pickle.load(f)
        print("   ✓ Feature scaler loaded")
        
        with open('models/co2_thresholds.pkl', 'rb') as f:
            thresholds = pickle.load(f)
        print("   ✓ CO2 thresholds loaded")
        print(f"     Low threshold: {thresholds['low']:.2f} kt CO2")
        print(f"     High threshold: {thresholds['high']:.2f} kt CO2")
        
        # Load dataset for verification
        print("\n2. Loading dataset...")
        df = pd.read_csv('data/ENERGY_DATA_CLEANED.csv')
        print(f"   ✓ Dataset loaded: {len(df)} records")
        
        # Get feature columns
        feature_columns = [
            "Access to electricity (% of population)",
            "Access to clean fuels for cooking",
            "Renewable-electricity-generating-capacity-per-capita",
            "Financial flows to developing countries (US $)",
            "Renewable energy share in the total final energy consumption (%)",
            "Electricity from fossil fuels (TWh)",
            "Electricity from nuclear (TWh)",
            "Electricity from renewables (TWh)",
            "Low-carbon electricity (% electricity)",
            "Primary energy consumption per capita (kWh/person)",
            "Energy intensity level of primary energy (MJ/$2017 PPP GDP)",
            "Renewables (% equivalent primary energy)",
            "gdp_growth",
            "gdp_per_capita",
            "Density_(P/Km2)",
            "Land Area(Km2)",
            "Latitude",
            "Longitude"
        ]
        
        # Prepare test data
        print("\n3. Testing model predictions...")
        X = df[feature_columns].copy()
        
        # Convert to numeric
        for col in X.columns:
            if X[col].dtype == 'object':
                X[col] = X[col].str.replace(",", "", regex=False)
                X[col] = pd.to_numeric(X[col], errors='coerce')
        
        X = X.fillna(X.median(numeric_only=True))
        X_scaled = scaler.transform(X)
        
        # Make predictions
        predictions = model.predict(X_scaled)
        
        print(f"   ✓ Predictions made for {len(predictions)} records")
        print(f"     Min CO2: {predictions.min():.2f} kt")
        print(f"     Max CO2: {predictions.max():.2f} kt")
        print(f"     Mean CO2: {predictions.mean():.2f} kt")
        
        # Sample predictions
        print("\n4. Sample predictions:")
        for i in range(0, min(5, len(predictions))):
            pred = predictions[i]
            if pred <= thresholds['low']:
                cat = "Low"
            elif pred <= thresholds['high']:
                cat = "Medium"
            else:
                cat = "High"
            print(f"   Sample {i+1}: {pred:.2f} kt CO2 → {cat} emissions")
        
        print("\n" + "=" * 60)
        print("✓ MODEL VERIFICATION SUCCESSFUL!")
        print("=" * 60)
        print("\nYou can now:")
        print("1. Run: python app.py (to start the Flask backend)")
        print("2. Visit: http://localhost/sustainalyze/frontend/")
        print("3. Enter values and make predictions!")
        
    except FileNotFoundError as e:
        print(f"\n✗ Error: {e}")
        print("Make sure you have run: python train_model.py")
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")

if __name__ == "__main__":
    verify_model()
