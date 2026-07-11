# Bangalore Lakes Water Quality Analysis
**Tracking pollution hotspots across 19 major Bangalore lakes using 13 months of official government monitoring data (Nov 2024 – Nov 2025).**

[![Live Demo](https://img.shields.io/badge/Live%20Demo-Streamlit-FF4B4B?logo=streamlit)](YOUR_STREAMLIT_LINK_HERE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)](https://www.python.org/)

![BOD Racing Bar Chart](outputs/bod_race_final.gif)

**7 of 19 major lakes are chronically polluted — including Jakkur Lake, widely cited as a restoration success story.**

---

## Why This Project

Bengaluru's lakes are under constant pollution pressure, but the data that could actually help track and fix this — monthly water-quality reports from the Karnataka State Pollution Control Board (KSPCB) — is published as scanned PDF documents, not usable datasets. Anyone wanting to understand lake health over time first has to manually read through dozens of PDF reports.

I built a pipeline that turns 13 months of these government PDFs into a single, clean dataset, then used it to answer a simple question: **which Bangalore lakes are chronically polluted, which are improving, and which had one-off pollution events worth investigating?**

## What I Did

1. **Extracted** water-quality data from 13 monthly KSPCB PDF reports (Nov 2024 – Nov 2025) using `pdfplumber`, pulling out station-level readings for BOD, Dissolved Oxygen, pH, temperature, and more.
2. **Combined** all 13 months into a single dataset — 1,720 station-month records across 273 monitoring stations.
3. **Found and fixed a hidden data-quality bug**: the PDF-to-text extraction had silently corrupted lake names (e.g. splitting "Karihobanahalli" into "Karihoba" + "-Halli"), fragmenting single lakes into multiple fake entries. Using fuzzy string matching, I merged these duplicates — reducing 174 raw name variants down to ~140 genuinely distinct lakes.
4. **Built four ways to explore lake health:**
   - A **racing bar chart** ranking 19 well-known lakes by pollution (BOD) every month, to separate chronic hotspots from one-off spikes
   - **DO trend charts** comparing each lake's oxygen levels against the healthy minimum (4.0 mg/L)
   - An **interactive map** plotting every monitored lake with its water quality status
   - A **"what-if" simulator** (Streamlit) that predicts how much a lake's oxygen would recover if pollution (BOD) were reduced by a chosen amount

## Live Demo
🔗 **[Try the DO Recovery Simulator](YOUR_STREAMLIT_LINK_HERE)**

## Key Findings

- **7 of 19 major lakes are chronically oxygen-deficient** — Dissolved Oxygen fell below the healthy minimum in 3 or more of the 13 months studied. **Jakkur Lake was the worst offender**, sitting below threshold in 7 of 13 months — despite its public reputation as a lake-restoration success story.
- **Lalbagh Tank recorded an isolated BOD spike of 56 mg/L in August 2025** — more than double the next-highest lake that month. Because the pipeline retains a `source_file` audit trail back to the original PDF, this reading can be traced and verified rather than dismissed as noise.
- A racing bar chart specifically surfaces something a static table can't: **which lakes stay polluted month after month (chronic, structural problems) versus which lakes spike once and recover (isolated events)** — these need very different kinds of intervention.

## Visuals

### BOD Racing Bar Chart
Watch which lakes stay at the top of the pollution ranking month after month (shown at the top of this README).

### Dissolved Oxygen Trajectories
Each panel shows one chronically low-oxygen lake against the 4.0 mg/L health threshold.

![DO Trend Small Multiples](outputs/do_small_multiples.png)

### Interactive Lake Map
An interactive Folium map plotting all monitored lakes by location and water-quality status — [view the map](outputs/final_dashboard_map.html).

### DO Recovery Simulator
A Streamlit what-if tool: select a lake, simulate a BOD reduction, and see the predicted DO recovery against the health threshold.

## Data Pipeline

| Stage | Tool |
|---|---|
| Source | KSPCB monthly water quality reports (PDF), Nov 2024 – Nov 2025 |
| Extraction | `pdfplumber` — table extraction from 13 monthly PDF reports |
| Cleaning | `pandas` + `difflib` fuzzy matching to fix fragmented lake names |
| Analysis | `pandas`, `numpy` |
| Static visuals | `matplotlib` (racing bar chart animation, DO trend charts) |
| Interactive map | `folium` |
| Interactive app | `streamlit` |

Final dataset: **1,720 station-month records** across **273 monitoring stations**, mapped to **~140 distinct lakes**, with a curated subset of **19 well-known Bangalore lakes** used for the visualizations above (selected for public recognizability and sufficient monthly data coverage — at least 9 of 13 months per lake).

## What Could Come Next

- Extend the pipeline to automatically ingest new KSPCB monthly reports as they're published, rather than a fixed 13-month window
- Add a Water Quality Index (WQI) score combining BOD, DO, pH, and temperature into a single "Good / Neutral / Critical" status per lake, for faster at-a-glance reading
- Investigate the Lalbagh Tank August 2025 spike further using rainfall data, to test whether it correlates with runoff events

## Repository Structure

```
bangalore-lakes-water-quality/
├── README.md
├── requirements.txt
├── data/
│   └── master_lakes_final.csv          # cleaned, combined dataset
├── scripts/
│   ├── racing_bar_chart.py             # builds the BOD racing bar chart
│   └── do_trend_analysis.py            # builds the DO small-multiples chart
├── app/
│   └── do_simulator.py                 # Streamlit DO Recovery Simulator
└── outputs/
    ├── bod_race_final.gif
    ├── do_small_multiples.png
    └── final_dashboard_map.html
```

## Running Locally

```bash
git clone https://github.com/nishmapm43/bangalore-lakes-water-quality.git
cd bangalore-lakes-water-quality
pip install -r requirements.txt

# Regenerate the static charts
python scripts/racing_bar_chart.py
python scripts/do_trend_analysis.py

# Launch the interactive simulator
streamlit run app/do_simulator.py
```

## Data Source & Limitations

Data is sourced from KSPCB's publicly released monthly lake water quality monitoring reports. As with any government-published monitoring data, coverage is uneven month to month (not every lake is sampled every month — missing months were linearly interpolated for animation purposes only, and are clearly distinguishable from directly measured values in the underlying dataset). This project is intended as a data analysis and visualization exercise, not as an authoritative regulatory source — always refer to KSPCB's original publications for official figures.

## Author

**Nishma P M**
[LinkedIn](https://www.linkedin.com/in/nishmapm) · [GitHub](https://github.com/nishmapm43)
