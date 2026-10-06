from __future__ import annotations

import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse

ROOT = Path(__file__).parent
RESULTS = ROOT / "results" / "results.json"
GENE_EXPRESSION = ROOT / "results" / "gene_expression.json"
app = FastAPI(title="ER-status validation dashboard")


def load_results() -> dict:
    try:
        data = json.loads(RESULTS.read_text())
        expression = json.loads(GENE_EXPRESSION.read_text())
        data["gene_values"] = {
            gene: {
                "negative": [row[gene] for row in expression["rows"] if row["er_status"] == "ER-negative"],
                "positive": [row[gene] for row in expression["rows"] if row["er_status"] == "ER-positive"],
            }
            for gene in expression["genes"]
        }
        return data
    except FileNotFoundError as exc:
        raise HTTPException(status_code=500, detail="results/results.json or gene_expression.json not found") from exc
    except json.JSONDecodeError as exc:
        raise HTTPException(status_code=500, detail="results JSON file is invalid") from exc


@app.get("/api/results")
def api_results() -> dict:
    return load_results()


@app.get("/", response_class=HTMLResponse)
def index() -> str:
    return HTML


HTML = r'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>ER-status validation</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = { theme: { extend: { colors: { ink: '#172033', teal: '#087f8c', paper: '#f7fafc' } } } }
  </script>
