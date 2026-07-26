#!/usr/bin/env python
"""Seaborn bar-plot re-render of the page-level retrieval-reversal figure
(figures/fig_pagelevel_reversal_bars.pdf), replacing
fig_e_retrieval_reversal_light.pdf.

Values transcribed from BASED/research/paq_verdict.json (historical
page-level 903-query cohort, uncorrected ColQwen2 loader, disclosed in
Appendix "The Page-Level System in Detail"); identical to the values quoted
in that appendix's prose. Nothing re-derived.

Run inside the `ml` conda env: python scripts/make_fig_pagelevel_reversal_bars.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Colors: adjacent validated pair from the paper's categorical palette
# (orange/violet; deliberately NOT the blue/green used for benchmarks in the
# forest figures, since color here encodes the scorer, not the benchmark).
C_COLQ = "#eb6834"   # ColQwen2 (trained retriever)
C_PAQ = "#4a3aa7"    # PAQ page router (reader attention)
INK = "#333333"

CELLS = ["LongDocURL", "MMLongBench-Doc"]
# (label, color, fresh?, [LDU, MMLB])
ARMS = [
    ("ColQwen2 fresh", C_COLQ, True, [0.512, 0.328]),
    ("ColQwen2 commit-once", C_COLQ, False, [0.216, 0.138]),
    ("PAQ router fresh", C_PAQ, True, [0.386, 0.258]),
    ("PAQ router commit-once", C_PAQ, False, [0.128, 0.095]),
]


def main():
    sns.set_theme(style="whitegrid", font="serif", rc={
        "font.size": 7, "axes.labelsize": 7.5, "xtick.labelsize": 7.5,
        "ytick.labelsize": 7, "legend.fontsize": 6.6,
        "grid.linewidth": 0.4, "grid.color": "#d9d9d9",
        "axes.edgecolor": "#999999", "axes.linewidth": 0.6,
        "mathtext.fontset": "dejavuserif",
    })
    fig, ax = plt.subplots(figsize=(3.0, 1.9))
    x = np.arange(len(CELLS))
    width = 0.19
    for k, (label, color, fresh, vals) in enumerate(ARMS):
        pos = x + (k - 1.5) * (width + 0.015)
        ax.bar(pos, vals, width,
               facecolor=color if fresh else "white",
               edgecolor=color, linewidth=0.9,
               hatch=None if fresh else "////", label=label, zorder=2)
        for p, v in zip(pos, vals):
            ax.text(p, v + 0.012, f"{v:.3f}", ha="center", va="bottom",
                    fontsize=5.8, color=INK)
    ax.set_xticks(x)
    ax.set_xticklabels(CELLS, color=INK)
    ax.set_ylabel("Accuracy", color=INK)
    ax.set_ylim(0, 0.58)
    ax.grid(axis="x", visible=False)
    ax.legend(ncol=2, frameon=False, loc="lower center",
              bbox_to_anchor=(0.5, 1.02), handlelength=1.2,
              columnspacing=0.9, handletextpad=0.5)
    sns.despine(ax=ax, left=True)
    ax.tick_params(axis="y", length=0)
    fig.savefig("figures/fig_pagelevel_reversal_bars.pdf",
                bbox_inches="tight")
    print("wrote figures/fig_pagelevel_reversal_bars.pdf")


if __name__ == "__main__":
    main()
