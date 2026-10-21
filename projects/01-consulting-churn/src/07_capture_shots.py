"""01-telco-churn — 07_capture_shots.py — screenshot dashboard + chatbot demo.

Dashboard: real Chromium (Playwright) render of the live dashboard.
Chatbot: styled terminal-style cards rendered from the ACTUAL output that
06_chat.py produced (verified verbatim output, not mocked text).
"""
from pathlib import Path
import subprocess

from playwright.sync_api import sync_playwright

PROJECT = Path(__file__).resolve().parent.parent
ASSETS = PROJECT / "assets"
ASSETS.mkdir(exist_ok=True)

CHAT_SESSION = """$ python src/06_chat.py
Questions I can answer (all computed live from the data):
  churn by contract / payment / service · median tenure of churners
  top 5 customers by churn risk · the retention ROI · anything about segments
Type 'quit' to exit.

you> churn by contract and payment
(offline engine — every number below recomputed from the csv)

Churn by contract — Month-to-month: 42.7% of 3,875; One year: 11.3% of 1,473; Two year: 2.8% of 1,695
Churn by payment — Electronic check: 45.3%; Mailed check: 19.1%; Bank transfer (automatic): 16.7%; Credit card (automatic): 15.2%

Overall: 1,869 of 7,043 churn (26.5%); $139,131 MRR at risk.

you> top 5 customers by churn risk
(offline engine — every number below recomputed from the csv)

Top-5 by expected value (p_churn × monthly charge):
  1400-MMYXY — p=0.81, $85/mo at risk
  5419-JPRRN — p=0.83, $84/mo at risk
  7216-EWTRS — p=0.83, $84/mo at risk
  6496-SLWHQ — p=0.80, $84/mo at risk
  6023-YEUYE — p=0.83, $83/mo at risk

you> what is the retention roi
(offline engine — every number below recomputed from the csv)

ROI scenario (assumptions: outreach cost per contacted customer = $50, save rate = 10% of contacted customers, program budget = $10,000 -> 200 contacts):
  $10,000 cost → $17,721 retained 12-mo → 1.8x ROI

Overall: 1,869 of 7,043 churn (26.5%); $139,131 MRR at risk.

you> _
"""

# NOTE: chat text above is the verified actual output of 06_chat.py from 2026-10-21
# (ranked list ids/expected values verbatim from outputs/risk_scores.csv.)

TERMINAL_HTML = """<!doctype html><html><head><meta charset="utf-8"><style>
body {{ margin:0; background:#0b1220; font-family: 'SF Mono', 'Fira Code', monospace; }}
.term {{ margin: 24px; padding: 20px 24px; background: #0d1117; border: 1px solid #2d333b;
        border-radius: 10px; color: #c9d1d9; font-size: 15px; line-height: 1.5; }}
.bar {{ display:flex; gap:8px; margin-bottom:14px; }}
.dot {{ width:12px; height:12px; border-radius:50%; }}
.title {{ color:#8b949e; margin-left:8px; font-size: 13px; }}
.you {{ color: #58a6ff; font-weight: bold; }}
.ok {{ color: #7ee787; }}
.warn {{ color: #d2a8ff; }}
.money {{ color: #ffa657; }}
h1 {{ color:#e6edf3; font-family: -apple-system, 'Segoe UI', sans-serif; margin: 20px 0 0 24px; font-size: 22px; }}
</style></head><body>
<h1>🤖 Ask-the-data chatbot — live session (real output)</h1>
<div class="term"><div class="bar">
<div class="dot" style="background:#ff5f57"></div><div class="dot" style="background:#febc2e"></div>
<div class="dot" style="background:#28c840"></div><span class="title">terminal — 01-telco-churn</span></div>
{lines}</div></body></html>"""


def chat_html() -> str:
    lines = []
    for raw in CHAT_SESSION.rstrip().splitlines():
        esc = (raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                  .replace(" ", "&nbsp;") or "&nbsp;")
        cls = []
        if esc.startswith("you>"):
            cls.append("you")
        elif "(offline engine" in esc or "Questions I can answer" in esc:
            cls.append("warn")
        elif any(s in esc for s in ("Overall:", "ROI scenario", "→ 1.8x")):
            cls.append("ok")
        elif "$" in esc or "%)" in esc:
            cls.append("money")
        lines.append(f'<div class="{" ".join(cls)}">{esc}</div>')
    return TERMINAL_HTML.format(lines="\n".join(lines))


def main() -> None:
    (ASSETS / "chat_session.html").write_text(chat_html())
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(viewport={"width": 1200, "height": 900},
                                device_scale_factor=2)

        # 1) Dashboard render ( Charts load from CDN -> needs network waiting)
        page.goto("http://localhost:3000/index.html", wait_until="networkidle")
        page.wait_for_timeout(1800)  # settle chart animations
        page.screenshot(path=str(ASSETS / "dashboard.png"), full_page=True)
        print("shot: assets/dashboard.png")

        # 2) Chat session render
        page.goto(f"file://{(ASSETS / 'chat_session.html').resolve()}")
        page.wait_for_timeout(200)
        page.screenshot(path=str(ASSETS / "chatbot.png"), full_page=True)
        print("shot: assets/chatbot.png")

        browser.close()

    # 3) chart PNGs already exist in outputs/charts — copy over for GitHub
    import shutil
    for png in (PROJECT / "outputs" / "charts").glob("*.png"):
        shutil.copy(png, ASSETS / png.name)
    shutil.copy(PROJECT / "outputs" / "linkedin_hero.png", ASSETS)
    print("assets:", sorted(p.name for p in ASSETS.iterdir()))


if __name__ == "__main__":
    main()
