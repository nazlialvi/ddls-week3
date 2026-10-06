# Specification: explainable ER-status shortlist

## Decision

The owner needs to decide whether to use **ESR1 expression alone** or a small broader oestrogen-programme signature to rank primary breast-tumour cases most likely to be **ER-positive** for a limited endocrine-therapy review. This is an explainable second opinion on the recorded clinical label, not breast-cancer detection and not a replacement for pathology.

## Data

Source: `data/expression.csv`.

- Rows: 198 primary breast-tumour records; one row per tumour.
- Columns: 1,009 total:
  - `sample_id`: sample/tumour identifier.
  - `er_status`: target label, encoded as `ER-positive` or `ER-negative`; the file has 134 positive and 64 negative records.
  - `hospital`: centre identifier; observed centres are GUY, IGR, JRH, KAR, and RH. Use only for a centre check, not as a shortlist feature.
  - `grade`: ordinal tumour grade, 1–3; the transcript states two records are missing.
  - `age`: accompanying patient clinical covariate.
  - `tumor_size_cm`: accompanying tumour-size clinical covariate.
  - 1,003 gene columns: continuous gene-expression measurements described in the transcript as cleaned log2 expression values. Relevant named genes include `ESR1`, `GATA3`, `FOXA1`, and `GREB1`.
- Covariates for the intended comparison: expression genes, beginning with `ESR1`; a possible small signature uses biologically nominated oestrogen-programme genes such as `GATA3`, `FOXA1`, and `GREB1`.
- Batch identifier: none is supplied in the file/brief. `hospital` is the available centre identifier and must remain a check rather than a predictor.

## Metric and baseline

The primary task is ranking likely ER-positive tumours and selecting an explainable ESR1 cut-off. Evaluate classification/ranking against `er_status`, using the counts above and below the cut-off and a clearly stated metric appropriate to the agreed review capacity. The transcript does not specify the number of review slots, the error trade-off, or the numerical borderline margin, so those operational choices must be recorded before calling a shortlist clinical.

**Baseline to beat:** predict `ER-positive` for every tumour: 134 correct out of 198, approximately 68%. No ESR1 or multi-gene result is trusted unless it is checked against and shown to improve on this majority-class baseline under the chosen evaluation procedure.

There is no supplied held-out set, independent pathology read, external validation cohort, or other truth source; `er_status` is the only reference label available.

## Done means

- Audit the file structure, labels, missingness, duplicate IDs/rows, expression range, outliers, and `ESR1` presence/validity without silently deleting questionable records.
- Report transcript-specified unavailable provenance items—Affymetrix probe-to-ESR1 mapping, batch/processing history, collection dates, and filtering/sampling criteria—as `unknown / not supplied` in the final output; do not infer them or leave them unmentioned.
- Rank all usable tumours by `ESR1` expression.
- Give one simple, explainable ESR1 cut-off and report ER-positive/ER-negative counts on each side.
- Compare ESR1 with the explicit majority-class baseline and state whether it improves it.
- Assess whether adding the small, explainable oestrogen-programme signature genuinely improves the ranked shortlist over ESR1 alone, without using hospital or tumour size to determine inclusion.
- Check whether the pattern is broadly similar across hospitals.
- Produce outputs under `results/`, including a tumour-board-ready table with: rank, tumour ID, ESR1 expression, suggested group, and borderline flag, plus the cut-off, side counts, centre check, baseline comparison, and limitations.
- If review capacity, error priority, or borderline rule remains unspecified, label the operational shortlist as unresolved rather than inventing those choices.

## Main trap

The most likely hidden trap is **confounding or technical/centre structure masquerading as ER biology**: the cohort is multi-centre, while batch, processing, probe-mapping, provenance, and dropped-reading details are not supplied. Independently, with only 198 tumours and 1,003 candidate genes, a broader model using many or all genes is at serious risk of overfitting or appearing to separate the classes well without genuine signal. A high apparent ESR1/signature result may also look impressive because it is evaluated on the same labelled data used to choose the cut-off or signature. Check centre consistency, keep hospital out of the decision, and require any broader-signature result to beat ESR1 alone under proper held-out cross-validation, as well as the honest baseline, before trusting it.
