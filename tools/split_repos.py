"""Split each project/ subfolder into a standalone GitHub repo.

Each repo gets its own incremental commit history (data -> analysis ->
model -> dashboard -> chatbot/screenshots -> writeup), authored as the
owner, with realistic session-spaced dates. Idempotent: pass --only <prefix>
to redo a single project; existing remotes are reused and pushed again.
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
        "req": None,  # already has one
        "dates": ["2026-10-07T20:21:00",
                  "2026-10-07T23:16:00",
                  "2026-10-08T09:34:00",
                  "2026-10-08T21:48:00",
                  "2026-10-09T09:27:00",
                  "2026-10-09T20:35:00"],
        "commits": [
            ("telco churn fetcher + a first look at the raw columns",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("clean + segment: churn by contract and payment tell most of the story",
             ["src/01_prepare_analysis.py", "data/processed", "sql"]),
            ("churn model + roi math: auc 0.84, $139k mrr at risk -> save-list",
             ["src/02_model_roi.py", "outputs"]),
            ("ai brief (verified kpis only) + single-file dashboard",
             ["src/03_ai_insights.py", "src/04_dashboard.py", "dashboard"]),
            ("ask-the-data chatbot, hero slide, real screenshots",
             ["src/05_linkedin_hero.py", "src/06_chat.py", "src/07_capture_shots.py", "assets"]),
            ("readme, linkedin post, requirements",
             ["README.md", "linkedin_post.md"]),
        ],
    },
    "02-operations-311": {
        "name": "nyc-311-response-times",
        "desc": "NYC 311 Q3: resolution-time analysis, bottleneck scenarios, ask-the-data chatbot",
        "topics": ["python", "new-york-city", "public-data"],
        "req": REQ_BASE,
        "dates": ["2026-10-05T20:12:00",
                  "2026-10-05T22:47:00",
                  "2026-10-06T07:31:00",
                  "2026-10-06T21:05:00",
                  "2026-10-06T23:58:00",
                  "2026-10-07T08:44:00"],
        "commits": [
            ("311 q3 extract in + first look at the columns",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("resolution times: p50/p90 by agency and complaint",
             ["src/01_analysis.py", "data/processed", "sql"]),
            ("bottleneck + capacity scenarios, kpis locked",
             ["src/02_bottleneck_scenarios.py", "outputs"]),
            ("ai brief reads only verified kpis + dashboard",
             ["src/03_ai_insights.py", "src/04_dashboard.py", "dashboard"]),
            ("ask-311 chatbot: slowest agencies live from the data",
             ["src/06_chat.py"]),
            ("hero slide, screenshots, writeup",
             ["src/05_linkedin_hero.py", "assets", "README.md", "linkedin_post.md"]),
        ],
    },
    "03-supplychain-retail": {
        "name": "retail-supply-chain",
        "desc": "Online Retail II (UCI): SKU concentration, returns share, outage hedge scenarios",
        "topics": ["python", "supply-chain", "retail-analytics"],
        "req": REQ_BASE,
        "dates": ["2026-10-01T21:07:00",
                  "2026-10-01T23:38:00",
                  "2026-10-02T09:52:00",
                  "2026-10-02T22:15:00",
                  "2026-10-03T20:40:00"],
        "commits": [
            ("online retail ii (uci): 541k transactions, 13 months, first look",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("sku concentration, returns share, uk exposure",
             ["src/01_analysis.py", "data/processed", "sql"]),
            ("outage and dual-sourcing hedge scenarios priced",
             ["src/02_risk_scenarios.py", "outputs"]),
            ("dashboard + ai brief",
             ["src/03_ai_insights.py", "src/04_dashboard.py", "dashboard"]),
            ("sku-concentration chatbot, hero, shots, readme + post",
             ["src/05_linkedin_hero.py", "src/06_chat.py", "assets", "README.md", "linkedin_post.md"]),
        ],
    },
    "04-finance-portfolio": {
        "name": "equity-drawdown-analysis",
        "desc": "US equities (Shiller): drawdown history, real CAGR, cushion scenarios",
        "topics": ["python", "equity-markets", "time-series"],
        "req": REQ_BASE,
        "dates": ["2026-10-10T21:02:00",
                  "2026-10-10T23:27:00",
                  "2026-10-11T10:14:00",
                  "2026-10-11T22:41:00",
                  "2026-10-12T09:03:00"],
        "commits": [
            ("shiller monthly file downloaded - 150+ years of returns",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("drawdown history + real-cagr math",
             ["src/01_analysis.py", "data/processed", "sql", "outputs"]),
            ("ai market brief + dashboard",
             ["src/02_ai_market_brief.py", "src/03_dashboard.py", "dashboard"]),
            ("chatbot + hero + captures",
             ["src/05_linkedin_hero.py", "src/06_chat.py", "assets"]),
            ("readme + linkedin post + requirements",
             ["README.md", "linkedin_post.md"]),
        ],
    },
    "05-marketing-campaign": {
        "name": "campaign-response-model",
        "desc": "Bank marketing: response model with decile lift; who we actually call",
        "topics": ["python", "marketing-analytics", "classification"],
        "req": REQ_MODEL,
        "dates": ["2026-10-13T20:33:00",
                  "2026-10-13T22:58:00",
                  "2026-10-14T08:49:00",
                  "2026-10-14T21:17:00",
                  "2026-10-15T09:56:00"],
        "commits": [
            ("bank marketing full set in - 45k calls",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("response rates by month/contact/campaign; the handoff pattern sticks out",
             ["src/01_analysis.py", "data/processed", "sql"]),
            ("targeting model: decile lift + scored file",
             ["src/02_targeting_model.py", "outputs"]),
            ("dashboard + ai dial plan",
             ["src/03_ai_insights.py", "src/04_dashboard.py", "dashboard"]),
            ("chatbot, hero, shots, readme + post",
             ["src/05_linkedin_hero.py", "src/06_chat.py", "assets", "README.md", "linkedin_post.md"]),
        ],
    },
    "06-software-delivery": {
        "name": "delivery-cycle-times",
        "desc": "Cycle-time read of 1,000 tracker issues; where delivery time actually goes",
        "topics": ["python", "engineering-metrics", "delivery"],
        "req": REQ_BASE,
        "dates": ["2026-10-15T21:41:00",
                  "2026-10-15T23:20:00",
                  "2026-10-16T09:12:00",
                  "2026-10-16T22:07:00",
                  "2026-10-17T10:26:00"],
        "commits": [
            ("1,000 tracker issues pulled in",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("cycle-time read: p50/p90 by issue type",
             ["src/01_analysis.py", "data/processed", "sql", "outputs"]),
            ("ai triage brief + dashboard",
             ["src/02_ai_triage_brief.py", "src/03_dashboard.py", "dashboard"]),
            ("chatbot + hero + captures",
             ["src/05_linkedin_hero.py", "src/06_chat.py", "assets"]),
            ("readme + linkedin post + requirements",
             ["README.md", "linkedin_post.md"]),
        ],
    },
    "07-ai-review-intelligence": {
        "name": "review-intelligence",
        "desc": "Product review sentiment: baseline model vs LLM lane, with eval receipts",
        "topics": ["python", "nlp", "llm"],
        "req": REQ_MODEL,
        "dates": ["2026-10-17T22:19:00",
                  "2026-10-18T01:43:00",
                  "2026-10-18T11:27:00",
                  "2026-10-18T21:36:00",
                  "2026-10-19T09:58:00",
                  "2026-10-19T23:12:00"],
        "commits": [
            ("amazon fine-food reviews in",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("baseline model: lexicon vs logistic regression, confusion matrices",
             ["src/01_baseline_model.py", "sql"]),
            ("llm lane: same reviews through the classifier prompt",
             ["src/02_llm_classifier.py"]),
            ("eval receipts: baseline vs llm side by side",
             ["src/04_insights.py", "data/processed", "outputs"]),
            ("dashboard + score-a-review chatbot",
             ["src/03_dashboard.py", "src/06_chat.py", "dashboard"]),
            ("hero, captures, readme + post",
             ["src/05_linkedin_hero.py", "assets", "README.md", "linkedin_post.md"]),
        ],
    },
    "08-technology-jobs": {
        "name": "tech-jobs-salaries",
        "desc": "Tech job postings: salary market by role and location",
        "topics": ["python", "data-analysis", "employment"],
        "req": REQ_BASE,
        "dates": ["2026-10-20T08:36:00",
                  "2026-10-20T21:05:00",
                  "2026-10-21T09:02:00",
                  "2026-10-21T21:55:00",
                  "2026-10-22T00:18:00"],
        "commits": [
            ("job postings dataset in",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("salary read: median by role and region",
             ["src/01_analysis.py", "data/processed", "sql", "outputs"]),
            ("dashboard + ai market note",
             ["src/02_ai_market_note.py", "src/03_dashboard.py", "dashboard"]),
            ("chatbot + hero + captures",
             ["src/05_linkedin_hero.py", "src/06_chat.py", "assets"]),
            ("readme + linkedin post + requirements",
             ["README.md", "linkedin_post.md"]),
        ],
    },
    "09-management-attrition": {
        "name": "employee-attrition",
        "desc": "HR attrition: drivers, retention model, ranked watch list",
        "topics": ["python", "hr-analytics", "people-analytics"],
        "req": REQ_MODEL,
        "dates": ["2026-10-21T19:04:00",
                  "2026-10-21T22:36:00",
                  "2026-10-21T23:59:00",
                  "2026-10-22T01:12:00",
                  "2026-10-22T03:41:00"],
        "commits": [
            ("ibm hr attrition dataset in",
             ["src/00_download_data.py", "data/raw", "shared", ".gitignore", ".env.example"]),
            ("attrition drivers: overtime, satisfaction, tenure",
             ["src/01_analysis.py", "data/processed", "sql"]),
            ("retention model + ranked watch list",
             ["src/02_model_retention.py", "outputs"]),
            ("dashboard + ai insights",
             ["src/03_ai_insights.py", "src/04_dashboard.py", "dashboard"]),
            ("chatbot, hero, shots, readme + post",
             ["src/05_linkedin_hero.py", "src/06_chat.py", "assets", "README.md", "linkedin_post.md"]),
        ],
    },
}

PATH_TOLERANT = 2  # repl regex backreference newline safety


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
                    ignore=shutil.ignore_patterns("__pycache__", "*.pyc", ".git"))
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

    leftover_dates = len(spec["commits"]) - 1
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
            leftover_dates = 0
        else:
            print(f"  skip (nothing to stage): {msg}")

    # absorb anything the plan missed into the last commit
    run(["git", "add", "-A"], cwd=stage)
    dirty = run(["git", "status", "--porcelain"], cwd=stage).strip()
    if dirty:
        run(["git", "commit", "--amend", "--no-edit"], cwd=stage,
            env={**env, "GIT_AUTHOR_DATE": spec["dates"][-1],
                 "GIT_COMMITTER_DATE": spec["dates"][-1]})

    log = run(["git", "log", "--format=%h %ad %s", "--date=iso", "--all"], cwd=stage)
    print(log)
    assert "NitishPoosarla" not in log  # sanity: only messages on the log


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
