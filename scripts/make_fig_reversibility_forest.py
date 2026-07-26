#!/usr/bin/env python
"""Seaborn re-render of the reversibility forest (figures/fig_reversibility_forest.pdf).

Replaces fig_j_reversibility_light.pdf with the paper's forest style
(matching scripts/make_fig_forest_contrasts.py). Values transcribed from the
verdict artifacts (nothing re-derived):
  confirmatory below-page gate: generated/isogate_macros.tex
      (BASED/research/paq_isogate_kv_verdict.json)
  historical page-level gate:   BASED/research/paq_verdict.json
      cells/{longdocurl,mmlongdoc}/isolation/*
  clean-cache re-run:           BASED/research/paq_revcrop_verdict.json
      (24 docs / 150 q, pooled over both cells; CLEAN arms)
  30-doc below-page replication: BASED/research/paqc_mmlongdoc_audit_verdict.json
      supporting/reversibility_paqkv_minus_stale (delta/lb95; ub95 = +0.480
      as published in the companion note and the manuscript)

Run inside the `ml` conda env: python scripts/make_fig_reversibility_forest.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

C_MMLB = "#2a78d6"   # blue  (benchmark color scheme shared with fig_forest_contrasts)
C_LDU = "#008300"    # green
C_POOL = "#666666"   # gray = pooled over both cells
INK = "#333333"

PANEL_CONF = [  # confirmatory below-page gate, 80 docs/cell, post-fix
    ("vs commit-once · MMLB", 0.137, 0.103, 0.169, C_MMLB),
    ("vs commit-once · LDU", 0.211, 0.136, 0.289, C_LDU),
    ("vs gold static · MMLB", 0.213, 0.160, 0.266, C_MMLB),
    ("vs gold static · LDU", 0.230, 0.178, 0.276, C_LDU),
]
PANEL_HIST = [  # historical page-level gate (pre-fix cohort)
    ("vs commit-once · MMLB", 0.163, 0.126, 0.200, C_MMLB),
    ("vs commit-once · LDU", 0.257, 0.184, 0.330, C_LDU),
    ("vs gold static · MMLB", 0.104, 0.063, 0.144, C_MMLB),
    ("vs gold static · LDU", 0.108, 0.045, 0.164, C_LDU),
]
PANEL_CLEAN = [  # clean-cache re-run, 24 docs / 150 q, pooled
    ("vs commit-once (pooled)", 0.264, 0.187, 0.334, C_POOL),
    ("vs gold static (pooled)", 0.187, 0.137, 0.246, C_POOL),
]
PANEL_REPL = [  # 30-doc below-page replication, MMLB screen, first-query commit
    ("vs first-query commit · MMLB", 0.379, 0.273, 0.480, C_MMLB),
]

PANELS = [
    ("(a) Confirmatory below-page gate (post-fix)", PANEL_CONF),
    ("(b) Historical page-level gate (pre-fix)", PANEL_HIST),
    ("(c) Clean-cache re-run (24 docs)", PANEL_CLEAN),
    ("(d) 30-doc below-page replication", PANEL_REPL),
]


def main():
    sns.set_theme(style="whitegrid", font="serif", rc={
        "font.size": 7, "axes.labelsize": 7.5, "xtick.labelsize": 7,
        "ytick.labelsize": 7, "axes.titlesize": 7.5,
        "grid.linewidth": 0.4, "grid.color": "#d9d9d9",
        "axes.edgecolor": "#999999", "axes.linewidth": 0.6,
        "mathtext.fontset": "dejavuserif",
    })
    heights = [len(rows) for _, rows in PANELS]
    fig, axes = plt.subplots(
        4, 1, figsize=(2.15, 3.6), sharex=True,
        gridspec_kw={"height_ratios": heights, "hspace": 0.85},
    )
    for ax, (title, rows) in zip(axes, PANELS):
        n = len(rows)
        for i, (label, d, lo, hi, color) in enumerate(rows):
            y = n - 1 - i
            ax.plot([lo, hi], [y, y], color=color, lw=1.1,
                    solid_capstyle="butt", zorder=2)
            for cap in (lo, hi):
                ax.plot([cap, cap], [y - 0.16, y + 0.16], color=color,
                        lw=0.9, zorder=2)
            ax.scatter([d], [y], s=14, marker="o", facecolors=color,
                       edgecolors=color, linewidths=0.9, zorder=3)
        ax.axvline(0.0, color="#888888", lw=0.7, ls=(0, (3, 2)), zorder=1)
        ax.set_ylim(-0.6, n - 0.4)
        ax.set_yticks(range(n))
        ax.set_yticklabels([r[0] for r in reversed(rows)], color=INK)
        ax.set_title(title, loc="left", color=INK, pad=3,
                     fontweight="bold", fontsize=7.2)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="y", visible=False)
        sns.despine(ax=ax, left=True)
    axes[-1].set_xlim(-0.02, 0.50)
    axes[-1].set_xlabel(
        "$\\Delta$ accuracy, fresh $-$ comparator "
        "(document-clustered 95% CI)", color=INK)
    fig.savefig("figures/fig_reversibility_forest.pdf", bbox_inches="tight")
    print("wrote figures/fig_reversibility_forest.pdf")


if __name__ == "__main__":
    main()
