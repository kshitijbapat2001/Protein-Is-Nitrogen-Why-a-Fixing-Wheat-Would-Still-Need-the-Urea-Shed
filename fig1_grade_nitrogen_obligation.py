"""Figure 1 and its data file. Run: python3 fig1_grade_nitrogen_obligation.py"""

from __future__ import annotations

import csv
import os

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

SOURCE_STANDARDS = ("Grain Trade Australia (2025) Wheat trading standards "
                    "2025/26; Grains Australia wheat classes")
SOURCE_TARGET = "Rogers & Oldroyd (2014) J Exp Bot 65:1939-1946"

PALETTE = {"s1": "#2a78d6", "s2": "#eb6834", "s3": "#1baf7a",
           "s4": "#eda100", "s5": "#e87ba4"}
SURFACE = "#fcfcfb"
INK = "#0b0b0b"
INK_2 = "#52514e"
INK_3 = "#8a8985"

N_TO_PROTEIN_FACTOR = 5.7
REFERENCE_YIELD_T_HA = 4.0
WHEAT_GRADES = [("APH2", 13.0), ("H2", 11.5), ("APW1", 10.5)]
TARGET_LOW = 25.0
TARGET_HIGH = 50.0
GRADE_COLOURS = [PALETTE["s1"], PALETTE["s5"], PALETTE["s3"]]


def grain_n_removed(yield_t_ha, protein_pc):
    return yield_t_ha * 1000.0 * (protein_pc / 100.0) / N_TO_PROTEIN_FACTOR


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


def write_data(outdir: str = "../data", name: str = "Figure1_data.csv"):
    os.makedirs(outdir, exist_ok=True)
    path = os.path.join(outdir, name)
    header = ["grade", "protein_floor_pc", "grain_yield_t_ha",
              "grain_N_removed_kg_N_ha", "target_low_kg_N_ha",
              "target_high_kg_N_ha", "coverage_low_pc", "coverage_high_pc",
              "source_protein_standard", "source_engineering_target"]
    rows = []
    for code, protein in WHEAT_GRADES:
        for y in (2.0, 3.0, 4.0, 5.0, 6.0):
            n = grain_n_removed(y, protein)
            rows.append([code, f"{protein:.1f}", f"{y:.1f}", f"{n:.1f}",
                         f"{TARGET_LOW:.0f}", f"{TARGET_HIGH:.0f}",
                         f"{TARGET_LOW / n * 100:.1f}",
                         f"{min(TARGET_HIGH / n * 100, 100.0):.1f}",
                         SOURCE_STANDARDS, SOURCE_TARGET])
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(header)
        w.writerows(rows)
    print(f"  wrote {path}  ({len(rows)} rows)")


def panel_a(ax) -> None:
    y = np.linspace(1.0, 7.0, 300)
    lo, hi = TARGET_LOW, TARGET_HIGH

    ax.axhspan(lo, hi, color=PALETTE["s2"], alpha=0.14, zorder=1)
    ax.axhline(lo, color=PALETTE["s2"], linewidth=0.9, linestyle=(0, (4, 3)),
               zorder=2)
    ax.axhline(hi, color=PALETTE["s2"], linewidth=0.9, linestyle=(0, (4, 3)),
               zorder=2)
    ax.text(6.92, (lo + hi) / 2.0,
            f"engineering target\n{lo:.0f}–{hi:.0f} kg N ha$^{{-1}}$",
            ha="right", va="center", fontsize=7.4, color=PALETTE["s2"],
            fontweight="bold", linespacing=1.3)

    for (code, protein), colour in zip(WHEAT_GRADES, GRADE_COLOURS):
        ax.plot(y, grain_n_removed(y, protein), color=colour, linewidth=2.0,
                zorder=4)
        ax.text(7.08, grain_n_removed(7.0, protein), f"{code}\n{protein:.1f}%",
                color=colour, fontsize=7.4, va="center", ha="left",
                fontweight="bold", linespacing=1.25)

    yr = REFERENCE_YIELD_T_HA
    ax.axvline(yr, color=INK_3, linewidth=0.8, linestyle=(0, (1, 1.8)), zorder=3)
    for (_code, protein), colour in zip(WHEAT_GRADES, GRADE_COLOURS):
        ax.plot([yr], [grain_n_removed(yr, protein)], marker="o", markersize=7,
                color=colour, markeredgecolor=ax.get_facecolor(),
                markeredgewidth=1.4, zorder=6)
    ax.annotate(f"{yr:.0f} t ha$^{{-1}}$ reference crop",
                xy=(yr, grain_n_removed(yr, WHEAT_GRADES[0][1])),
                xytext=(2.0, 138), textcoords="data", ha="left", va="center",
                fontsize=7.2, color=INK_2,
                arrowprops=dict(arrowstyle="-", color=INK_3, linewidth=0.7,
                                shrinkA=2, shrinkB=4))

    ax.set_xlim(1.0, 7.0)
    ax.set_ylim(0, 165)
    ax.set_xlabel("Grain yield (t ha$^{-1}$)")
    ax.set_ylabel("Grain nitrogen removed (kg N ha$^{-1}$)")
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)
    ax.text(0.02, 0.955,
            f"protein = N × {N_TO_PROTEIN_FACTOR}, so a grade floor is a\n"
            "nitrogen floor",
            transform=ax.transAxes, ha="left", va="top", fontsize=7.2,
            color=INK_2, linespacing=1.35)
    ax.text(0.0, 1.05, "a", transform=ax.transAxes, fontsize=11,
            fontweight="bold", color=INK, va="bottom")


