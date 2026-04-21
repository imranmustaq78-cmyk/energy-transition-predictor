# Energy Transition Predictor

A Python tool that fetches live U.S. energy data from the EIA Open Data API
and generates a 2x2 dashboard with a 6-month AI forecast for Coal, Natural Gas,
Solar, and Wind energy sources.

No CSV files. No manual downloads. Just run the script and the data comes to you.

Built for policy researchers and data analysts at the Sustainable Development Policy Institute (SDPI).

---

## Output

A 2x2 chart exported as a high-resolution PNG (300 dpi), ready for reports and presentations.

| Chart | Unit |
|---|---|
| Coal Production | Thousand Short Tons |
| Natural Gas | Billion Cubic Feet |
| Solar Energy | Thousand MWh |
| Wind Energy | Thousand MWh |

Solid bars = historical actuals. Hatched bars = AI forecast. Shaded region = forecast window.

---

## Step 0 - Get a Free EIA API Key

1. Go to https://www.eia.gov/opendata/register.php
2. Enter your name and email address
3. Your API key is emailed to you instantly

---

## Project Structure

```
energy-transition-predictor/
|
|-- energy_transition_predictor.py   <- main script
|-- requirements.txt                 <- Python dependencies
|-- README.md                        <- you are here
|
|-- output/
    |-- energy_transition_predictor.png  <- chart saved here after running
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/energy-transition-predictor.git
cd energy-transition-predictor
```

### 2. Create a virtual environment

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

## Set Your API Key

Option A - Environment variable (recommended for public GitHub repos):

```bash
# Windows
set EIA_API_KEY=your_key_here

# macOS / Linux
export EIA_API_KEY=your_key_here
```

Option B - Hard-code it for quick local testing. Open the script and change:

```python
API_KEY = os.environ.get("EIA_API_KEY", "PASTE_YOUR_KEY_HERE")
```

to:

```python
API_KEY = "your_key_here"
```

Never commit a real API key to a public GitHub repo. Always use the environment variable for shared code.

---

## Usage

### Run from the terminal

```bash
python energy_transition_predictor.py
```

### Use from a Jupyter Notebook

```python
from energy_transition_predictor import fetch_all, build_predictor

raw_data = fetch_all()
build_predictor(raw_data)
```

---

## How It Works

```
EIA Open Data API
      |
      v
fetch_all()        <- pulls live monthly data for all 4 sources
      |
      v
clean()            <- deduplicates revised estimates, sorts oldest to newest
      |
      v
forecast()         <- fits LinearRegression on time-step index, projects 6 months ahead
      |
      v
draw_chart()       <- plots historical and forecast bars with labels
      |
      v
build_predictor()  <- assembles 2x2 figure, saves 300-dpi PNG
```

---

## Dependencies

| Package | Purpose |
|---|---|
| requests | Live HTTP calls to the EIA API |
| pandas | Data wrangling and date handling |
| numpy | Numeric arrays for regression |
| matplotlib | Chart rendering |
| scikit-learn | Linear regression forecast model |

```bash
pip install -r requirements.txt
```

---

## Contributing

Pull requests are welcome. If you want to add more energy sources, improve the
forecast model, or add interactivity, please open an issue first to discuss.

---

## License

MIT License - free to use, modify, and share with attribution.