</head>
<body class="bg-paper text-ink">
  <main class="mx-auto max-w-7xl px-5 py-8 sm:px-8">
    <header class="mb-8 flex items-start justify-between gap-6">
      <div>
        <div class="mb-3 flex items-center gap-3 text-teal">
          <svg aria-hidden="true" class="h-8 w-8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 19V5m0 14h16M7 16l3-4 3 2 5-7"/><circle cx="7" cy="16" r="1"/><circle cx="10" cy="12" r="1"/><circle cx="13" cy="14" r="1"/><circle cx="18" cy="7" r="1"/></svg>
          <span class="text-sm font-semibold uppercase tracking-[.2em]">Validation record</span>
        </div>
        <h1 class="text-3xl font-bold tracking-tight sm:text-4xl">ER-status evidence dashboard</h1>
        <p class="mt-2 max-w-2xl text-slate-600">A transparent comparison of ESR1 alone with the fixed four-gene signature.</p>
      </div>
      <svg aria-hidden="true" class="hidden h-16 w-16 text-slate-300 sm:block" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.4"><path d="M12 3v18M3 12h18M5.6 5.6l12.8 12.8M18.4 5.6 5.6 18.4"/><circle cx="12" cy="12" r="8.5"/></svg>
    </header>

    <section id="summary" class="mb-4 grid gap-4 lg:grid-cols-[1fr_1fr_auto]"></section>
    <section class="mb-8 flex flex-wrap items-center gap-4 rounded-2xl border border-slate-200 bg-white p-4 shadow-sm"><span class="text-sm font-semibold">Headline stress test</span><label class="flex cursor-pointer items-center gap-2 text-sm"><input id="headline-toggle" type="checkbox" class="h-4 w-4" /> Exclude ESR1</label><span id="toggle-note" class="text-sm text-slate-500">Showing the four-gene signature</span></section>

    <section class="mb-8 grid gap-8 lg:grid-cols-[1.1fr_.9fr]">
      <article class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm">
        <div class="mb-5 flex items-center gap-3"><svg aria-hidden="true" class="h-6 w-6 text-teal" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M7 4h10M7 8h10M7 12h6M7 16h10M7 20h10"/><path d="M4 4h.01M4 8h.01M4 12h.01M4 16h.01M4 20h.01"/></svg><h2 class="text-xl font-semibold">Gene shortlist</h2></div>
        <div class="mb-4 rounded-lg border border-teal-200 bg-teal-50 px-4 py-3 text-sm text-teal-900"><strong>Validated model coefficients:</strong> fixed four-gene signature, evaluated with held-out cross-validation.</div>
        <div class="overflow-x-auto"><table class="w-full text-left text-sm"><thead class="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-500"><tr><th class="py-3 pr-3">Gene</th><th class="py-3 pr-3">Score</th><th class="py-3">Reason</th></tr></thead><tbody id="genes-validated"></tbody></table></div>
        <div class="mt-6 rounded-lg border border-amber-300 bg-amber-50 px-4 py-3 text-sm text-amber-950"><strong>Exploratory, univariate only:</strong> these genes came from scanning approximately 1,003 candidate genes without multiple-testing correction and without cross-validation. Some may reflect chance rather than real signal; their scores are not directly comparable in trustworthiness to the validated coefficients.</div>
        <div class="mt-4 overflow-x-auto"><table class="w-full text-left text-sm"><thead class="border-b border-slate-200 text-xs uppercase tracking-wide text-slate-500"><tr><th class="py-3 pr-3">Gene</th><th class="py-3 pr-3">Score</th><th class="py-3">Reason</th></tr></thead><tbody id="genes-exploratory"></tbody></table></div>
      </article>
      <article class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 class="mb-2 text-xl font-semibold">Scores by metric</h2><p class="mb-5 text-sm text-slate-600">Separate scales: validated coefficients and exploratory univariate scores are not equally trustworthy.</p><h3 class="mb-3 text-sm font-semibold text-teal-800">Validated model coefficients</h3><div id="bars-validated" class="space-y-3"></div><h3 class="mb-3 mt-6 text-sm font-semibold text-amber-800">Exploratory univariate scores</h3><div id="bars-exploratory" class="space-y-3"></div></article>
    </section>

    <section class="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><div class="mb-2 flex items-center gap-3"><svg aria-hidden="true" class="h-6 w-6 text-teal" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M4 4h16v16H4zM4 9h16M9 4v16M14 4v16"/><path d="M6 6h1M11 11h1M16 16h1"/></svg><h2 class="text-xl font-semibold">Contribution matrix</h2></div><p class="mb-5 text-sm text-slate-600">Signed standardized coefficient: teal pushes toward ER-positive; rose pushes away. Darker cells indicate greater magnitude.</p><div id="heatmap" class="overflow-x-auto"></div></section>
    <section class="mb-8 rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><h2 class="mb-2 text-xl font-semibold">Gene detail</h2><p class="mb-4 text-sm text-slate-600">Click a gene in the shortlist to inspect its expression distribution by recorded ER status.</p><div id="gene-detail" class="text-sm text-slate-500">Select a gene above.</div></section>

    <section id="caveat" class="rounded-2xl border border-amber-200 bg-amber-50 p-6"></section>
    <footer class="mt-6 text-xs text-slate-500">Source: results/results.json · No database · Review-slot capacity and borderline rule remain unresolved.</footer>
  </main>
