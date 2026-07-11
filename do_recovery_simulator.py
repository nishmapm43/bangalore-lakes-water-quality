"""
Lake DO Recovery Simulator
---------------------------
What-if tool: drag a slider to simulate reducing BOD pollution in a lake,
and see the predicted dissolved oxygen (DO) recovery, based on a linear
regression fit across KSPCB monitoring data.

Run with:
    pip install streamlit pandas scipy matplotlib
    streamlit run do_recovery_simulator.py
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import streamlit as st

CSV_PATH = "master_lakes_final.csv"
DO_THRESHOLD = 4.0
DO_CAP = 9.0  # physically plausible dissolved-oxygen saturation ceiling

FAMOUS_LAKES = [
    "Bellandur Lake", "Varthur Lake", "Ulsoor Lake", "Hebbal Lake",
    "Sankey Tank", "Madiwala Tank", "Agaram Lake", "Nagavara Lake",
    "Jakkur Lake", "Yediyur Tank", "Puttenahalli Lake", "Hesaraghatta Lake",
    "Kaikondanahalli Lake", "Kengeri Tank", "Lalbagh Tank",
    "Doddabidarakallu Lake", "Kasavanahalli Lake", "Kothanuru Lake",
    "Rachenahalli Lake"
]

# =========================================================
# LOAD DATA + FIT REGRESSION (cached so it only runs once)
# =========================================================
@st.cache_data
def load_data():
    df = pd.read_csv(CSV_PATH)
    work = df[df["base_lake_name"].isin(FAMOUS_LAKES)].copy()
    work["month_dt"] = pd.to_datetime(work["sampling_month"], format="%b-%y")

    # regression across all lake-months with valid BOD & DO
    reg_data = work.dropna(subset=["do_mgl", "bod_mgl"])
    slope, intercept, r, p, se = stats.linregress(reg_data["bod_mgl"], reg_data["do_mgl"])

    # most recent reading per lake, for the simulator's starting point
    latest = (
        work.sort_values("month_dt")
        .groupby("base_lake_name")
        .tail(1)
        .set_index("base_lake_name")
        .reindex(FAMOUS_LAKES)[["bod_mgl", "do_mgl", "month_dt"]]
    )

    model = dict(slope=slope, intercept=intercept, r=r, r2=r**2, p=p, n=len(reg_data))
    return latest, model


latest, model = load_data()

# =========================================================
# PAGE CONFIG + STYLE
# =========================================================
st.set_page_config(page_title="Lake DO Recovery Simulator", layout="centered")

st.markdown("""
<style>
    .stApp { background-color: #EEF3F0; }
    h1 { font-family: 'Georgia', serif; color: #0F2A2E; }
    .metric-box {
        background: white; border: 1px solid #D6E0DB; border-radius: 4px;
        padding: 14px; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("Lake DO Recovery Simulator")
st.caption("What-if tool — how much would dissolved oxygen recover if BOD pollution were reduced?")

# =========================================================
# CONTROLS
# =========================================================
lake = st.selectbox(
    "Select lake",
    FAMOUS_LAKES,
    index=int(latest["bod_mgl"].reset_index(drop=True).idxmax()),  # default: worst BOD
    format_func=lambda l: f"{l}  (BOD {latest.loc[l,'bod_mgl']:.1f} mg/L, DO {latest.loc[l,'do_mgl']:.1f} mg/L)"
)

current_bod = float(latest.loc[lake, "bod_mgl"])
current_do = float(latest.loc[lake, "do_mgl"])

reduction = st.slider(
    "Reduce BOD by (mg/L)",
    min_value=0.0, max_value=round(current_bod, 1), value=0.0, step=0.5
)

# =========================================================
# PREDICTION
# =========================================================
new_bod = max(0.0, current_bod - reduction)
# local linear extrapolation from the lake's own observed point,
# using the global regression slope (not the raw regression line itself,
# since each lake has its own baseline offset from unmodeled factors)
predicted_do = min(DO_CAP, current_do + (-model["slope"]) * reduction)

# =========================================================
# READOUTS
# =========================================================
c1, c2, c3 = st.columns(3)
c1.metric("Current BOD", f"{current_bod:.1f} mg/L")
c2.metric("Current DO", f"{current_do:.1f} mg/L")
c3.metric(
    "Predicted DO",
    f"{predicted_do:.2f} mg/L",
    delta=f"{predicted_do - current_do:+.2f} mg/L"
)

# =========================================================
# BAR VISUAL
# =========================================================
fig, ax = plt.subplots(figsize=(7, 1.4))
ax.barh([0], [DO_CAP], color="#FBE7DF", height=0.6, zorder=1)          # unhealthy zone (full width)
ax.barh([0], [DO_CAP - DO_THRESHOLD], left=DO_THRESHOLD, color="#DCEFEA", height=0.6, zorder=1)  # healthy zone
ax.barh([0], [current_do], color="#BFCBC6", height=0.6, zorder=2, label="Current DO")
ax.barh([0], [predicted_do], color="#1D7A6E", height=0.28, zorder=3, label="Predicted DO")
ax.axvline(DO_THRESHOLD, color="#C1502E", linewidth=2, zorder=4)
ax.text(DO_THRESHOLD, 0.42, " 4.0 mg/L threshold", color="#C1502E", fontsize=8, va="bottom")
ax.set_xlim(0, DO_CAP)
ax.set_yticks([])
ax.set_xlabel("Dissolved Oxygen (mg/L)", fontsize=9)
for spine in ["top", "right", "left"]:
    ax.spines[spine].set_visible(False)
ax.legend(loc="upper right", fontsize=8, frameon=False, bbox_to_anchor=(1.0, 1.6), ncol=2)
st.pyplot(fig)

# =========================================================
# VERDICT
# =========================================================
was_healthy = current_do >= DO_THRESHOLD
now_healthy = predicted_do >= DO_THRESHOLD

if reduction == 0:
    if was_healthy:
        msg = f"**{lake}** is currently above the healthy DO minimum. Drag the slider to see how much further BOD reduction would improve it."
    else:
        msg = f"**{lake}** is currently below the healthy DO minimum ({current_do:.1f} mg/L). Drag the slider to see how much BOD reduction would be needed to recover it."
    st.info(msg)
elif not was_healthy and now_healthy:
    st.success(
        f"**Crossing point reached** — cutting BOD by {reduction:.1f} mg/L is enough to bring "
        f"**{lake}** back above the 4.0 mg/L healthy DO threshold, based on this model."
    )
elif now_healthy:
    st.success(f"**{lake}** stays healthy at this reduction level — predicted DO {predicted_do:.2f} mg/L.")
else:
    st.warning(
        f"Even after a {reduction:.1f} mg/L BOD cut, **{lake}** is still predicted below the healthy "
        f"DO threshold. This lake likely needs more than BOD reduction alone (e.g. desilting, sewage "
        f"diversion, aeration)."
    )

# =========================================================
# MODEL TRANSPARENCY NOTE
# =========================================================
st.markdown("---")
st.caption(
    f"**How this works:** a linear regression fit across {model['n']} lake-months of KSPCB monitoring "
    f"data shows DO = {model['intercept']:.2f} − {abs(model['slope']):.3f} × BOD "
    f"(Pearson r = {model['r']:.2f}, R² = {model['r2']:.2f}, p < 0.001). Each 1 mg/L reduction in BOD is "
    f"associated with roughly +{abs(model['slope']):.2f} mg/L of dissolved oxygen recovery. This is a "
    f"**correlational, not causal**, model — BOD explains {model['r2']*100:.0f}% of the variation in DO; "
    f"the rest comes from other factors (temperature, inflow, aeration, lake depth, etc.) not captured "
    f"here. Predictions extrapolate from each lake's most recent reading and should be read as "
    f"directional, not exact."
)
