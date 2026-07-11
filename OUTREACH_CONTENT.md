# Outreach Content — Bangalore Lakes Water Quality Project

Fill in the bracketed placeholders before using ([GitHub link], [Streamlit link], [your name], etc.)

---

## LinkedIn Post

I spent the last few weeks turning a stack of government PDF reports into a working water-quality analytics project — and learned more about real-world messy data than I expected.

🌊 **What I built:** an end-to-end analysis of 13 months of Bangalore lake water quality data (Nov 2024–Nov 2025), covering 19 well-known lakes including Bellandur, Varthur, Ulsoor, and Jakkur.

**The process:**
📄 Extracted tabular data from 13 monthly KSPCB PDF reports using pdfplumber
🧹 Found and fixed a systematic text-extraction bug that had silently fragmented lake names (e.g. "Karihoba-Halli" vs. the correct "Karihobanahalli") — this alone changed the lake count from 174 down to ~140 real, distinct lakes
📊 Built a racing bar chart animating monthly BOD (Biochemical Oxygen Demand) rankings to spot chronic pollution hotspots vs. one-off spikes
📈 Charted Dissolved Oxygen trends against the minimum healthy threshold (4.0 mg/L) — 7 of 19 major lakes were chronically below it
🗺️ Built an interactive map of all monitored lakes
🧪 Built a Streamlit "what-if" simulator predicting DO recovery from BOD reduction

**One finding that surprised me:** Jakkur Lake, often cited as a lake-restoration success story, was below the healthy oxygen threshold in 7 of the 13 months — a reminder that public reputation and current data don't always agree.

Full write-up, code, and the live simulator are linked below 👇
🔗 GitHub: [GitHub link]
🔗 Live demo: [Streamlit link]

Would love feedback from anyone working in environmental data, GIS, or public-sector analytics.

#DataAnalytics #Python #DataVisualization #EnvironmentalData #OpenData #Streamlit #Bangalore #WaterQuality

---

## Resume Bullets

**Option A — Data Analyst / Data Science focused:**
- Built an end-to-end water quality analytics pipeline processing 1,720 records from 13 monthly government PDF reports (KSPCB) using Python (pandas, pdfplumber), identifying and correcting a systematic data-extraction bug that had fragmented ~20% of lake name entries
- Designed and built 4 data visualizations (animated racing bar chart, trend analysis, interactive map, Streamlit simulator) to communicate pollution trends across 19 Bangalore lakes to non-technical audiences
- Identified 7 chronically oxygen-deficient lakes through threshold-based trend analysis, surfacing findings that contradicted public assumptions about lake restoration success

**Option B — shorter, single-bullet version:**
- Built a Python data pipeline and interactive dashboard (pandas, Streamlit, Folium) analyzing 13 months of Bangalore lake water quality data from government PDF reports, uncovering and fixing a systematic data-quality issue and identifying 7 chronically polluted lakes

---

## Recruiter / Cold Outreach Message

Hi [Recruiter Name],

I wanted to share a recent project that reflects the kind of data work I enjoy — turning messy, real-world government data into something usable and insightful.

I built an end-to-end analysis of Bangalore's lake water quality using 13 months of official monitoring PDFs: extracted and cleaned the raw data (catching and fixing a data-extraction bug along the way), then built a racing bar chart, trend analysis, an interactive map, and a small Streamlit "what-if" simulator to explore pollution recovery scenarios.

- Code + write-up: [GitHub link]
- Live interactive demo: [Streamlit link]

Happy to walk through the approach or the trickier parts (like the PDF extraction and data cleaning) in more detail if useful. Let me know if this is relevant to any roles you're working on.

Best,
[Your Name]
[LinkedIn] · [Email/Phone]

---

## Short version (for a DM or quick intro)

Hi [Name] — sharing a project I built analyzing Bangalore lake water quality from 13 months of government PDF reports (Python, pandas, Streamlit, Folium). Includes a live interactive simulator: [Streamlit link]. Code here: [GitHub link]. Open to feedback or relevant opportunities!
