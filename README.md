# 🌍 SUSTAINALYZE - Carbon Emission Forecasting

SUSTAINALYZE is a web-based system that forecasts carbon emissions using machine learning. It aims to help policymakers, researchers, and sustainability enthusiasts analyze and predict CO₂ emissions based on energy and economic indicators, supporting climate action aligned with **UN Sustainable Development Goal 13**.

---

## 🧪 Project Overview

- **Model:** Gradient Boosting Regressor trained on global energy data
- **Features:** 18 energy and economic indicators including renewable energy share, electricity mix, GDP, population density, and more
- **Prediction Categories:** Low, Medium, High CO₂ emissions
- **Data Source:** Global Data on Sustainable Energy (Kaggle, 2023), World Bank, IEA, UN databases
- **Frontend:** HTML, CSS, JavaScript, Chart.js
- **Backend:** Python, Flask

---

## ⚡ Features

1. **Prediction Tool**
   - Input key energy and economic indicators
   - Get predicted CO₂ emissions (Mt)
   - See the category (Low / Medium / High) with thresholds

2. **Data Visualizations**
   - CO₂ Emissions Distribution
   - Renewable vs Fossil Fuel vs Nuclear energy share
   - GDP per Capita vs CO₂ Emissions scatter plot
   - Renewable Energy Share Trend

3. **About Section**
   - Project mission, technology, data sources, and model accuracy

---

## 🛠️ Setup Instructions

> Make sure you have **Python 3.10+** and **XAMPP** installed for local development.

1. **Open VS Code Terminal** in your project folder (`E:\XAMPP\htdocs\sustainalyze`) and upgrade pip:
```powershell
PS E:\XAMPP\htdocs\sustainalyze> python -m pip install --upgrade pip
````

2. **Install Python dependencies**:

```powershell
PS E:\XAMPP\htdocs\sustainalyze> pip install -r requirements.txt
```

3. **Train the model** (optional, if you want to retrain):

```powershell
PS E:\XAMPP\htdocs\sustainalyze> cd backend
PS E:\XAMPP\htdocs\sustainalyze\backend> python train_model.py
```

4. **Run the backend server**:

```powershell
PS E:\XAMPP\htdocs\sustainalyze> cd backend
PS E:\XAMPP\htdocs\sustainalyze\backend> python app.py
```

5. **Access the system in your browser**:

```
http://localhost/sustainalyze/frontend/
```

---

## 🗂️ Folder Structure

```
sustainalyze/
│
├─ backend/
│  ├─ app.py                  # Flask backend API
│  ├─ train_model.py          # Script to train the model
│  ├─ verify_model.py         # Script to test model performance
│  ├─ data/
│  │   └─ ENERGY_DATA_CLEANED.csv
│  └─ models/
│      ├─ gb_reg_model.pkl
│      ├─ scaler.pkl
│      └─ co2_thresholds.pkl
│
├─ frontend/
│  ├─ index.html              # Main frontend page
│  ├─ app.js                  # Frontend JavaScript
│  ├─ styles.css              # CSS styles
│  └─ data/
│      └─ ENERGY_DATA_CLEANED.csv
│
├─ requirements.txt           # Python dependencies
├─ package.json               # (Optional) frontend package info
└─ SETUP_GUIDE.txt / QUICK_START.TXT
```

---

## 📊 Visualization Features

* **CO₂ Emissions Distribution:** Bar chart showing emission ranges
* **Renewable vs Fossil Fuel vs Nuclear Energy:** Pie chart of energy mix
* **GDP vs CO₂ Emissions:** Scatter plot showing correlation between GDP per capita and CO₂ emissions
* **Renewable Energy Share Trend:** Line chart showing trends in renewable energy usage

All charts are interactive and display labels on hover for clarity.

---

## 💡 Notes

* Ensure the backend server is running before accessing the frontend.
* The system currently uses a local CSV dataset; any updates to the dataset require retraining the model for accurate predictions.

---

## 👨‍💻 Contributors

* **Leonardo Antero Yoro** - Project Lead / Model Creator
* **Alberto Catapang** - MiniLM Model Creator / Data Collector
* **Naithan Balondo** - Frontend Developer / Visualization Integrator

---

## 📄 Data

Data sourced from Kaggle, World Bank, IEA, and UN databases.

---

## 🔗 Access

* Frontend: `http://localhost/sustainalyze/frontend/`
* Backend API: `http://localhost:5000/api/predict`

