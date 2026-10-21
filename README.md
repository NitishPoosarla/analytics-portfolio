# Business-Analytics × AI Portfolio — 9 Full Decision Projects

<!-- portfolio-hub-tl;dr -->
> **Every project here answers one real business question end-to-end** — data →
> analysis → model → costed scenario → interactive dashboard → **an AI chatbot
> that computes its answers live from the data** → verified numbered README with
> real screenshots. Python computes and verifies every number; AI explains and
> frames, and structurally cannot invent a KPI.

## The AI-native analytics stack (consistent across all 9)

| Layer | What ships | The rule |
|---|---|---|
| **Analysis** | deterministic Python (`01_analysis` / `02_model`, numpy·pandas·sklearn) | every metric recomputable from the raw download in one rerun |
| **AI narration** | `03_ai_*.py` — an LLM that **receives only verified numbers** and narrates the decision | never computes, never invents; offline fallback engine without a key |
| **Ask-the-data chatbot** | `src/06_chat.py` — REPL + one-shot, answers with metrics computed live at question time | the screenshot in each README is verbatim output, not mock text |
| **Decision dashboard** | `dashboard/index.html` — single-file, CDN-free-shape, **PDF-export button** | opens by double-click; numbers match the README exactly |
| **Visuals** | `src/05_linkedin_hero.py` branded slide + `tools/capture.py` real-Chromium screenshots | reproducible capture, committed in `assets/` |

## The nine projects

| # | Project | Domain | The decision | Headline (verified) |
|---|---|---|---|---|
| 01 | [Telco churn → retention ROI](projects/01-consulting-churn) | Consulting | Who do we pay to keep, and is the program worth it? | 26.5% churn $139k MRR at risk; top-contract 42.7% churn; AUC 0.84; 1.8× program ROI |
| 02 | [NYC 311 service operations](projects/02-operations-311) | Operations | Where does service time go; which capacity fix pays? | 150k cases; 25.3% miss 72h SLA; Scenario A frees $527k/quarter |
| 03 | [Online retail supply chain](projects/03-supplychain-retail) | Retail/SCM | Concentrate risk: hedge SKUs or export push? | top-20 SKUs = 13.7% of revenue; returns 9.2%; UK = 84% |
| 04 | [S&P 500 drawdown math](projects/04-finance-portfolio) | Finance | Can the client actually hold their plan? | 9.0%/yr nominal but 9.5-yr avg underwater; real CAGR 2.5% |
| 05 | [Bank telemarketing targeting](projects/05-marketing-campaign) | Marketing | Who do we call next? Model-ranked deciles, not scripts | top decile: 10% of contacts → 61% of conversions; ROI 5.6× |
| 06 | [Delivery triage on 1,000 issues](projects/06-software-delivery) | Engineering analytics | What actually slows issue flow? | median 0.9d vs p90 10.9d; labels cut open age 38% |
| 07 | [Review intelligence with an eval receipt](projects/07-ai-review-intelligence) | AI/GenAI | Can a GenAI classifier beat a $0 baseline — proved? | baseline 80.1% vs LLM-lane 61.3% sampled — baseline ships, AI lane behind an eval gate |
| 08 | [AI job-market salaries](projects/08-technology-jobs) | Technology | What does the market pay, by lever? | global median $101.6k; US $135k; remote +16%; senior 2.4× junior |
| 09 | [Employee attrition watch-list](projects/09-management-attrition) | Management | Which levers predict leaving, who to engage first? | 16.1% attrition; OT 30.5% vs 10.4%; top-5 ranked 1:1 list |

Each project folder is self-contained: `README.md` (with hero + dashboard + chatbot screenshots), `src/` (00–04 + `05_linkedin_hero.py` + `06_chat.py`), `dashboard/index.html`, `outputs/` (verified KPIs, segments, charts), `sql/`, `data/`, `linkedin_post.md`.

## How to run any project

```bash
cd projects/01-consulting-churn        # or any of the 9
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/00_download_data.py      # pulls the public dataset
.venv/bin/python src/01_prepare_analysis.py   # name differs slightly per project
.venv/bin/python src/03_ai_insights.py        # optional: GROQ_API_KEY in .env for LLM narration
.venv/bin/python src/06_chat.py               # ask the data anything it can compute
```

A shared build toolkit lives in [`tools/`](tools) — `capture.py` (real-Chromium screenshots of every dashboard and chatbot session) and `patch_readme.py` (README visual embeds). The "screenshots" are reproducible, not hidden dev magic.

## The hiring pitch, in one paragraph

These are not "I made a notebook" projects. Each one prices a decision: a retention budget with stated assumptions and a ranked save-list; a capacity redeployment with a $ number per quarter; a sourcing hedge costed against an outage; drawdown math that survives client meetings. Every wall has a chatbot on it: ask *the data* in natural language and get **computed** answers — the same pattern analysts are now being hired for, minus the hallucination risk, because the LLM here is structurally incapable of inventing a number.

## Honest limitations

- Public datasets → findings are directional decision-support on realistic business problems, not company-specific causal claims.
- Project 07's LLM lane was run in its free lexicon-fallback mode (no API key in the build environment); the full API-key mode re-runs `02_llm_classifier.py` and the eval receipt on request — clearly labeled in the output.
- LLM narration in `03_*`/`06_*` scripts is one documented request away (`GROQ_API_KEY` in `.env`); the deterministic engines shown run fully offline.

*Built 2026 · 9 projects · 2 per week pace, ~one repo that reads like an analyst's first quarter.*
