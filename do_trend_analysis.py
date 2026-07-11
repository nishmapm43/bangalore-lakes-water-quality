"""
Dissolved Oxygen (DO) Trend Analysis
Bangalore Lakes Water Quality Analysis

Identifies lakes chronically below the healthy DO threshold (4.0 mg/L) and
plots each one as a small-multiples panel for clear, non-overlapping comparison.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

CSV_PATH = "../data/master_lakes_final.csv"
OUTPUT_PNG = "../outputs/do_small_multiples.png"

FAMOUS_LAKES = [
    "Bellandur Lake", "Varthur Lake", "Ulsoor Lake", "Hebbal Lake",
    "Sankey Tank", "Madiwala Tank", "Agaram Lake", "Nagavara Lake",
    "Jakkur Lake", "Yediyur Tank", "Puttenahalli Lake", "Hesaraghatta Lake",
    "Kaikondanahalli Lake", "Kengeri Tank", "Lalbagh Tank",
    "Doddabidarakallu Lake", "Kasavanahalli Lake", "Kothanuru Lake",
    "Rachenahalli Lake"
]

DO_THRESHOLD = 4.0
CHRONIC_MONTHS = 3


def load_and_pivot(csv_path):
    df = pd.read_csv(csv_path)
    work = df[df["base_lake_name"].isin(FAMOUS_LAKES)].dropna(subset=["do_mgl"]).copy()
    work["month_dt"] = pd.to_datetime(work["sampling_month"], format="%b-%y")
    agg = work.groupby(["base_lake_name", "month_dt"], as_index=False)["do_mgl"].mean()
    pivot = agg.pivot(index="month_dt", columns="base_lake_name", values="do_mgl").sort_index()
    pivot.index = pivot.index.strftime("%b-%Y")
    return pivot


def plot_small_multiples(pivot):
    below_count = (pivot < DO_THRESHOLD).sum()
    chronic_lakes = below_count[below_count >= CHRONIC_MONTHS].sort_values(ascending=False).index.tolist()
    print(f"Chronic lakes (>= {CHRONIC_MONTHS} months below {DO_THRESHOLD} mg/L):", chronic_lakes)

    n = len(chronic_lakes)
    ncols = 4
    nrows = int(np.ceil(n / ncols))

    fig, axes = plt.subplots(nrows, ncols, figsize=(16, 3.2 * nrows), sharey=True, sharex=True)
    axes = axes.flatten()

    for i, lake in enumerate(chronic_lakes):
        ax = axes[i]
        series = pivot[lake]
        below_mask = series < DO_THRESHOLD

        ax.plot(pivot.index, series, color="#2b6cb0", linewidth=2, zorder=3)
        ax.scatter(np.array(pivot.index)[below_mask], series[below_mask], color="#e53e3e", s=35, zorder=4)
        ax.scatter(np.array(pivot.index)[~below_mask], series[~below_mask], color="#2b6cb0", s=25, zorder=4)

        ax.axhline(DO_THRESHOLD, color="#e53e3e", linestyle="--", linewidth=1.2, alpha=0.7, zorder=2)
        ax.fill_between(pivot.index, 0, DO_THRESHOLD, color="#e53e3e", alpha=0.06, zorder=1)

        ax.set_title(f"{lake}\n({below_count[lake]} mo. below threshold)", fontsize=10, fontweight="bold")
        ax.tick_params(axis="x", rotation=60, labelsize=7)
        ax.tick_params(axis="y", labelsize=8)
        ax.grid(alpha=0.2)
        ax.set_ylim(0, pivot.max().max() * 1.05)

    for j in range(n, len(axes)):
        axes[j].axis("off")

    fig.suptitle(
        "Dissolved Oxygen (DO) Trajectories — Chronic Intervention Candidates\n"
        f"(Red dashed line = minimum healthy DO of {DO_THRESHOLD} mg/L)",
        fontsize=14, fontweight="bold", y=1.02,
    )
    fig.text(0.5, -0.02, "Sampling Month", ha="center", fontsize=11)
    fig.text(-0.01, 0.5, "Dissolved Oxygen (mg/L)", va="center", rotation="vertical", fontsize=11)

    plt.tight_layout()
    plt.savefig(OUTPUT_PNG, dpi=140, bbox_inches="tight")
    print(f"Saved {OUTPUT_PNG}")


if __name__ == "__main__":
    pivot = load_and_pivot(CSV_PATH)
    plot_small_multiples(pivot)
