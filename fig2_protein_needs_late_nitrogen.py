"""Figure 2 and its data file. Run: python3 fig2_protein_needs_late_nitrogen.py"""

from __future__ import annotations

import csv
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

SOURCE_ANY_TIMING = "Wang et al. (2023) Agric Water Manag 290:108587"
SOURCE_LATE = "Giordano et al. (2023) Field Crops Res 290:108740"
SOURCE_MECHANISM = "Bogard et al. (2010) J Exp Bot 61:4303-4312"

PALETTE = {"s1": "#2a78d6", "s2": "#eb6834", "s3": "#1baf7a",
           "s4": "#eda100", "s5": "#e87ba4"}
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
INK_3 = "#8a8985"

N_ADDITION_META = {"yield_gain": 0.1485, "gpc_gain": 0.0662}
LATE_SEASON_N = {"yield_effect": 0.0, "gpc_gain": 0.0396,
                 "pairwise_comparisons": 542, "environments": 127}


def apply_print_style() -> None:
    mpl.rcParams.update({
        "figure.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 8.5,
        "axes.labelsize": 8.5,
        "axes.labelcolor": INK,
        "axes.edgecolor": INK_3,
        "axes.linewidth": 0.7,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "xtick.color": INK_2,
        "ytick.color": INK_2,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "xtick.major.width": 0.7,
        "ytick.major.width": 0.7,
        "legend.frameon": False,
        "legend.fontsize": 8,
        "grid.color": "#e6e5e1",
        "grid.linewidth": 0.6,
        "lines.linewidth": 2.0,
        "lines.solid_capstyle": "round",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "svg.fonttype": "none",
    })


def save(fig, stem: str, outdir: str = "../figures"):
    os.makedirs(outdir, exist_ok=True)
    png = os.path.join(outdir, f"{stem}.png")
    pdf = os.path.join(outdir, f"{stem}.pdf")
    fig.savefig(png, dpi=400, bbox_inches="tight", pad_inches=0.04)
    fig.savefig(pdf, bbox_inches="tight", pad_inches=0.04)
    print(f"  wrote {png}")
    print(f"  wrote {pdf}")
    return png, pdf


def write_data(outdir: str = "../data", name: str = "Figure2_data.csv"):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, name)
    rows = [
        ["Nitrogen added (any timing)", "Grain yield",
         f"{N_ADDITION_META['yield_gain'] * 100:.2f}", "", "",
         SOURCE_ANY_TIMING],
        ["Nitrogen added (any timing)", "Grain protein concentration",
         f"{N_ADDITION_META['gpc_gain'] * 100:.2f}", "", "",
         SOURCE_ANY_TIMING],
        ["Nitrogen added late in the season", "Grain yield",
         f"{LATE_SEASON_N['yield_effect'] * 100:.2f}",
         str(LATE_SEASON_N["pairwise_comparisons"]),
         str(LATE_SEASON_N["environments"]), SOURCE_LATE],
        ["Nitrogen added late in the season", "Grain protein concentration",
         f"{LATE_SEASON_N['gpc_gain'] * 100:.2f}",
         str(LATE_SEASON_N["pairwise_comparisons"]),
         str(LATE_SEASON_N["environments"]), SOURCE_LATE],
    ]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["treatment", "response", "pooled_effect_pc",
                    "pairwise_comparisons", "environments", "source"])
        w.writerows(rows)
        w.writerow([])
        w.writerow(["mechanism", SOURCE_MECHANISM])
    print(f"  wrote {path}  ({len(rows)} rows)")


def main() -> None:
    apply_print_style()
    fig, ax = plt.subplots(figsize=(5.9, 3.5))

    treatments = [
        ("Nitrogen added\n(any timing)",
         N_ADDITION_META["yield_gain"] * 100.0,
         N_ADDITION_META["gpc_gain"] * 100.0),
        ("Nitrogen added\nlate in the season",
         LATE_SEASON_N["yield_effect"] * 100.0,
         LATE_SEASON_N["gpc_gain"] * 100.0),
    ]
    x = np.arange(len(treatments))
    w = 0.30
    gap = 0.035

    yields = [t[1] for t in treatments]
    proteins = [t[2] for t in treatments]

    ax.bar(x - w / 2 - gap, yields, width=w, color=PALETTE["s1"], zorder=3)
    ax.bar(x + w / 2 + gap, proteins, width=w, color=PALETTE["s3"], zorder=3)

    for i in range(len(treatments)):
        if yields[i] > 0.4:
            ax.text(x[i] - w / 2 - gap, yields[i] + 0.35, f"+{yields[i]:.2f}%",
                    ha="center", va="bottom", fontsize=8, color=INK,
                    fontweight="bold")
        else:
            ax.plot([x[i] - w - gap, x[i] - gap], [0, 0], color=PALETTE["s1"],
                    linewidth=2.4, solid_capstyle="butt", zorder=4)
            ax.text(x[i] - w / 2 - gap, 0.55, "neutral", ha="center",
                    va="bottom", fontsize=8, color=PALETTE["s1"],
                    fontweight="bold")
        ax.text(x[i] + w / 2 + gap, proteins[i] + 0.35, f"+{proteins[i]:.2f}%",
                ha="center", va="bottom", fontsize=8, color=INK,
                fontweight="bold")

    ax.annotate(
        "grain protein tracks post-anthesis\nnitrogen uptake, so protein is\n"
        "bought with late nitrogen",
        xy=(x[1] + w / 2 + gap, proteins[1] + 0.9), xytext=(1.05, 10.6),
        textcoords="data", ha="center", va="center", fontsize=7.4,
        color=INK_2, linespacing=1.4,
        arrowprops=dict(arrowstyle="-", color=INK_3, linewidth=0.7,
                        shrinkA=2, shrinkB=4),
    )

    ax.set_xticks(x)
    ax.set_xticklabels([t[0] for t in treatments], fontsize=8, color=INK)
    ax.set_ylabel("Pooled effect on wheat (%)")
    ax.set_ylim(0, 17.5)
    ax.set_xlim(-0.6, len(treatments) - 0.4)
    ax.yaxis.set_major_locator(plt.MultipleLocator(5))
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)

    handles = [
        Patch(facecolor=PALETTE["s1"], label="Grain yield"),
        Patch(facecolor=PALETTE["s3"], label="Grain protein concentration"),
    ]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(0.26, 1.02),
              labelcolor=INK_2, handlelength=1.5, handleheight=1.0)

    save(fig, "Figure2_protein_needs_late_nitrogen")
    plt.close(fig)
    write_data()


if __name__ == "__main__":
    main()
