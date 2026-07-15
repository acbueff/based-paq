# AGENT PROMPT — compose the PAQ "living paper" (comprehensive, honest, ongoing-research LaTeX) + Sol clarity review

> Paste as the task for the composing agent. You are the WRITER (Fable composes prose; Opus-4.8 orchestrates;
> Sol reviews). Working dirs: repo `/home/andbu/Documents/autoresearch/BASED` (source of results/figures/notes);
> output `/home/andbu/Documents/autoresearch/BASED-PAQ-paper` (LaTeX lives here; already has `aaai2027.sty`,
> `aaai2027.bst`, `AuthorKit27/`, `figures/`). This is a **LIVING document** the human uses to communicate ONGOING
> research to colleagues — comprehensive, current-state, HONEST. It is NOT an AAAI camera-ready; page limits do not
> bind — completeness + clarity do. No GPU. Do not touch the frozen harness/pins. Commit is the orchestrator's job.

## 0. THE HARD HONESTY BAR (this program's #1 failure mode is over-claiming — violate this and the doc is useless)
State the CURRENT TRUTH, not a hoped-for win:
- PAQ (training-free page selection via the reader's own question→page attention) **LOSES head-to-head to a SOTA
  trained retriever (ColQwen2-fresh) at page level by ~10pt** (LB95 −0.129 @b=5%), on every stratum.
- **CAPS (ACL 2026, Zhu et al., "Attention as Selector") already published** attention-based page selection beating
  ColPali on these benchmarks — the page-level *method* is scooped; cite it prominently and position against it.
- What IS genuinely ours + confirmed: (i) a rigorous **multi-query REVERSIBILITY** result — per-query re-selection
  beats commit-once selection (paq vs its own scorer committed once, and vs a gold-oracle static), **both cells,
  907-query confirmatory, doc-clustered**; (ii) the first *executed* retrieval-vs-selection panel on
  MMLongBench-Doc/LongDocURL at 64K; (iii) the finding that **page quantization (not selection quality) is the
  binding constraint** → the open contribution is BELOW page granularity.
- PAQ-T (expert-head + higher-res) reaches **RECALL parity** with ColQwen2 zero-shot (0.674/0.628 vs 0.664/0.536) —
  but that is *recall*, accuracy read-eval PENDING; and expert-head selection is CAPS's method (our novelty = the
  multi-query amortization, not the selector).
- The extensions (E2/PAQ-KV token-level, E1/PAQ-Fovea region-level) are PROPOSED/PENDING, ~1-in-3 odds — mark them
  clearly as roadmap, not results.
- Use the exact confidence intervals; report per-cell (never average away heterogeneity); label the 4 timeout-missing
  queries; keep the oracle-answerable subset secondary; `gold_frequency_static` is a strong gold-informed static
  ceiling, NOT "best possible"; full-context/oracle are reference rows, not competitors; the query-agnostic eviction
  family (H2O/FastV/LOOK-M/KVzip) is a demoted control (≤ random; disclosed proxies).

## 1. SOURCES (read these; pull numbers verbatim — do NOT invent)
- Results/verdicts: `research/paq_verdict.json` (confirmatory isolation + budget curves + retrieval secondary +
  strata), `research/paq_t_gate_verdict.json` (PAQ-T recall gate), `research/paq_results.jsonl` (per-query per-arm),
  `research/paq_retrieval_scores.json`.
- Design notes: `research/design_notes/paq_build_spec_2026-07-14.md`, `paq_gate_result_2026-07-14.md`,
  `paq_result_review_2026-07-14.md`, `paq_aaai_review_2026-07-15.md`, `fable_paq_vs_colqwen_2026-07-15.md`,
  `fable_paq_caps_extensions_2026-07-15.md`, `lane_c_fable_2026-07-14.md`.
- The prior prose draft (reuse/extend, honor its honest framing): `paper/main.md`.
- The bus (chronology + all numbers): `research/MM_LANES/CROSS_LANE_LOG.md`; the retro `retro/RETRO_2026-07-15.md`.
- Harness (for the algorithm boxes): `scripts/paq.py`, `scripts/paq_t_gate.py`, `scripts/paq_retrieval_arms.py`.
- Figure generator: `scripts/paq_figs.py` (reads the verdict JSONs → `paper/figs/*.png`, light+dark). Re-run it;
  EXTEND it for the new results (retrieval reversal bars; PAQ-T recall ladder coarse→hires→expert vs ColQwen2; the
  page→region→token reversibility schematic). Copy the light-theme PNGs into `BASED-PAQ-paper/figures/`.

## 2. DELIVERABLE — `BASED-PAQ-paper/paq_living.tex` (+ `references.bib`), comprehensive sections:
1. **Abstract** — the multi-query doc-VQA setting; the reversibility result; honest current state (page-level
   scooped/lost, below-page open).
2. **Introduction** — problem, multi-query regime (MMLongBench-Doc ~6.97 q/doc, LongDocURL ~3.6), the question:
   can query-conditioned selection beat retrieval at matched budget on long multimodal docs?
3. **Benchmarks & setup** — the two cells, the frozen pins (screen 30 docs/cell ⊂ confirmatory 80 docs/cell / 907 q),
   Qwen3-VL-8B reader, matched page budget b, the 37% oracle-unanswerable base-model ceiling.
