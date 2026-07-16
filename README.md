# based-paq

Living research document for **PAQ (Prefill-once, Ask-many)** — query-conditioned page selection for multi-query
document VQA. This is an *ongoing-research* paper (not a camera-ready): it documents the benchmarks, baselines,
methods, current results, and open roadmap, and is updated as the research evolves.

- `paq_living.tex` / `paq_living.pdf` — the comprehensive living paper (build: `tectonic paq_living.tex`).
- `figures/` — generated figures.
- `references.bib` — bibliography.
- `LIVING_PAPER_COMPOSE_PROMPT.md` — the prompt used to (re)compose the document.

Current state (2026-07-16, honest): the confirmed contribution is a multi-query **reversibility** result
(per-query re-selection beats commit-once selection, both cells, doc-clustered; verified robust to a
KV-cache bug found and fixed mid-program). PAQ v1 does **not** beat a SOTA trained retriever (ColQwen2) at
page level, and page-level attention selection was concurrently published by CAPS (ACL 2026). The expert-head
variant **PAQ-T** now has its accuracy read-eval: **non-inferiority (parity)** with ColQwen2-fresh at matched
budget — training-free, single model, but *not* a beat. Two lanes are running to convert parity into a beat:
(B) an off-benchmark LoRA selection-adapter (designed, CPU prep done, GPU-gated) and (C) below-page **PAQ-KV**
reversible KV-block selection (identity spike passed; 30-doc dev screen in progress). A sealed fresh test set
(73/45 docs) is reserved for one-touch final evaluation. See the paper for details.
