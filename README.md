# Analytics portfolio — 9 projects, one repo

I picked business questions a BA would actually get paid for, found public
datasets, and carried each one to a decision with a number attached. Not
notebooks-to-nobody. Each folder is a finished piece: analysis, model if it
needs one, a dashboard you can open, SQL, and a writeup with the numbers I
checked twice.

## What's in each project

- `src/` — numbered scripts. 00 downloads the public data, 01–02 analysis/model,
  03–04 the brief and the dashboard, 05 the banner image, 06 the chatbot.
- `dashboard/index.html` — opens by double click, has an export-PDF button,
  and shows the same numbers the README shows.
- `outputs/` — kpis.json and the segment CSVs / charts the scripts produce.
- `assets/` — screenshots taken from real runs (how: `tools/capture.py`).
- `sql/` — the query layer (`analysis.sql` per project).

## Why every project has a chatbot (src/06_chat.py)

I wanted something I could open in front of a hiring manager and interrogate
live: "which agency is slowest?", "what conversion do we get in the top
decile?". The chat answers by recomputing from the csv at question time. The
rule I hold myself to: python computes, the LLM (if I give it a key) only
narrates numbers python already produced, and with no key at all you get the
same answers from a deterministic path. The chatbot screenshots in the
READMEs are its actual output, captured in `tools/`.

## Projects

| # | Folder | Question | One number I keep citing |
|---|---|---|---|
| 01 | [consulting/churn](projects/01-consulting-churn) | who do we pay to keep, and is retention worth it | 26.5% churn, $139k MRR at risk, modeled AUC 0.84 |
| 02 | [operations/311](projects/02-operations-311) | where does service time go in a city agency | 25.3% of a quarter's 150k cases miss the 72h SLA |
| 03 | [retail/supply chain](projects/03-supplychain-retail) | hedge SKU concentration or push exports | top-20 SKUs = 13.7% of revenue; returns = 9.2% |
| 04 | [finance](projects/04-finance-portfolio) | can a client actually hold their plan through drawdowns | avg 9.5 years underwater after a top-10 crash |
| 05 | [marketing](projects/05-marketing-campaign) | who do we call next | top decile: 10% of contacts, 61% of conversions |
| 06 | [engineering analytics](projects/06-software-delivery) | what slows issue flow in a real tracker | median 0.9d vs p90 10.9d cycle time |
| 07 | [AI review classification](projects/07-ai-review-intelligence) | can a GenAI classifier beat a $0 baseline | baseline 80.1% vs lexicon lane 61.3%, so the baseline ships |
| 08 | [jobs market](projects/08-technology-jobs) | what does the DS job market pay and why | US median $135k; remote +16%; senior 2.4x entry |
| 09 | [people analytics](projects/09-management-attrition) | which levers predict attrition | overtime 30.5% vs 10.4%; first two years 29.8% |

Each project also lives as its own repo, same code and same history, if you
don't want the whole bundle:
[churn-retention-analysis](https://github.com/NitishPoosarla/churn-retention-analysis) ·
[nyc-311-response-times](https://github.com/NitishPoosarla/nyc-311-response-times) ·
[retail-supply-chain](https://github.com/NitishPoosarla/retail-supply-chain) ·
[equity-drawdown-analysis](https://github.com/NitishPoosarla/equity-drawdown-analysis) ·
[campaign-response-model](https://github.com/NitishPoosarla/campaign-response-model) ·
[delivery-cycle-times](https://github.com/NitishPoosarla/delivery-cycle-times) ·
[review-intelligence](https://github.com/NitishPoosarla/review-intelligence) ·
[tech-jobs-salaries](https://github.com/NitishPoosarla/tech-jobs-salaries) ·
[employee-attrition](https://github.com/NitishPoosarla/employee-attrition)

## Running one

```bash
cd projects/01-consulting-churn   # in a standalone repo: skip the cd, you're already at the root
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python src/00_download_data.py    # script names vary slightly per project
.venv/bin/python src/01_prepare_analysis.py
.venv/bin/python src/06_chat.py             # try it: "churn by contract"
```

If you add `GROQ_API_KEY` to `.env`, scripts 03 and 06 route their narration
through the LLM in free tier mode; without it, both work offline.

## Caveats I keep attached to the work

Public data, public snapshots, so these are directional reads on realistic
problems, not client deliverables, and I say so in every README. Assumptions
that aren't computable (call cost, margins, staff rates) are labeled in the
outputs. Project 07's LLM lane ran in lexicon-fallback mode for this build;
the eval receipt records that explicitly.

Built in Python (pandas, sklearn, matplotlib), 2026.