4. **Baselines (the executed panel)** — full-context, oracle, gold_frequency_static, paq_stale, SnapKV-fresh/stale,
   H2O/FastV/LOOK-M/KVzip (demoted controls, proxies disclosed), **ColQwen2-fresh/stale, CLIP** (the deployable
   retrievers). A clear taxonomy: reversible (re-select) vs commit-once; deployable vs oracle vs reference.
5. **Method(s)** — PAQ (coarse-to-fine page routing: eager two-pass in-place question→page attention, top-b, reread);
   the REVERSIBILITY framing + the ISOLATION protocol (paq_stale = same scorer committed once; gold_frequency_static
   = gold-oracle static); PAQ-T (expert-head via held-out-doc CV + higher scoring-res); and the EXTENSIONS
   (E2/PAQ-KV token-level reversible KV selection; E1/PAQ-Fovea region-level foveation — marked ROADMAP).
6. **Maths** (proper notation + short derivations/definitions): recall@b; matched per-instance page budget;
   **document-cluster paired bootstrap** LB95 (define one-sided vs two-sided precisely); commitment_pressure =
   distinct_gold / (b·n_pages); the isolation-gate criterion (ISOLATED iff LB95(paq−paq_stale)>0 AND
   LB95(paq−gold_frequency_static)>0).
7. **Algorithms** (algorithm environments): (a) PAQ per-query scorer + matched-budget selection; (b) expert-head
   selection with held-out-doc CV (no selection-on-test); (c) the stale (commit-once) vs reselect arm deployments;
   (d) OOM-safe per-layer-hook attention capture.
8. **Results** — with figures + tables, per-cell:
   - Confirmatory isolation (paq vs paq_stale, vs gold_frequency_static; both cells; answerable subset; budget
     curves 2.5/5/10%; paq@10%≈full-context on longdocurl).
   - The retrieval comparison (PAQ vs ColQwen2-fresh/stale, CLIP) — the honest −10pt page-level loss + PAQ beating
     commit-once variants; the fusion ceiling (+0.035) + weak complementarity (6% rescue).
   - PAQ-T recall gate (coarse→hires→expert ladder; parity with ColQwen2; expert-head is the lever) — RECALL, read-eval pending.
   - Efficiency framing (training-free, no separate retriever; Sol's honest Pareto caveats — measurement pending).
9. **Related work** — SnapKV/H2O/FastV/LOOK-M/KVzip/Quest; **CAPS (prominently)**; ColPali/ColQwen2; MMLongBench-Doc/
   LongDocURL; the region-level neighbors (RegionRAG/Snappy/AGREE/ViCrop); the identified OPEN cell below page level.
10. **Current state, open questions & roadmap** — what's confirmed vs pending; the page→region→token reversibility
    thesis; the honest odds (~1-in-3) on the extensions; the moving retriever bar (ColQwen3).
11. **Limitations** — heterogeneity, page-routing scope, base-model ceiling, res-cap on big docs, CAPS overlap, recall≠accuracy.
12. **Appendix** — full panel tables; the cross-family review trail (anti-strawman); reproducibility (frozen shas,
    commands); the timeout-recovery note.

Compile-check: `pdflatex paq_living` (twice) + `bibtex` if a bib is used; ensure it builds (or leave a clear
`README` with the exact build command if a package is missing on the host). Reference every figure/table/algorithm
in the text; number equations. Keep ONE coherent authorial voice.

## 3. THEN — Sol clarity/interpretability review (run this CLI at the end, from the paper dir)
After the .tex compiles (or is complete), run:
```
cd /home/andbu/Documents/autoresearch/BASED-PAQ-paper && \
/home/andbu/.local/bin/cursor-agent -p -f --output-format text --model gpt-5.6-sol-xhigh \
"Review paq_living.tex as a colleague-facing LIVING research doc (comprehensive, ongoing research). GOAL: make it
CLEAR, interpretable, and easily digestible for a researcher new to this project. Specifically: (1) is the narrative
arc followable — problem → multi-query regime → PAQ → reversibility result → the honest ColQwen2 loss + CAPS overlap
→ below-page roadmap? Fix confusing ordering/transitions. (2) Are the FIGURES, PLOTS, TABLES clear, correctly
captioned, referenced in text, and self-explanatory? Flag any that are unreadable or unexplained. (3) Are the MATHS
(recall@b, doc-cluster LB95, commitment_pressure, the isolation gate) and ALGORITHM boxes (PAQ scorer, expert-head
CV, arm deployments) correct, well-notated, and understandable? (4) Is every claim HONEST + consistent with the
numbers (no over-claim; per-cell; CAPS credited; PAQ-T is recall-not-accuracy; extensions are roadmap)? (5) APPLY
concrete edits directly to paq_living.tex where they improve clarity/digestibility (tighten prose, fix captions,
add a missing definition, reorder), and RETURN a summary of what you changed + any remaining clarity/correctness
issues you could not fix. Do not weaken the honesty; do not invent results."
```
Fold Sol's edits (it edits in place); if Sol flags correctness/honesty issues, FIX them or escalate to the
orchestrator. Return: the final .tex path, the compiled PDF (or the build blocker), the figure list, and Sol's
change-summary + residual issues.
