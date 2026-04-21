# Energy Transition Predictor
# Fetches live data from EIA API and plots a 6-month forecast
# Get a free API key at: https://www.eia.gov/opendata/register.php

import os
import time
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from sklearn.linear_model import LinearRegression


# --- Configuration ---

API_KEY = os.environ.get("EIA_API_KEY", "PASTE_YOUR_KEY_HERE")

HISTORY_WINDOW  = 8
FORECAST_MONTHS = 6
BASE_URL        = "https://api.eia.gov/v2/seriesid/{sid}"

SOURCES = {
    "Coal Production": {
        "sid":   "COAL.PRODUCTION.TOT-US-TOT.M",
        "color": "#34495e",
        "unit":  "Thousand Short Tons",
    },
    "Natural Gas": {
        "sid":   "NG.N9070US2.M",
        "color": "#d35400",
        "unit":  "Billion Cubic Feet",
    },
    "Solar Energy": {
        "sid":   "ELEC.GEN.SUN-US-99.M",
        "color": "#f1c40f",
        "unit":  "Thousand MWh",
    },
    "Wind Energy": {
        "sid":   "ELEC.GEN.WND-US-99.M",
        "color": "#2980b9",
        "unit":  "Thousand MWh",
    },
}


# --- Data Fetching ---

def fetch_series(name, sid, months=60):
    params = {
        "api_key":            API_KEY,
        "data[]":             "value",
        "sort[0][column]":    "period",
        "sort[0][direction]": "desc",
        "length":             months,
    }

    for attempt in range(3):
        try:
            r = requests.get(BASE_URL.format(sid=sid), params=params, timeout=20)
            r.raise_for_status()
            rows = r.json().get("response", {}).get("data", [])
            if not rows:
                print(f"No data returned for {name}")
                return pd.DataFrame()

            df = pd.DataFrame(rows)
            df.columns = [c.lower() for c in df.columns]
            if "date" in df.columns:
                df = df.rename(columns={"date": "period"})

            df = df[["period", "value"]].copy()
            df["source"] = name
            df["value"]  = pd.to_numeric(df["value"],  errors="coerce")
            df["period"] = pd.to_datetime(df["period"], errors="coerce")
            df = df.dropna().sort_values("period").reset_index(drop=True)
            print(f"Fetched {name}: {len(df)} months")
            return df

        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {name}: {e}")
            time.sleep(2 ** attempt)

    return pd.DataFrame()


def fetch_all():
    frames = []
    for name, cfg in SOURCES.items():
        df = fetch_series(name, cfg["sid"])
        if not df.empty:
            frames.append(df)
    if not frames:
        raise RuntimeError("No data fetched. Check your API key and connection.")
    return pd.concat(frames, ignore_index=True)


# --- Data Cleaning ---

def clean(df, name):
    subset = df[df["source"].str.contains(name, case=False)].copy()
    if subset.empty:
        return subset
    subset = (
        subset.groupby("period", as_index=False)["value"]
        .sum()
        .sort_values("period")
        .reset_index(drop=True)
    )
    subset["step"] = range(len(subset))
    return subset


# --- Forecasting ---

def forecast(series):
    model = LinearRegression().fit(series[["step"]], series["value"])
    last  = int(series["step"].max())
    steps = np.arange(last + 1, last + FORECAST_MONTHS + 1).reshape(-1, 1)
    preds = model.predict(steps)
    dates = pd.date_range(series["period"].max(), periods=FORECAST_MONTHS + 1, freq="ME")[1:]
    labels = dates.strftime("%b %y").tolist()
    return preds, labels


# --- Plotting ---

def add_labels(ax, bars, values, n):
    fs = 8 if n > 12 else 9
    for bar, val in zip(bars, values):
        h = bar.get_height()
        if h == 0:
            continue
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            h * 1.015,
            f"{val:,.0f}",
            ha="center", va="bottom",
            fontsize=fs, fontweight="bold"
        )


def draw_chart(ax, name, recent, preds, h_labels, f_labels, color, unit):
    xh = np.arange(len(h_labels))
    xf = np.arange(len(h_labels), len(h_labels) + len(f_labels))
    n  = len(xh) + len(xf)

    bh = ax.bar(xh, recent["value"], color=color, alpha=0.9,  width=0.7, label="Historical")
    bf = ax.bar(xf, preds,           color=color, alpha=0.55, width=0.7, hatch="///", label="AI Forecast")

    add_labels(ax, bh, recent["value"].tolist(), n)
    add_labels(ax, bf, preds.tolist(),            n)

    if len(xf):
        ax.axvspan(xf[0] - 0.5, xf[-1] + 0.5, color="grey", alpha=0.07, zorder=0)

    ax.set_xticks(np.concatenate([xh, xf]))
    ax.set_xticklabels(h_labels + f_labels, rotation=45, ha="right", fontsize=9)
    ax.yaxis.set_major_formatter(ticker.StrMethodFormatter("{x:,.0f}"))
    ax.set_ylim(0, ax.get_ylim()[1] * 1.12)
    ax.set_title(name,                     fontsize=14, fontweight="bold", pad=8)
    ax.set_ylabel(unit,                    fontsize=10, fontweight="bold")
    ax.set_xlabel("Timeline (Month-Year)", fontsize=10, fontweight="bold")
    ax.legend(fontsize=9)


# --- Build Predictor ---

def build_predictor(raw_df, output_dir="output"):
    plt.style.use("fivethirtyeight")
    fig, axes = plt.subplots(2, 2, figsize=(20, 14))
    plt.subplots_adjust(hspace=0.55, wspace=0.35)
    axes = axes.flatten()

    for i, (name, cfg) in enumerate(SOURCES.items()):
        ax     = axes[i]
        series = clean(raw_df, name)

        if series.empty:
            ax.set_title(f"{name} - No Data", fontsize=13)
            continue

        recent   = series.tail(HISTORY_WINDOW).reset_index(drop=True)
        h_labels = recent["period"].dt.strftime("%b %y").tolist()
        preds, f_labels = forecast(series)

        all_labels = h_labels + f_labels
        if len(all_labels) != len(set(all_labels)):
            f_labels = [l + "*" for l in f_labels]

        draw_chart(ax, name, recent, preds, h_labels, f_labels, cfg["color"], cfg["unit"])
        print(f"Plotted {name}")

    fig.suptitle(
        "U.S. Energy Transition Predictor - 6-Month Forecast Outlook",
        fontsize=20, fontweight="bold", y=1.01
    )

    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "energy_transition_predictor.png")
    plt.savefig(path, bbox_inches="tight", dpi=300, facecolor="white")
    print(f"Saved: {path}")
    plt.show()


# --- Run ---

if __name__ == "__main__":
    raw_data = fetch_all()
    build_predictor(raw_data)
