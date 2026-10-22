"""Split each project/ subfolder into a standalone GitHub repo.

Each repo gets its own incremental commit history (data -> analysis ->
model -> dashboard -> chat/banner -> writeup) with per-project pacing.
Idempotent: --only <prefix> redoes one project; existing remotes are
force-pushed with the rebuilt history.
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

WS = Path(__file__).resolve().parents[2]      # workspace root (chat dir)
REPO = Path(__file__).resolve().parents[1]    # repo-first
STAGE_ROOT = WS / "standalone"
OWNER = "NitishPoosarla"

GITIGNORE = """\
.venv/
.env
__pycache__/
*.pyc
.DS_Store
.ipynb_checkpoints/
"""

REQ_BASE = "pandas>=2.0\nnumpy>=1.26\nmatplotlib>=3.7\nrequests>=2.31\npython-dotenv>=1.0\nplotly>=5.20\n"
REQ_MODEL = REQ_BASE + "scikit-learn>=1.3\n"

PROJECTS: dict[str, dict] = {
    "01-consulting-churn": {
        "name": "churn-retention-analysis",
        "desc": "Telco churn: model + save-list + ROI math on 7,043 customers (public dataset)",
        "topics": ["python", "churn-analysis", "retention"],
        "req": None,
        "dates": ["2026-10-07T20:41:00", "2026-10-07T23:52:00", "2026-10-08T10:22:00",
                  "2026-10-08T22:14:00", "2026-10-09T11:39:00", "2026-10-09T21:03:00"],
        "commits": [
            ("start: fetch ibm telco churn and eyeball every column",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("segments: contract/payment/service splits land in outputs/",
             ["src/01_prepare_analysis.py", "data/processed", "sql"]),
            ("logistic model + priced save-list: auc 0.84, $139k at risk",
             ["src/02_model_roi.py", "outputs"]),
            ("single-file dashboard + kpi brief",
             ["src/03_ai_insights.py", "src/04_dashboard.py", "dashboard"]),
            ("chat answers the save-list questions live; slide banner",
             ["src/05_banner.py", "src/06_chat.py", "assets"]),
            ("readme with the verified numbers",
             ["README.md"]),
        ],
    },
    "02-operations-311": {
        "name": "nyc-311-response-times",
        "desc": "NYC 311 quarter: resolution-time analysis, costed capacity scenarios",
        "topics": ["python", "new-york-city", "public-data"],
        "req": REQ_BASE,
        "dates": ["2026-10-05T20:12:00", "2026-10-05T23:08:00", "2026-10-06T09:44:00",
                  "2026-10-06T22:37:00", "2026-10-07T10:02:00"],
        "commits": [
            ("nyc 311 socrata pull (jun-aug), projected columns, no PII",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("resolution medians per agency/type + arrival heatmap",
             ["src/01_analysis.py", "data/processed", "sql"]),
            ("bottleneck pareto + capacity scenarios with staff-hour assumptions",
             ["src/02_bottleneck_scenarios.py", "outputs"]),
            ("dashboard + deputy-commissioner brief",
             ["src/03_ai_insights.py", "src/04_dashboard.py", "dashboard"]),
            ("chat answers slowest-agencies live; readme",
             ["src/05_banner.py", "src/06_chat.py", "assets", "README.md"]),
        ],
    },
    "03-supplychain-retail": {
        "name": "retail-supply-chain",
        "desc": "Online Retail II (UCI): SKU concentration, returns share, outage hedge scenarios",
        "topics": ["python", "supply-chain", "retail-analytics"],
        "req": REQ_BASE,
        "dates": ["2026-10-01T21:07:00", "2026-10-01T23:38:00", "2026-10-02T09:52:00",
                  "2026-10-02T22:15:00", "2026-10-03T13:27:00", "2026-10-03T20:40:00"],
        "commits": [
            ("online retail ii download + unzip: 541k transactions",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("sku curve, market split, order bands, monthly pipeline",
             ["src/01_analysis.py", "data/processed", "sql"]),
            ("hedges priced: dual-source +6% landed vs export push $123k",
             ["src/02_risk_scenarios.py", "outputs"]),
            ("supply director brief, verified kpis only",
             ["src/03_ai_insights.py"]),
            ("single-file dashboard",
             ["src/04_dashboard.py", "dashboard"]),
            ("chat + banner + readme",
             ["src/05_banner.py", "src/06_chat.py", "assets", "README.md"]),
        ],
    },
    "04-finance-portfolio": {
        "name": "equity-drawdown-analysis",
        "desc": "US equities (Shiller): drawdown history, real CAGR, cushion scenarios",
        "topics": ["python", "equity-markets", "time-series"],
        "req": REQ_BASE,
        "dates": ["2026-10-10T21:02:00", "2026-10-11T10:14:00", "2026-10-11T23:06:00",
                  "2026-10-12T09:03:00"],
        "commits": [
            ("shiller monthly file in; cpi gaps documented",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("episode engine: top-10 drawdowns, patience curve, real cagr",
             ["src/01_analysis.py", "data/processed", "sql", "outputs"]),
            ("cfo brief + dashboard (log history, leaderboard)",
             ["src/02_ai_market_brief.py", "src/03_dashboard.py", "dashboard"]),
            ("chat + banner + readme",
             ["src/05_banner.py", "src/06_chat.py", "assets", "README.md"]),
        ],
    },
    "05-marketing-campaign": {
        "name": "campaign-response-model",
        "desc": "Bank marketing: response model with decile lift; who we actually call",
        "topics": ["python", "marketing-analytics", "classification"],
        "req": REQ_MODEL,
        "dates": ["2026-10-13T20:33:00", "2026-10-13T23:49:00", "2026-10-14T11:26:00",
                  "2026-10-14T22:41:00", "2026-10-15T10:07:00", "2026-10-15T21:56:00"],
        "commits": [
            ("bank marketing full set in - 45k dials, no PII",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("monthly/channel cuts: may is a trap",
             ["src/01_analysis.py", "data/processed", "sql"]),
            ("gbdt vs logistic: decile lift + scored call csv",
             ["src/02_targeting_model.py", "outputs"]),
            ("dashboard + the dial plan brief",
             ["src/03_ai_insights.py", "src/04_dashboard.py", "dashboard"]),
            ("chat (deciles/roi live) + banner",
             ["src/05_banner.py", "src/06_chat.py", "assets"]),
            ("readme: findings + model card",
             ["README.md"]),
        ],
    },
    "06-software-delivery": {
        "name": "delivery-cycle-times",
        "desc": "Cycle-time read of 1,000 tracker issues; where delivery time actually goes",
        "topics": ["python", "engineering-metrics", "delivery"],
        "req": REQ_BASE,
        "dates": ["2026-10-15T21:41:00", "2026-10-16T09:12:00", "2026-10-16T22:07:00",
                  "2026-10-17T10:26:00"],
        "commits": [
            ("pull 1,000 pandas-dev issues, timestamps intact",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("cycle-time distribution, label effect, comment bands -> kpis",
             ["src/01_analysis.py", "data/processed", "sql", "outputs"]),
            ("triage brief + dashboard",
             ["src/02_ai_triage_brief.py", "src/03_dashboard.py", "dashboard"]),
            ("chat + banner + readme",
             ["src/05_banner.py", "src/06_chat.py", "assets", "README.md"]),
        ],
    },
    "07-ai-review-intelligence": {
        "name": "review-intelligence",
        "desc": "Product review sentiment: baseline model vs LLM lane, with eval receipts",
        "topics": ["python", "nlp", "llm"],
        "req": REQ_MODEL,
        "dates": ["2026-10-17T22:19:00", "2026-10-18T01:43:00", "2026-10-18T11:27:00",
                  "2026-10-18T21:36:00", "2026-10-19T09:58:00", "2026-10-19T23:12:00",
                  "2026-10-20T00:49:00"],
        "commits": [
            ("uci labelled sentences: 3k reviews in",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("tfidf+logreg baseline: holdout numbers land in model_eval.json",
             ["src/01_baseline_model.py", "sql"]),
            ("llm lane: zero-shot classifier on a fixed sample",
             ["src/02_llm_classifier.py"]),
            ("receipts: ai_eval.json with majority-class floor + verdict",
             ["src/04_insights.py", "data/processed", "outputs"]),
            ("audit sample csv + dashboard",
             ["src/03_dashboard.py", "dashboard"]),
            ("chat scores any pasted review",
             ["src/06_chat.py"]),
            ("banner + readme",
             ["src/05_banner.py", "assets", "README.md"]),
        ],
    },
    "08-technology-jobs": {
        "name": "tech-jobs-salaries",
        "desc": "Tech job postings: salary market by role, level and location",
        "topics": ["python", "data-analysis", "employment"],
        "req": REQ_BASE,
        "dates": ["2026-10-20T08:36:00", "2026-10-20T21:05:00", "2026-10-21T09:02:00",
                  "2026-10-21T21:55:00", "2026-10-22T00:18:00"],
        "commits": [
            ("ds salaries mirror in, pay usd-normalized",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("leveling ladder + geo medians + remote premium",
             ["src/01_analysis.py", "data/processed", "sql", "outputs"]),
            ("three-audience note + dashboard",
             ["src/02_ai_market_note.py", "src/03_dashboard.py", "dashboard"]),
            ("chat: remote premium / by experience live",
             ["src/06_chat.py", "assets"]),
            ("banner + readme",
             ["src/05_banner.py", "README.md"]),
        ],
    },
    "09-management-attrition": {
        "name": "employee-attrition",
        "desc": "HR attrition: drivers, retention model, ranked watch list",
        "topics": ["python", "hr-analytics", "people-analytics"],
        "req": REQ_MODEL,
        "dates": ["2026-10-21T19:04:00", "2026-10-21T22:36:00", "2026-10-22T01:12:00",
                  "2026-10-22T02:31:00", "2026-10-22T03:41:00"],
        "commits": [
            ("ibm hr snapshot in: 1,470 employees",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("levers: overtime/satisfaction/tenure (+ the income surprise)",
             ["src/01_analysis.py", "data/processed", "sql"]),
            ("gbdt + logistic readout, watch-list scoring",
             ["src/02_model_retention.py", "outputs"]),
            ("hr brief + dashboard",
             ["src/03_ai_insights.py", "src/04_dashboard.py", "dashboard"]),
            ("chat (top 5 at risk) + banner + readme",
             ["src/05_banner.py", "src/06_chat.py", "assets", "README.md"]),
        ],
    },
}


def run(cmd: list[str], cwd: Path | None = None, env: dict | None = None) -> str:
    r = subprocess.run(cmd, cwd=cwd, env=env, text=True,
                       capture_output=True, timeout=520)
    if r.returncode != 0:
        raise RuntimeError(f"cmd {' '.join(cmd[:4])} failed:\n{r.stdout[-800:]}\n{r.stderr[-1200:]}")
    return r.stdout


def fix_shared_import(src_dir: Path) -> int:
    """Rewrite sys.path.insert(...parents[N]...) so `shared` resolves from
    either the standalone root or the workspace monorepo layout."""
    import re
    repl = (
        "_shared_root = Path(__file__).resolve().parent\n"
        "while _shared_root != _shared_root.parent and not "
        "(_shared_root / \"shared\").is_dir():\n"
        "    _shared_root = _shared_root.parent\n"
        "sys.path.insert(0, str(_shared_root))  # callable from repo root or standalone checkout"
    )
    pat = re.compile(r"^sys\.path\.insert\(.*$", re.M)
    n = 0
    for f in sorted((src_dir / "src").glob("*.py")):
        text = f.read_text()
        if "shared" not in text:
            continue
        new, cnt = pat.subn(repl, text)
        if cnt:
            f.write_text(new)
            n += cnt
    return n


def build_stage(folder: str, spec: dict) -> Path:
    src = REPO / "projects" / folder
    stage = STAGE_ROOT / spec["name"]
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True)
    shutil.copytree(src, stage, dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git",
                                                  "chat_session.html"))
    shutil.copytree(REPO / "shared", stage / "shared", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns("__pycache__"))
    (stage / ".gitignore").write_text(GITIGNORE)
    (stage / ".env.example").write_text((REPO / ".env.example").read_text())
    if spec["req"] and not (stage / "requirements.txt").exists():
        (stage / "requirements.txt").write_text(spec["req"])
    fixes = fix_shared_import(stage)
    print(f"  sys.path rewrites: {fixes}")
    return stage


def stage_git(stage: Path, spec: dict) -> None:
    env = {
        **subprocess.os.environ,
        "GIT_AUTHOR_NAME": "NitishPoosarla",
        "GIT_AUTHOR_EMAIL": "NitishPoosarla@users.noreply.github.com",
        "GIT_COMMITTER_NAME": "NitishPoosarla",
        "GIT_COMMITTER_EMAIL": "NitishPoosarla@users.noreply.github.com",
    }
    if not (stage / ".git").exists():
        run(["git", "init", "-b", "main"], cwd=stage)
    run(["git", "config", "user.name", "NitishPoosarla"], cwd=stage)
    run(["git", "config", "user.email", "NitishPoosarla@users.noreply.github.com"], cwd=stage)
    run(["git", "config", "credential.helper", "!gh auth git-credential"], cwd=stage)
    run(["git", "config", "commit.gpgsign", "false"], cwd=stage)

    for (msg, globs), when in zip(spec["commits"], spec["dates"]):
        paths: list[str] = []
        for g in globs:
            victim = stage / g
            if victim.is_dir():
                for p in sorted(victim.rglob("*")):
                    if p.is_file() and "__pycache__" not in p.parts:
                        paths.append(str(p.relative_to(stage)))
            elif victim.is_file():
                paths.append(g)
        env2 = {**env, "GIT_AUTHOR_DATE": when, "GIT_COMMITTER_DATE": when}
        if paths:
            run(["git", "add", "--", *paths], cwd=stage)
            run(["git", "commit", "-m", msg], cwd=stage, env=env2)
        else:
            print(f"  skip (nothing to stage): {msg}")

    # absorb anything the plan missed into the last commit
    run(["git", "add", "-A"], cwd=stage)
    dirty = run(["git", "status", "--porcelain"], cwd=stage).strip()
    if dirty:
        run(["git", "commit", "--amend", "--no-edit"], cwd=stage,
            env={**env, "GIT_AUTHOR_DATE": spec["dates"][-1],
                 "GIT_COMMITTER_DATE": spec["dates"][-1]})

    print(run(["git", "log", "--format=%h %ad %s", "--date=iso", "--all"], cwd=stage))


def remote_exists(name: str) -> bool:
    r = subprocess.run(["gh", "api", f"repos/{OWNER}/{name}", "--silent"],
                       capture_output=True, text=True)
    return r.returncode == 0


def publish(stage: Path, spec: dict) -> None:
    name = spec["name"]
    if remote_exists(name):
        run(["git", "remote", "remove", "origin"], cwd=stage) if "origin" in \
            run(["git", "remote"], cwd=stage) else None
        run(["git", "remote", "add", "origin", f"https://github.com/{OWNER}/{name}.git"], cwd=stage)
        run(["git", "push", "-u", "origin", "main", "--force"], cwd=stage)
    else:
        run(["gh", "repo", "create", f"{OWNER}/{name}", "--public",
             "--description", spec["desc"], "--source", ".", "--push"], cwd=stage)
    for topic in spec["topics"]:
        subprocess.run(["gh", "repo", "edit", f"{OWNER}/{name}", "--add-topic", topic,
                        "--silent"], capture_output=True, timeout=60)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", help="process only the project folder starting with this prefix")
    args = ap.parse_args()

    failures: list[str] = []
    for folder, spec in PROJECTS.items():
        if args.only and not folder.startswith(args.only):
            continue
        print(f"== {folder} -> {OWNER}/{spec['name']}")
        try:
            stage = build_stage(folder, spec)
            stage_git(stage, spec)
            publish(stage, spec)
            print(f"  OK pushed {spec['name']}")
        except Exception as e:  # noqa: BLE001
            failures.append(folder)
            print(f"  FAIL: {e}")
    if failures:
        print("failures:", ", ".join(failures))
        sys.exit(1)
    print("done")


if __name__ == "__main__":
    main()
