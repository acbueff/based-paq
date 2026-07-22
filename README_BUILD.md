# Building paq_living.pdf

The host has no full TeX Live (the conda `ml` env ships pdflatex without LaTeX format files),
so the document is compiled with a self-contained **tectonic** binary (checked in this
directory; it fetches packages on demand over IPv4):

```bash
cd /home/andbu/Documents/autoresearch/BASED-PAQ-paper
./tectonic -X compile paq_living.tex        # runs TeX + BibTeX passes automatically
```

On any machine with full TeX Live the equivalent is:

```bash
pdflatex paq_living && bibtex paq_living && pdflatex paq_living && pdflatex paq_living
```

Figures are generated as publication-quality vector PDFs plus preview PNGs (light+dark) by
`BASED/scripts/paq_figs.py` from `research/paq_verdict.json` + `research/paq_t_gate_verdict.json`
and the figure-specific verdicts loaded by that script. The first-page overview reads the sealed
result directly from `research/paq_sealed_final_sealed_verdict.json`; nothing is hand-entered.
Re-run the script and re-copy after any new verdict:

```bash
cd /home/andbu/Documents/autoresearch/BASED
/home/andbu/miniconda3/envs/ml/bin/python scripts/paq_figs.py
cp paper/figs/*_light.pdf paper/figs/*_light.png ../BASED-PAQ-paper/figures/
```
