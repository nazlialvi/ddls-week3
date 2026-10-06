# Operating instructions

## Environment

- Use `uv` for Python. Create the environment with `uv venv` when needed.
- Run all Python commands with `uv run python ...`; this is the cross-platform command for this project.
- Keep analysis reproducible and do not infer values that are not present in the supplied files.

## Data

- The data are in `data/expression.csv`.
- Load the CSV as one row per tumour and use its header as the source of truth for column names and meanings.
- The file currently shows 198 data rows and 1,009 columns: `sample_id`, `er_status`, `hospital`, `grade`, `age`, `tumor_size_cm`, and 1,003 gene-expression columns.
- Gene-expression fields are continuous values described in the transcript as cleaned log2 expression values. The clinical label is `er_status`; `hospital` is the centre identifier/check, not a decision feature. `grade`, `age`, and `tumor_size_cm` are accompanying clinical fields.
- Relevant gene columns include `ESR1`, `GATA3`, `FOXA1`, and `GREB1`.

## Outputs

- Write generated results and reports under `results/`. Do not overwrite source data.

## Trust rule

Every number reported must be checked against an honest baseline before it is trusted. For this task, the explicit baseline is calling every tumour `ER-positive` (134/198, about 68%), because ER-positive is the larger class. Report whether any ESR1 or broader-signature result actually improves on that baseline; do not present an unvalidated number as evidence.
