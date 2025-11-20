# Flask API for SUSTAINALYZE
from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import pickle
import json

app = Flask(__name__)
CORS(app)

# Load trained model, scaler, and thresholds
with open('models/gb_reg_model.pkl', 'rb') as f:
    gb_reg = pickle.load(f)

with open('models/scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

with open('models/co2_thresholds.pkl', 'rb') as f:
    thresholds = pickle.load(f)

# Feature order
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

def co2_category(pred):
    """Convert numeric CO2 emission to Low/Medium/High category."""
    if pred <= thresholds["low"]:
        return "Low"
    elif pred <= thresholds["high"]:
        return "Medium"
    else:
        return "High"

@app.route('/', methods=['GET'])
def home():
    """Root route - indicates API is running."""
    return jsonify({
        "message": "SUSTAINALYZE Backend API",
        "status": "running",
        "endpoints": {
            "/api/predict": "POST - Predict CO2 emissions",
            "/api/features": "GET - Get feature list and ranges"
        }
    })

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict CO2 emissions and category from input features."""
    try:
        data = request.json
        
        # Create DataFrame with input values
        input_df = pd.DataFrame([data])
        
        # Reorder columns to match training
        input_df = input_df[feature_columns]
        
        # Scale features
        input_scaled = scaler.transform(input_df)
        
        # Predict
        pred_value = gb_reg.predict(input_scaled)[0]
        pred_cat = co2_category(pred_value)
        
        return jsonify({
            "success": True,
            "co2_emission": round(pred_value, 2),
            "category": pred_cat,
            "thresholds": {
                "low": round(thresholds["low"], 2),
                "high": round(thresholds["high"], 2)
            }
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

@app.route('/api/features', methods=['GET'])
def get_features():
    """Return feature list and their ranges."""
    return jsonify({
        "features": feature_columns,
        "feature_ranges": {
            "Access to electricity (% of population)": {"min": 0, "max": 100},
            "Access to clean fuels for cooking": {"min": 0, "max": 100},
            "Renewable-electricity-generating-capacity-per-capita": {"min": 0, "max": 10},
            "Financial flows to developing countries (US $)": {"min": 0, "max": 10000000},
            "Renewable energy share in the total final energy consumption (%)": {"min": 0, "max": 100},
            "Electricity from fossil fuels (TWh)": {"min": 0, "max": 1000},
            "Electricity from nuclear (TWh)": {"min": 0, "max": 500},
            "Electricity from renewables (TWh)": {"min": 0, "max": 1000},
            "Low-carbon electricity (% electricity)": {"min": 0, "max": 100},
            "Primary energy consumption per capita (kWh/person)": {"min": 100, "max": 10000},
            "Energy intensity level of primary energy (MJ/$2017 PPP GDP)": {"min": 1, "max": 30},
            "Renewables (% equivalent primary energy)": {"min": 0, "max": 100},
            "gdp_growth": {"min": -10, "max": 15},
            "gdp_per_capita": {"min": 100, "max": 150000},
            "Density_(P/Km2)": {"min": 1, "max": 2000},
            "Land Area(Km2)": {"min": 100, "max": 10000000},
            "Latitude": {"min": -90, "max": 90},
            "Longitude": {"min": -180, "max": 180}
        }
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
