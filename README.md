# based-paq

Living research document for **PAQ (Prefill-once, Ask-many)** — query-conditioned page selection for multi-query
document VQA. This is an *ongoing-research* paper (not a camera-ready): it documents the benchmarks, baselines,
methods, current results, and open roadmap, and is updated as the research evolves.

- `paq_living.tex` / `paq_living.pdf` — the comprehensive living paper (build: `tectonic paq_living.tex`).
- `figures/` — generated figures.
- `references.bib` — bibliography.
- `LIVING_PAPER_COMPOSE_PROMPT.md` — the prompt used to (re)compose the document.

Current state (2026-07-15, honest): the confirmed contribution is a multi-query **reversibility** result
(per-query re-selection beats commit-once selection, both cells, doc-clustered); PAQ does **not** beat a SOTA
trained retriever (ColQwen2) at page level, and page-level attention selection was concurrently published by CAPS
(ACL 2026); the open direction is *below* page granularity (token- and region-level). See the paper for details.
