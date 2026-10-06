# Part 4 validation

## Baselines and model performance

- **Majority baseline:** predicting ER-positive for every tumour gives **134/198 = 67.68% accuracy**.
- **ESR1-alone baseline:** the held-out cross-validated ESR1 cut-off gives **174/198 = 87.88% accuracy**, an improvement of **20.20 percentage points** over the majority baseline.
- **Broader four-gene signature:** the held-out cross-validated model using `ESR1`, `GATA3`, `FOXA1`, and `GREB1` gives **175/198 = 88.38% accuracy**. This is **+20.71 points** over the majority baseline and only **+0.51 points** over ESR1 alone.

## Hospital trap check

The hospital × `er_status` chi-square test gives **χ²(4) = 8.277, p = 0.0820**. The observed differences, including JRH’s 11/24 ER-positive rate (45.8%), are not statistically distinguishable from chance at the conventional 0.05 level and remain consistent with sampling noise in a small hospital group. Hospital remains excluded from the feature set.

The signature result was scored using held-out cross-validation predictions, not training predictions. The small +0.51-point margin does not establish a meaningful advantage for the broader signature.

## Gene-set selection record

The four genes—`ESR1`, `GATA3`, `FOXA1`, and `GREB1`—were selected purely from the interview transcript’s biological/domain knowledge and were fixed before modelling. No data-driven search across the full 1,003-gene set was used to choose them, including no comparison of cross-validation accuracy across candidate gene sets. Therefore, no gene-set selection optimism from such a search is being added to the reported margin.

## Biological/measurement caveat

Clinical ER status and mRNA expression measure different biological layers, and their imperfect concordance could deflate the apparent margin—or limit how well this result generalizes to another assay or population. The transcript does not document the exact clinical assay, so it is not factual to assert that it was IHC. This mRNA–protein/assay discordance was not directly testable because no independent protein measurements or assay details are supplied.

The class imbalance is handled explicitly by comparing against the 67.68% majority baseline. The pre-selection history of the 1,003 genes is documented but cannot be quantified further from the supplied files.
