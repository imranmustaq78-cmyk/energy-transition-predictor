# 🌱 U.S. Energy Transition Dashboard

A Python data-visualisation tool that tracks U.S. energy production trends across **Coal, Natural Gas, Solar, and Wind** — and generates a **6-month AI-powered forecast** using linear regression.

Built for policy researchers and data analysts at the [Sustainable Development Policy Institute (SDPI)](https://sdpi.org).

---

## 📊 Output Preview

> A 2 × 2 dashboard exported as a high-resolution PNG (300 dpi), ready for reports and presentations.

| Chart | Description |
|---|---|
| **Coal Production** | Monthly output in Thousand Short Tons |
| **Natural Gas** | Monthly consumption in Trillion Btu |
| **Solar Energy** | Monthly generation in Trillion Btu |
| **Wind Energy** | Monthly generation in Trillion Btu |

Solid bars = historical actuals · Hatched bars = AI forecast · Shaded region = forecast window

---

## 🗂 Project Structure

```
us-energy-transition-dashboard/
│
├── us_energy_transition_dashboard.py   ← main script (this file)
├── requirements.txt                    ← Python dependencies
├── README.md                           ← you are here
│
├── data/
│   └── eia_export.csv                  ← place your EIA data export here
│
└── output/
    └── us_energy_transition_dashboard.png   ← generated chart saved here
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/us-energy-transition-dashboard.git
cd us-energy-transition-dashboard
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

##  Usage

### Option A — Command line

```bash
python us_energy_transition_dashboard.py --input data/eia_export.csv
```

Save to a custom output folder:

```bash
python us_energy_transition_dashboard.py --input data/eia_export.csv --output results/
```

### Option B — Jupyter Notebook / interactive Python

```python
import pandas as pd
from us_energy_transition_dashboard import build_dashboard

raw_data = pd.read_csv("data/eia_export.csv")
build_dashboard(raw_data)
```

---

## 📋 Data Format

The input CSV (or DataFrame) must contain **at least** these three columns:

| Column | Type | Example |

| `seriesDescription` | string | `"Coal Production"` |
| `period` | ISO date string | `"2025-10-01"` |
| `value` | numeric | `44760` |

Data can be exported directly from the **[U.S. EIA Open Data API](https://www.eia.gov/opendata/)**.

---

##  How the Forecast Works

1. All available historical data for a source is collected.
2. A **linear regression** model is fitted on a numeric time-step index.
3. The model extrapolates **6 months** beyond the last recorded data point.
4. Forecast bars are rendered with a hatched pattern and a shaded background region to clearly distinguish them from actuals.

> **Note:** Linear regression captures long-run trends but does not model seasonality. For production-grade forecasting consider SARIMA or Prophet.

---

## Known Issues Fixed in This Version

 Bug , Root Cause ,Fix Applied 
| Multiple values stacked in one bar | Duplicate rows per period in raw data | `groupby('Date').sum()` before plotting |
| Bar labels overlapping / invisible | Labels placed at exact bar height | Labels nudged 1.5 % above bar top |
| Labels clipped at chart top | Y-axis too short | Y-limit extended to 112 % of max value |
| Bars overlapping each other | String x-labels allow matplotlib duplicates | Integer positions + `set_xticks()` |

---

## 📦 Dependencies

```
pandas
numpy
matplotlib
scikit-learn
```

See `requirements.txt` for pinned versions.

---

## 📄 License

MIT License — feel free to use, modify, and share with attribution.

---

## 🤝 Contributing

Pull requests are welcome! If you have ideas for adding more energy sources, improving the forecast model, or adding interactivity (Plotly / Dash), please open an issue first to discuss.

---

*Made with 🐍 Python · 📊 Matplotlib · 🤖 scikit-learn*
