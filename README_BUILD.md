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

Figures are the light-theme PNGs in `figures/`, generated (light+dark) by
`BASED/scripts/paq_figs.py` from `research/paq_verdict.json` + `research/paq_t_gate_verdict.json`
(nothing hand-entered — re-run the script and re-copy after any new verdict):

```bash
cd /home/andbu/Documents/autoresearch/BASED
/home/andbu/miniconda3/envs/ml/bin/python scripts/paq_figs.py
cp paper/figs/*_light.png ../BASED-PAQ-paper/figures/
```
