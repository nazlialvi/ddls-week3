# ER-status validation dashboard

A small FastAPI + Tailwind CDN dashboard that reads `results/results.json` from disk. It uses no database and exposes the same data through `/api/results`.

## Run

From this folder:

```bash
uv run uvicorn app:app --host 0.0.0.0 --port 8001
```

Open http://localhost:8001.

The app displays the trustworthy ESR1 headline result beside its majority-class baseline, the gene shortlist and scores, a signed contribution heatmap, the hospital chi-square trap check, and the biological/measurement caveat. `requirements.txt` lists the runtime packages.
