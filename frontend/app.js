// ===============================
// app.js – CLEAN & FULLY FIXED VERSION
// ===============================

const API_URL = "http://localhost:5000/api";
const Papa = window.Papa;

// Track active charts
const chartInstances = {};

// Make openTab available globally
window.openTab = openTab;

// =====================================================
// 1. FIXED PREDICTION HANDLER  (Only ONE handler exists)
// =====================================================

document.getElementById("predictionForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const fieldMapping = {
    "Access to electricity (% of population)": "Access to electricity (% of population)",
    "Access to clean fuels for cooking": "Access to clean fuels for cooking",
    "Renewable-electricity-generating-capacity-per-capita": "Renewable-electricity-generating-capacity-per-capita",
    "Financial flows to developing countries (US $)": "Financial flows to developing countries (US $)",
    "Renewable energy share in the total final energy consumption (%)": "Renewable energy share in the total final energy consumption (%)",
    "Electricity from fossil fuels (TWh)": "Electricity from fossil fuels (TWh)",
    "Electricity from nuclear (TWh)": "Electricity from nuclear (TWh)",
    "Electricity from renewables (TWh)": "Electricity from renewables (TWh)",
    "Low-carbon electricity (% electricity)": "Low-carbon electricity (% electricity)",
    "Primary energy consumption per capita (kWh/person)": "Primary energy consumption per capita (kWh/person)",
    "Energy intensity level of primary energy (MJ/$2017 PPP GDP)": "Energy intensity level of primary energy (MJ/$2017 PPP GDP)",
    "Renewables (% equivalent primary energy)": "Renewables (% equivalent primary energy)",
    gdp_growth: "gdp_growth",
    gdp_per_capita: "gdp_per_capita",
    "Density_(P/Km2)": "Density_(P/Km2)",
    "Land Area(Km2)": "Land Area(Km2)",
    Latitude: "Latitude",
    Longitude: "Longitude",
  };

  const input = {};
  let missing = [];

  Object.entries(fieldMapping).forEach(([fieldId, featureName]) => {
    const raw = document.getElementById(fieldId)?.value;
    if (raw === "" || raw === undefined) {
      missing.push(fieldId);
    }
    input[featureName] = Number.parseFloat(raw);
  });

  if (missing.length > 0) {
    alert("Please fill in all fields. Missing: " + missing.join(", "));
    return;
  }

  try {
    const response = await fetch(`${API_URL}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(input),
    });

    const result = await response.json();

    if (result.success) {
      displayResult(result);
    } else {
      alert("Error: " + result.error);
    }
  } catch (error) {
    alert("Connection error. Make sure backend is running at http://localhost:5000");
  }
});

// Display result
function displayResult(result) {
  document.getElementById("resultEmission").textContent = result.co2_emission.toFixed(2);

  const categoryDiv = document.getElementById("resultCategory");
  categoryDiv.className = "result-category " + result.category.toLowerCase();
  categoryDiv.textContent = `Category: ${result.category}`;

  const infoDiv = document.getElementById("resultInfo");
  infoDiv.innerHTML = `
    <strong>Thresholds:</strong><br>
    Low: ≤ ${result.thresholds.low} kt CO₂<br>
    Medium: ${result.thresholds.low} – ${result.thresholds.high} kt CO₂<br>
    High: > ${result.thresholds.high} kt CO₂
  `;

  document.getElementById("result").classList.remove("hidden");
}

// =====================================
// 2. TAB SWITCHING
// =====================================
function openTab(evt, tabName) {
  const contents = document.querySelectorAll(".tab-content");
  contents.forEach((content) => content.classList.remove("active"));

  const buttons = document.querySelectorAll(".tab-btn");
  buttons.forEach((btn) => btn.classList.remove("active"));

  document.getElementById(tabName).classList.add("active");
  evt.currentTarget.classList.add("active");

  if (tabName === "visualizations") initializeCharts();
}

// =====================================
// 3. CSV + CHART RENDERING
// =====================================
async function initializeCharts() {
  const csvPath = "data/ENERGY_DATA_CLEANED.csv";

  try {
    const response = await fetch(csvPath);
    if (!response.ok) throw new Error("Failed to load CSV file");

    const csvText = await response.text();
    const parsed = Papa.parse(csvText, { header: true, skipEmptyLines: true });
    const data = parsed.data;

    createEmissionsChart(data);
    createEnergySourcesChart(data);
    createGDPCorrelationChart(data);
    createRenewableTrendsChart(data);
  } catch (err) {
    console.error("Error loading charts:", err);
  }
}

function destroyIfExists(id) {
  if (chartInstances[id]) {
    chartInstances[id].destroy();
    delete chartInstances[id];
  }
}

// =====================================
// CHART 1 — Emissions Histogram
// =====================================
function createEmissionsChart(data) {
  const id = "emissionChart";
  destroyIfExists(id);

  const ctx = document.getElementById(id).getContext("2d");

  const emissions = data
    .map(r => Number(r["Co2_emission"]))
    .filter(v => !isNaN(v));

  const bins = [0, 50, 100, 500, 1000, 5000, 10000];

  const counts = bins.map((bin, i) =>
    emissions.filter(e => e >= bin && (i === bins.length - 1 || e < bins[i + 1])).length
  );

  chartInstances[id] = new Chart(ctx, {
    type: "bar",
    data: {
      labels: bins.map((b, i) => (i === bins.length - 1 ? `${b}+` : `${b}-${bins[i + 1]}`)),
      datasets: [{ label: "CO₂ Emissions (kt)", data: counts }],
    },
    options: {
      plugins: { tooltip: { enabled: true } },
      scales: {
        y: { title: { display: true, text: "# of Countries" } },
        x: { title: { display: true, text: "Emissions Range (kt)" } },
      }
    }
  });
}

// =====================================
// CHART 2 — Energy Sources
// =====================================
function createEnergySourcesChart(data) {
  const id = "energySourceChart";
  destroyIfExists(id);

  const ctx = document.getElementById(id).getContext("2d");

  const renewable = data.filter(r => Number(r["Electricity from renewables (TWh)"]) > 0).length;
  const fossil = data.filter(r => Number(r["Electricity from fossil fuels (TWh)"]) > 0).length;
  const nuclear = data.filter(r => Number(r["Electricity from nuclear (TWh)"]) > 0).length;

  chartInstances[id] = new Chart(ctx, {
    type: "pie",
    data: {
      labels: ["Renewables", "Fossil Fuels", "Nuclear"],
      datasets: [{ data: [renewable, fossil, nuclear] }],
    },
    options: { plugins: { tooltip: { enabled: true } } }
  });
}

// =====================================
// CHART 3 — GDP vs CO₂
// =====================================
function createGDPCorrelationChart(data) {
  const id = "gdpChart";
  destroyIfExists(id);

  const ctx = document.getElementById(id).getContext("2d");

  const points = data
    .filter(r => Number(r["gdp_per_capita"]) > 0 && Number(r["Co2_emission"]) > 0)
    .slice(0, 50)
    .map(r => ({ x: Number(r["gdp_per_capita"]), y: Number(r["Co2_emission"]) }));

  chartInstances[id] = new Chart(ctx, {
    type: "scatter",
    data: {
      datasets: [{ label: "GDP per Capita vs CO₂", data: points }],
    },
    options: {
      parsing: false,
      plugins: { tooltip: { enabled: true } },
      scales: {
        x: { title: { display: true, text: "GDP per Capita (USD)" } },
        y: { title: { display: true, text: "CO₂ Emissions (kt)" } },
      }
    }
  });
}

// =====================================
// CHART 4 — Renewable Share Trend
// =====================================
function createRenewableTrendsChart(data) {
  const id = "renewableShareChart";
  destroyIfExists(id);

  const ctx = document.getElementById(id).getContext("2d");

  const renewable = data
    .map(row => Number(row["Renewable energy share in the total final energy consumption (%)"]))
    .filter(v => !isNaN(v))
    .slice(0, 50);

  chartInstances[id] = new Chart(ctx, {
    type: "line",
    data: {
      labels: renewable.map((_, i) => `Point ${i + 1}`),
      datasets: [{ label: "Renewable Share (%)", data: renewable }]
    }
  });
}