def panel_b(ax) -> None:
    yr = REFERENCE_YIELD_T_HA
    lo, hi = TARGET_LOW, TARGET_HIGH
    codes = [g[0] for g in WHEAT_GRADES]
    obligations = [grain_n_removed(yr, g[1]) for g in WHEAT_GRADES]

    x = np.arange(len(codes))
    w = 0.46
    gap = 2.0

    for i, total in enumerate(obligations):
        ax.bar(x[i], hi, width=w, color=PALETTE["s2"], zorder=3)
        ax.bar(x[i], hi - lo, bottom=lo, width=w, color=PALETTE["s2"],
               alpha=0.45, zorder=4)
        ax.plot([x[i] - w / 2, x[i] + w / 2], [lo, lo], color="white",
                linewidth=1.2, zorder=5)
        ax.bar(x[i], total - hi, bottom=hi + gap, width=w,
               color=PALETTE["s1"], zorder=3)

        ax.text(x[i], lo / 2.0, f"{lo:.0f}–{hi:.0f}", ha="center",
                va="center", color="white", fontsize=8, fontweight="bold",
                zorder=6)
        ax.text(x[i], hi + gap + (total - hi) / 2.0, f"{total - hi:.0f}",
                ha="center", va="center", color="white", fontsize=8,
                fontweight="bold", zorder=6)
        ax.text(x[i], total + 3.5,
                f"{total:.0f} kg N ha$^{{-1}}$\n"
                f"{lo / total * 100:.0f}–{hi / total * 100:.0f}% covered",
                ha="center", va="bottom", fontsize=7.4, color=INK,
                fontweight="bold", linespacing=1.35)

    ax.set_xticks(x)
    ax.set_xticklabels([f"{g[0]}\n{g[1]:.1f}% protein" for g in WHEAT_GRADES],
                       fontsize=7.8, color=INK)
    ax.set_xlabel("Milling grade delivered", labelpad=3)
    ax.set_ylabel(f"Grain nitrogen obligation at {yr:.0f} t ha$^{{-1}}$\n"
                  "(kg N ha$^{-1}$)")
    ax.set_ylim(0, 118)
    ax.set_xlim(-0.62, len(codes) - 0.38)
    ax.grid(axis="y", zorder=0)
    ax.set_axisbelow(True)

    handles = [
        Patch(facecolor=PALETTE["s2"], label="Coverable by engineered fixation"),
        Patch(facecolor=PALETTE["s1"],
              label="Residual: manufactured fertiliser still required"),
    ]
    ax.legend(handles=handles, loc="upper left", bbox_to_anchor=(-0.02, -0.22),
              labelcolor=INK_2, handlelength=1.5, handleheight=1.0)
    ax.text(0.0, 1.05, "b", transform=ax.transAxes, fontsize=11,
            fontweight="bold", color=INK, va="bottom")


def main() -> None:
    apply_print_style()
    fig, axes = plt.subplots(1, 2, figsize=(9.4, 4.0),
                             gridspec_kw={"width_ratios": [1.18, 1.0],
                                          "wspace": 0.40})
    panel_a(axes[0])
    panel_b(axes[1])
    save(fig, "Figure1_grade_nitrogen_obligation")
    plt.close(fig)
    write_data()


if __name__ == "__main__":
    main()
