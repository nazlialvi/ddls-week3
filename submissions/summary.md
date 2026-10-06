# Project summary

## Goal

Dr. Camille Dubois and the tumour board need an explainable way to rank 198 diagnosed primary breast tumours most likely to be ER-positive for limited endocrine-therapy review. The decision is whether ESR1 alone is sufficient or whether a small oestrogen-programme signature is needed; this is a second opinion on recorded ER status, not a replacement for pathology.

## Result versus baseline

The four-gene signature (`ESR1`, `GATA3`, `FOXA1`, `GREB1`) achieved **88.38% accuracy (175/198)** under held-out cross-validation, versus the majority-class baseline of **67.68% (134/198)**: a **+20.71-point margin**. ESR1 alone tied the four-gene signature exactly in this held-out evaluation: **88.38% (175/198)**. The added genes changed which specific cases were misclassified but did not improve the aggregate number correct.

## Caveat

The hospital/centre-confounding check gave **χ²(4) = 8.277, p = 0.082**. The observed centre differences are not statistically distinguishable from chance at the conventional threshold in this sample, but the test does not rule out centre confounding, batch effects, or limited transportability; hospital therefore stayed out of the feature set. Clinically recorded ER status and ESR1 mRNA expression measure different biological layers, so imperfect concordance may limit the result’s interpretation and generalisation.

## AI-use disclosure

Pi built the `uv` environment, ran the analysis, wrote the result files and report, and built the FastAPI/Tailwind dashboard. During the session it fixed the undefined headline counts, raw template text leaking into the gene table, non-clickable gene rows, the README port mismatch, and dynamically injected bar colours. Live API/assert-based tests verified the result fields, the ESR1-exclusion toggle’s updated headline and baseline comparison, and the expression-detail data and click path for every shortlist gene.
