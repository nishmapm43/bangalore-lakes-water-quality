"""
Racing Bar Chart: BOD Levels Over Time
Bangalore Lakes Water Quality Analysis

Animates monthly BOD (Biochemical Oxygen Demand) rankings across 19 well-known
Bangalore lakes, Nov 2024 - Nov 2025, to reveal chronic pollution hotspots.
"""

import os
import shutil
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image as PILImage

# =========================================================
# CONFIG
# =========================================================
CSV_PATH = "../data/master_lakes_final.csv"
OUTPUT_GIF = "../outputs/bod_race_final.gif"
FRAME_DIR = "gif_frames"

FAMOUS_LAKES = [
    "Bellandur Lake", "Varthur Lake", "Ulsoor Lake", "Hebbal Lake",
    "Sankey Tank", "Madiwala Tank", "Agaram Lake", "Nagavara Lake",
    "Jakkur Lake", "Yediyur Tank", "Puttenahalli Lake", "Hesaraghatta Lake",
    "Kaikondanahalli Lake", "Kengeri Tank", "Lalbagh Tank",
    "Doddabidarakallu Lake", "Kasavanahalli Lake", "Kothanuru Lake",
    "Rachenahalli Lake"
]
BARS_SHOWN = len(FAMOUS_LAKES)
STEPS_PER_MONTH = 10
GIF_FRAME_DURATION_MS = 400

LAKE_COL, MONTH_COL, BOD_COL = "base_lake_name", "sampling_month", "bod_mgl"


def load_and_pivot(csv_path):
    df = pd.read_csv(csv_path)
    work = df[df[LAKE_COL].isin(FAMOUS_LAKES)][[LAKE_COL, MONTH_COL, BOD_COL]].dropna(subset=[BOD_COL]).copy()
    work["month_dt"] = pd.to_datetime(work[MONTH_COL], format="%b-%y")

    agg = work.groupby([LAKE_COL, "month_dt"], as_index=False)[BOD_COL].mean()
    pivot = agg.pivot(index="month_dt", columns=LAKE_COL, values=BOD_COL).sort_index()
    pivot_top = pivot.reindex(columns=FAMOUS_LAKES)
    pivot_top.index = pivot_top.index.strftime("%b-%Y")

    # reinsert any silently-missing months (e.g. a month with zero readings across all lakes)
    full_range = pd.date_range(
        pd.to_datetime(pivot_top.index[0], format="%b-%Y"),
        pd.to_datetime(pivot_top.index[-1], format="%b-%Y"),
        freq="MS",
    ).strftime("%b-%Y")
    pivot_top = pivot_top.reindex(full_range).interpolate(method="linear").ffill().bfill()
    return pivot_top


def build_frames(pivot_top):
    labels = pivot_top.columns.tolist()
    raw = pivot_top.values
    n_frames = (len(pivot_top) - 1) * STEPS_PER_MONTH + 1
    interp = np.zeros((n_frames, raw.shape[1]))
    frame_labels = []

    for i in range(len(pivot_top) - 1):
        for s in range(STEPS_PER_MONTH):
            idx = i * STEPS_PER_MONTH + s
            t = s / STEPS_PER_MONTH
            interp[idx] = raw[i] * (1 - t) + raw[i + 1] * t
            frame_labels.append(pivot_top.index[i])
    interp[-1] = raw[-1]
    frame_labels.append(pivot_top.index[-1])
    return labels, interp, frame_labels


def render_and_save(labels, interp, frame_labels):
    if os.path.exists(FRAME_DIR):
        shutil.rmtree(FRAME_DIR, ignore_errors=True)
    os.makedirs(FRAME_DIR, exist_ok=True)

    colors = plt.cm.tab20(np.linspace(0, 1, len(labels)))
    color_map = dict(zip(labels, colors))

    fig, ax = plt.subplots(figsize=(11, 10))
    plt.subplots_adjust(left=0.28, right=0.92, top=0.90, bottom=0.08)

    saved_paths = []
    for frame in range(len(interp)):
        ax.clear()
        vals = interp[frame]
        order = np.argsort(vals)[::-1][:BARS_SHOWN]
        names = [labels[i] for i in order]
        values = [vals[i] for i in order]
        y_pos = np.arange(BARS_SHOWN)[::-1]

        ax.barh(y_pos, values, color=[color_map[n] for n in names])
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names, fontsize=9)

        for y, v, n in zip(y_pos, values, names):
            ax.text(v + max(vals.max() * 0.02, 0.3), y, f"{v:.1f}", va="center", fontsize=8)

        frame_max = max(vals.max(), 5)
        ax.set_xlim(0, frame_max * 1.2)
        ax.set_ylim(-0.6, BARS_SHOWN - 0.4)
        ax.set_xlabel("BOD (mg/L)")
        ax.set_title(
            f"BOD Levels Over Time — Bangalore's Famous Lakes\n{frame_labels[frame]}",
            fontsize=13, fontweight="bold",
        )
        ax.spines[["top", "right"]].set_visible(False)
        ax.grid(axis="x", alpha=0.2)

        path = f"{FRAME_DIR}/frame_{frame:04d}.png"
        fig.savefig(path, dpi=100)
        saved_paths.append(path)

    plt.close(fig)
    print(f"Rendered {len(saved_paths)} frames")

    frames = [PILImage.open(p) for p in saved_paths]
    frames[0].save(
        OUTPUT_GIF, save_all=True, append_images=frames[1:],
        duration=GIF_FRAME_DURATION_MS, loop=0,
    )
    print(f"Saved {OUTPUT_GIF}")


if __name__ == "__main__":
    pivot_top = load_and_pivot(CSV_PATH)
    labels, interp, frame_labels = build_frames(pivot_top)
    render_and_save(labels, interp, frame_labels)
