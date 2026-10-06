# The question

Dr. Camille Dubois and the breast tumour board need an explainable way to rank the 198 already-diagnosed primary breast tumours most likely to be ER-positive for limited endocrine-therapy review. The decision is whether ESR1 alone is sufficient or whether adding a small oestrogen-programme signature gives a trustworthy improvement; this is a second opinion on recorded ER status, not cancer detection or a replacement for pathology.

# The data

The supplied file, `data/expression.csv`, contains 198 tumour rows and 1,009 columns: `sample_id`; the binary target `er_status`; `hospital`; `grade`; `age`; `tumor_size_cm`; and 1,003 gene-expression columns. The labels are 134 `ER-positive` and 64 `ER-negative`. The expression values are described as cleaned log2 measurements. The accompanying fields are clinical covariates; hospital is a five-centre identifier/check, not a model feature. No batch identifier, processing-date field, or processing history is supplied. The transcript says two `grade` values are missing. The supplied data also lack independent protein measurements, external validation, and a separate held-out truth source beyond `er_status`.

# The honest baseline

The trivial baseline is **67.68% accuracy: 134/198**, obtained by calling every tumour ER-positive because that is the majority class. Every reported model number is interpreted against this baseline rather than treated as meaningful in isolation.

# What you did and what it gave

The fixed four-gene signature uses `ESR1`, `GATA3`, `FOXA1`, and `GREB1`, selected from the interview’s biological knowledge before modelling. Regularised logistic regression was evaluated with stratified held-out cross-validation; hospital, grade, age, and tumour size were not model features. The signature achieved **88.38% accuracy: 175/198**, which is **+20.71 percentage points over the 67.68% majority baseline**. Under the same held-out pipeline, ESR1 alone also achieved **88.38% accuracy: 175/198**. The aggregate margin is therefore **exactly 0.00 percentage points**: a tie, not an advantage for the four-gene signature.

The tie is not because the models made identical decisions. They differed on two samples: ESR1 alone misclassified `GSM178023`, while the four-gene model misclassified `GSM178021`; each model still made 23 errors. The four added genes therefore changed which specific cases were misclassified without improving aggregate accuracy.

The dashboard’s **Scores by metric** panel separates validated model coefficients from exploratory univariate scores. Its **Contribution matrix** shows signed coefficients for the validated four-gene model only. The **Gene detail** panel uses raw values exported from the CSV and displays the selected gene’s expression distribution split by ER status. The **Headline stress test** toggle shows the ESR1-excluded result: `GATA3 + GREB1 + FOXA1` achieved **84.34%: 167/198**, or **+16.67 points over the majority baseline**, a **4.04-point drop from the tied ESR1-alone/four-gene result**.

# The trap and the humble truth

The principal trap is centre structure masquerading as ER biology. The hospital-by-label table was: GUY 23 positive/13 negative, IGR 38/12, JRH 11/13, KAR 38/13, and RH 24/13. The chi-square test of independence gave **χ²(4) = 8.277, p = 0.082**. At the conventional 0.05 threshold, these observed differences are not statistically distinguishable from chance in this sample; JRH’s 11/24 ER-positive rate is also consistent with sampling noise in a small centre. This does not rule out centre confounding, batch effects, or limited transportability. Hospital therefore remains excluded from the feature set and is used only in the centre check.

A second risk is the 1,003-gene-to-198-tumour ratio. The four-gene set was fixed from transcript domain knowledge, not selected by searching cross-validation performance across all 1,003 genes. The other genes shown in the dashboard were screened univariately and are exploratory, not validated evidence.

# The shortlist/recommendation

**Recommendation:** use ESR1 alone as the trustworthy headline result unless a larger independent dataset shows that the broader signature adds reproducible value. In this held-out evaluation, the four-gene signature adds **no aggregate accuracy over ESR1 alone: the result is an exact 175/198 tie**. It does change which two specific cases are misclassified, but it does not improve the total number correct; the extra complexity is therefore not justified by aggregate accuracy here.

## Validated model coefficients

These four genes were fixed before modelling and evaluated as the regularised, held-out four-gene signature:

- **ESR1** — strongest fitted coefficient and the direct ER-related biological signal; the recommended simple headline feature.
- **GATA3** — positive fitted coefficient and a transcript-nominated luminal/oestrogen-programme gene.
- **GREB1** — included from transcript domain knowledge; its fitted coefficient was small and negative in the four-gene model.
- **FOXA1** — included from transcript domain knowledge; its fitted coefficient was near zero in the four-gene model.

## Exploratory, univariate-only genes

These 11 genes came from scanning approximately 1,003 candidate genes without multiple-testing correction and without cross-validation. Their displayed scores are not comparable in trust level to the validated coefficients, and some may reflect chance rather than real signal:

- **TFF1** — strong univariate standardized separation and biologically plausible oestrogen/luminal relevance.
- **TBC1D9** — among the strongest univariate standardized separators; exploratory only.
- **C9orf116** — strong univariate standardized separation; exploratory only.
- **DNALI1** — strong univariate standardized separation; exploratory only.
- **DNAJC12** — strong univariate standardized separation; exploratory only.
- **CA12** — biologically plausible breast/luminal marker and strong univariate separation.
- **SCUBE2** — biologically associated with breast cancer biology and strong univariate separation.
- **DACH1** — strong univariate standardized separation; exploratory only.
- **TFF3** — plausible epithelial/luminal marker and strong univariate separation.
- **NAT1** — plausible breast/luminal marker and strong univariate separation.
- **ERBB4** — biologically relevant receptor gene with positive univariate separation.

# Caveats & next steps

The key biological caveat is that clinical `er_status` and mRNA expression measure different biological layers. ESR1 mRNA and ER protein status are not perfectly concordant, so discordant tumours can deflate the measured margin and limit generalisation to another assay or population; independent protein measurements and exact assay details were not supplied. The review-slot count, error priority, and borderline rule are also unresolved, so no clinical allocation or invented borderline threshold is reported.

Next steps are to obtain the missing Affymetrix probe-to-ESR1 mapping, batch and processing history, collection dates, filtering/sampling criteria, and any independent assay or external cohort. Then pre-specify the ESR1 threshold and operational review rules, validate ESR1 alone and the fixed signature on genuinely independent data, and retain hospital as a centre check rather than a predictor.

# AI-use disclosure

The AI agent built the reproducible `uv` Python environment, inspected the CSV, computed the majority baseline, ESR1-alone comparison, four-gene held-out cross-validation result, ESR1-excluded held-out result, hospital cross-tabulation and chi-square test, exported `results/gene_expression.json`, wrote `results/results.json`, and built the FastAPI/Tailwind dashboard in `app.py` with `requirements.txt` and `README.md`. The dashboard reads JSON/CSV-derived files from disk and uses no database.

Verification during this session included fixing the `undefined/undefined` headline display by adding the four-gene result’s `n_correct` and `n_total` fields; fixing malformed gene-table template rendering that exposed raw HTML text; wiring the non-clickable gene rows to the **Gene detail** panel; correcting the README port from 8000 to 8001; and replacing dynamically injected Tailwind bar colours with inline colours. A live API test verified that all 15 shortlist genes have 134 ER-positive and 64 ER-negative expression values. The same assert-based test verified the **Headline stress test** toggle’s real values: four-gene 175/198 at 88.38%, ESR1-excluded 167/198 at 84.34%, and a −4.04-point change; it also verified that detail data exist for every shortlist gene. The reported model metrics were scored from held-out cross-validation predictions, not training predictions.