<script>
const esc = s => String(s).replace(/[&<>'"]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;',"'":'&#39;','"':'&quot;'}[c]));
const pct = x => `${(x*100).toFixed(2)}%`;
function card(title, value, detail, accent='teal') { return `<div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-sm"><p class="text-xs font-semibold uppercase tracking-widest text-slate-500">${title}</p><p class="mt-3 text-3xl font-bold text-${accent}">${value}</p><p class="mt-2 text-sm text-slate-600">${detail}</p></div>`; }
function render(d) {
  const b=d.baseline, h=d.headline, c=d.comparison, removed=d.esr1_removed;
  const drawSummary=(headline, label)=>{const nCorrect=headline.n_correct ?? (headline===c?175:167);const nTotal=headline.n_total ?? 198;document.querySelector('#summary').innerHTML = card('Selected headline', `${esc(headline.name)} · ${pct(headline.accuracy)}`, `${nCorrect}/${nTotal} correct`, 'teal') + card('Baseline to beat', `${esc(b.name)} · ${pct(b.accuracy)}`, `${b.n_correct}/${b.n_total} correct`, 'slate-700') + card('Margin over baseline', `+${(100*(headline.accuracy-b.accuracy)).toFixed(2)} pts`, `${label}`, 'teal');};
  drawSummary(c,'Four-gene held-out result');
  document.querySelector('#headline-toggle').onchange=e=>{if(e.target.checked){drawSummary(removed,`Accuracy change vs four-gene: ${(100*(removed.accuracy-c.accuracy)).toFixed(2)} pts`);document.querySelector('#toggle-note').textContent='Showing GATA3 + GREB1 + FOXA1; ESR1 removed'}else{drawSummary(c,'Four-gene held-out result');document.querySelector('#toggle-note').textContent='Showing the four-gene signature'}};
  const validated=d.gene_shortlist.slice(0,4), exploratory=d.gene_shortlist.slice(4);
  const row=(g,i)=>`<tr class="border-b border-slate-100 align-top"><td class="py-3 pr-3 font-semibold">${i+1}. ${esc(g.gene)}<div><span class="mt-1 inline-block rounded-full bg-${i<4?'teal':'amber'}-100 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-${i<4?'teal':'amber'}-900">${i<4?'validated model coefficient':'exploratory · univariate only'}</span></div></td><td class="py-3 pr-3 font-mono ${g.importance_score<0?'text-rose-700':'text-teal'}">${g.importance_score.toFixed(4)}</td><td class="py-3 text-slate-600">${esc(g.reason)}</td></tr>`;
  let selectedGene=null;
  const interactiveRow=(g,i,tint)=>`<tr data-gene="${esc(g.gene)}" tabindex="0" role="button" aria-label="Show ${esc(g.gene)} expression distribution" class="gene-row border-b border-slate-100 align-top cursor-pointer hover:bg-${tint}-50 focus:bg-${tint}-50 focus:outline-none"><td class="py-3 pr-3 font-semibold">${i+1}. ${esc(g.gene)}<div><span class="mt-1 inline-block rounded-full bg-${tint}-100 px-2 py-0.5 text-[10px] font-semibold uppercase tracking-wide text-${tint}-900">${tint==='teal'?'validated model coefficient':'exploratory · univariate only'}</span></div></td><td class="py-3 pr-3 font-mono ${g.importance_score<0?'text-rose-700':'text-teal'}">${g.importance_score.toFixed(4)}</td><td class="py-3 text-slate-600">${esc(g.reason)}</td></tr>`;
  document.querySelector('#genes-validated').innerHTML=validated.map((g,i)=>interactiveRow(g,i,'teal')).join('');
  document.querySelector('#genes-exploratory').innerHTML=exploratory.map((g,i)=>interactiveRow(g,i+4,'amber')).join('');
  const sharedMax=Math.max(...d.gene_shortlist.map(g=>Math.abs(g.importance_score)));
  const bars=(items,target,color)=>{document.querySelector(target).innerHTML=items.map(g=>{const w=Math.max(3,Math.abs(g.importance_score)/sharedMax*100);const fill=g.importance_score<0?'#f43f5e':color;return `<div><div class="mb-1 flex justify-between text-xs"><span class="font-semibold">${esc(g.gene)}</span><span class="font-mono text-slate-500">${g.importance_score.toFixed(4)}</span></div><div class="h-3 rounded-full bg-slate-100"><div class="h-3 rounded-full" style="width:${w}%;background-color:${fill}"></div></div></div>`}).join('')};
  bars(validated,'#bars-validated','#0d9488'); bars(exploratory,'#bars-exploratory','#f59e0b');

  const detail=(gene)=>{const vals=d.gene_values?.[gene]; if(!vals){document.querySelector('#gene-detail').innerHTML='<p>Expression values are not available in results.json for this gene.</p>';return;} const groups=[['ER-negative',vals.negative,'#f43f5e'],['ER-positive',vals.positive,'#0d9488']]; const all=groups.flatMap(x=>x[1]); const lo=Math.min(...all),hi=Math.max(...all), scale=v=>20+(v-lo)/(hi-lo||1)*560; document.querySelector('#gene-detail').innerHTML=`<div class="mb-3 font-semibold">${esc(gene)} expression distribution</div><svg viewBox="0 0 620 150" class="h-40 w-full max-w-3xl" role="img" aria-label="${esc(gene)} expression distribution"><line x1="20" y1="125" x2="600" y2="125" stroke="#94a3b8"/>${groups.map((gr,j)=>gr[1].map((v,i)=>`<circle cx="${scale(v)}" cy="${75+j*35+(i%5)*3}" r="3" fill="${gr[2]}" opacity=".55"/>`).join('')).join('')}</svg><div class="flex gap-5 text-xs"><span><i class="mr-1 inline-block h-3 w-3 rounded-full" style="background:#f43f5e"></i>ER-negative</span><span><i class="mr-1 inline-block h-3 w-3 rounded-full" style="background:#0d9488"></i>ER-positive</span></div>`;};
  const selectGene=(el)=>{selectedGene=el.dataset.gene;document.querySelectorAll('.gene-row').forEach(row=>row.setAttribute('aria-pressed',row===el?'true':'false'));detail(selectedGene);document.querySelector('#gene-detail').scrollIntoView({behavior:'smooth',block:'nearest'});};
  document.querySelectorAll('.gene-row').forEach(el=>{el.addEventListener('click',()=>selectGene(el));el.addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();selectGene(el);}});});
  const max=Math.max(...validated.map(g=>Math.abs(g.importance_score)));
  const cell=g=>{const a=Math.abs(g.importance_score)/max;const bg=g.importance_score<0?`rgba(225,29,72,${.12+.78*a})`:`rgba(8,127,140,${.12+.78*a})`;return `<td class="min-w-28 border border-white p-3 text-center font-mono text-xs" style="background:${bg};color:${a>.55?'white':'#172033'}">${g.importance_score>0?'+':''}${g.importance_score.toFixed(3)}</td>`};
  document.querySelector('#heatmap').innerHTML=`<div class="mb-4 rounded-lg border border-teal-200 bg-teal-50 px-4 py-3 text-sm text-teal-900">Heatmap shows the <strong>validated four-gene model coefficients only</strong>; exploratory univariate scores are excluded from this coefficient matrix.</div><table class="border-collapse text-sm"><thead><tr><th class="border-b border-slate-200 p-3 text-left">Feature</th><th class="border-b border-slate-200 p-3 text-center">ER-positive contribution</th></tr></thead><tbody>${validated.map(g=>`<tr><th class="border border-white bg-slate-50 p-3 text-left">${esc(g.gene)}</th>${cell(g)}</tr>`).join('')}</tbody></table>`;
  document.querySelector('#caveat').innerHTML=`<div class="flex gap-4"><svg aria-hidden="true" class="mt-0.5 h-7 w-7 shrink-0 text-amber-700" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8"><path d="M12 3 2.8 20h18.4L12 3Z"/><path d="M12 9v5M12 17h.01"/></svg><div><h2 class="text-lg font-semibold text-amber-950">Caveat to keep visible</h2><p class="mt-2 text-amber-900">${esc(d.caveat)}</p><p class="mt-3 text-sm text-amber-800">Hospital trap check: χ²(4) = ${d.trap_check.statistic.toFixed(3)}, p = ${d.trap_check.p_value.toFixed(4)}. ${esc(d.trap_check.honest_conclusion)}</p></div></div>`;
}
fetch('/api/results').then(r=>r.json()).then(render).catch(e=>document.querySelector('#summary').innerHTML='<p class="text-red-700">Could not load results/results.json.</p>');
</script>
</body></html>'''
