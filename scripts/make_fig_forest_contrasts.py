#!/usr/bin/env python
"""Three-panel forest plot of the paper's key paired contrasts (fig_forest_contrasts.pdf).

Every number is transcribed from the verdict-backed values already in
paq_aaai_v3.tex (nothing re-derived):
  panel A: generated/isogate_macros.tex  (research/paq_isogate_kv_verdict.json)
  panel B: tab:contrasts sources -- paq_colqwen_corrected_beat.json (MMLB dev),
           paq_sealed_final_sealed_verdict.json (MMLB sealed),
           paqc_topup_fulloracle_posthoc.json / corrected-loader LDU close-out,
           paq_mmdocrag_verdict.json, paq_mmdocirqa_verdict.json
  panel C: tab:crossreader sources -- cross-reader port verdicts
           (BASED/research/paq_{qwen3vl4b,qwen25vl,internvl}_*_verdict.json)

Run inside the `ml` conda env:  python scripts/make_fig_forest_contrasts.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

# Categorical palette (dataviz reference palette, slots 1-4; all-pairs validated).
C_MMLB = "#2a78d6"   # blue
C_LDU = "#008300"    # green
C_RAG = "#e87ba4"    # magenta
C_IR = "#c98500"     # yellow (dark step for print contrast)
INK = "#333333"

# (label, delta, lo, hi, color, emphasize)
PANEL_A = [  # PAQ-KV fresh minus comparator, confirmatory below-page isolation gate
    ("vs commit-once · MMLB", 0.137, 0.103, 0.169, C_MMLB, False),
    ("vs commit-once · LDU", 0.211, 0.136, 0.289, C_LDU, False),
    ("vs gold static · MMLB", 0.213, 0.160, 0.266, C_MMLB, False),
    ("vs gold static · LDU", 0.230, 0.178, 0.276, C_LDU, False),
]
PANEL_B = [  # PAQ-KV minus ColQwen2-fresh, per dataset
    ("MMLB (dev)", 0.077, 0.040, 0.115, C_MMLB, False),
    ("MMLB (sealed)", 0.076, 0.029, 0.122, C_MMLB, True),
    ("MMDocRAG", 0.057, 0.040, 0.076, C_RAG, False),
    ("LDU", 0.019, -0.019, 0.061, C_LDU, False),
    ("MMDocIR-QA", -0.043, -0.065, -0.011, C_IR, False),
]
PANEL_C = [  # PAQ-KV minus ColQwen2-fresh, per reader (MMLB and LDU dev pins)
    ("Qwen3-VL-8B · MMLB", 0.077, 0.040, 0.115, C_MMLB, False),
    ("Qwen3-VL-8B · LDU", 0.019, -0.019, 0.061, C_LDU, False),
    ("Qwen3-VL-4B · MMLB", 0.030, -0.004, 0.065, C_MMLB, False),
    ("Qwen3-VL-4B · LDU", 0.006, -0.028, 0.043, C_LDU, False),
    ("Qwen2.5-VL-7B · MMLB", 0.007, -0.037, 0.049, C_MMLB, False),
    ("Qwen2.5-VL-7B · LDU", -0.078, -0.116, -0.037, C_LDU, False),
    ("InternVL3.5-8B · MMLB", -0.067, -0.106, -0.029, C_MMLB, False),
    ("InternVL3.5-8B · LDU", -0.090, -0.127, -0.057, C_LDU, False),
]

PANELS = [
    ("(a) Isolation gate: fresh − committed", PANEL_A),
    ("(b) PAQ-KV − ColQwen2, per dataset", PANEL_B),
    ("(c) PAQ-KV − ColQwen2, per reader", PANEL_C),
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
        3, 1, figsize=(2.15, 4.3), sharex=True,
        gridspec_kw={"height_ratios": heights, "hspace": 0.55},
    )
    for ax, (title, rows) in zip(axes, PANELS):
        n = len(rows)
        for i, (label, d, lo, hi, color, emph) in enumerate(rows):
            y = n - 1 - i
            sig = lo > 0 or hi < 0
            ax.plot([lo, hi], [y, y], color=color, lw=1.1,
                    solid_capstyle="butt", zorder=2)
            for cap in (lo, hi):
                ax.plot([cap, cap], [y - 0.16, y + 0.16], color=color,
                        lw=0.9, zorder=2)
            marker = "D" if emph else "o"
            ax.scatter([d], [y], s=34 if emph else 14, marker=marker,
                       facecolors=color if sig else "white",
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
    axes[-1].set_xlim(-0.155, 0.305)
    axes[-1].set_xlabel(
        "$\\Delta$ accuracy (document-clustered 95% CI)", color=INK)

    # Key: benchmark colors (row 1) and marker semantics (row 2).
    from matplotlib.lines import Line2D
    color_handles = [
        Line2D([], [], marker="o", ls="none", ms=4.5, mfc=c, mec=c, label=l)
        for l, c in [("MMLB", C_MMLB), ("LDU", C_LDU),
                     ("MMDocRAG", C_RAG), ("MMDocIR-QA", C_IR)]
    ]
    style_handles = [
        Line2D([], [], marker="o", ls="none", ms=4.5, mfc=INK, mec=INK,
               label="CI excludes 0"),
        Line2D([], [], marker="o", ls="none", ms=4.5, mfc="white", mec=INK,
               label="CI includes 0"),
        Line2D([], [], marker="D", ls="none", ms=5, mfc=INK, mec=INK,
               label="sealed run"),
    ]
    leg1 = fig.legend(handles=color_handles, ncol=4, frameon=False,
                      loc="lower center", bbox_to_anchor=(0.5, -0.035),
                      fontsize=6.4, handletextpad=0.15, columnspacing=0.7)
    fig.add_artist(leg1)
    fig.legend(handles=style_handles, ncol=3, frameon=False,
               loc="lower center", bbox_to_anchor=(0.5, -0.075),
               fontsize=6.4, handletextpad=0.15, columnspacing=0.7)

    fig.savefig("figures/fig_forest_contrasts.pdf", bbox_inches="tight")
    print("wrote figures/fig_forest_contrasts.pdf")


if __name__ == "__main__":
    main()
