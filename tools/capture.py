"""Portfolio screenshot kit — one live Chromium pass per project.

For the given project folder it:
  1. serves the dashboard on a private localhost port
  2. runs the ask-the-data chatbot one-shot for the given questions and uses the
     VERBATIM captured output (not mock text) to render a terminal-style page
  3. screenshots dashboard.png + chatbot.png into <project>/assets/
  4. copies outputs/charts/*.png and linkededin hero into assets/

Run:
  python tools/capture.py --project 02-operations-311 \
      --title "🤖 Ask-the-data chatbot — live session (real output)" \
      --q1 "slowest agencies" --q2 "top case types" --q3 "scenario"
"""
from __future__ import annotations

import argparse
import functools
import http.server
import os
import shutil
import socketserver
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent  # repo root

CHAT_FONT_CSS = """body { margin:0; background:#0b1220; font-family: 'Liberation Mono', 'SF Mono', monospace; }
.term { margin: 24px; padding: 20px 24px; background: #0d1117; border: 1px solid #2d333b;
        border-radius: 10px; color: #c9d1d9; font-size: 15px; line-height: 1.5; white-space: pre-wrap; }
.bar { display:flex; gap:8px; margin-bottom:14px; }
.dot { width:12px; height:12px; border-radius:50%; }
.title { color:#8b949e; margin-left:8px; font-size: 13px; }
.you { color: #58a6ff; font-weight: bold; }
.warn { color: #d2a8ff; }
.ok { color: #7ee787; }
.money { color: #ffa657; }
h1 { color:#e6edf3; font-family: 'Liberation Sans', -apple-system, sans-serif; margin: 20px 0 0 24px; font-size: 22px; }"""


def chat_page_html(title: str, blocks: list[tuple[str, str]], project_label: str) -> str:
    body = []
    for q, out in blocks:
        out = out.strip("\n")
        lines = []
        body.append(f'<span class="you">you&gt; {q}</span>')
        for raw in out.rstrip().splitlines():
            esc = (raw.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
                      .replace(" ", "&nbsp;") or "&nbsp;")
            cls = []
            if esc.startswith("you>"):
                cls.append("you")
            elif "computed live" in esc or "could not map" in esc:
                cls.append("warn")
            elif any(s in esc for s in ("→", "ROI", "Overall:", "×", "median 1.5h")):
                cls.append("ok")
            elif "$" in esc or "%" in esc:
                cls.append("money")
            lines.append(f'<div class="{" ".join(cls)}">{esc}</div>')
        body.append("\n".join(lines))
    return f"""<!doctype html><html><head><meta charset="utf-8"><style>{CHAT_FONT_CSS}</style></head>
<body>
<h1>{title}</h1>
<div class="term"><div class="bar">
<div class="dot" style="background:#ff5f57"></div><div class="dot" style="background:#febc2e"></div>
<div class="dot" style="background:#28c840"></div><span class="title">terminal — {project_label}</span></div>
{"<br>".join(body)}</div></body></html>"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--title", required=True)
    ap.add_argument("--q", action="append", default=[], help="chat question (repeatable)")
    args = ap.parse_args()

    proj = REPO / "projects" / args.project
    py = os.environ.get("PY", sys.executable)
    assets = proj / "assets"
    assets.mkdir(exist_ok=True)

    # 1) verbatim chat capture — real output of 06_chat.py, one question at a time
    blocks = []
    for q in args.q:
        r = subprocess.run([py, str(proj / "src" / "06_chat.py"), q],
                           capture_output=True, text=True, timeout=90)
        blocks.append((q, r.stdout if r.returncode == 0 else (r.stderr or "error")))
        print(f"chat ok [{q}] rc={r.returncode}")

    session_file = assets / "chat_session.html"
    session_file.write_text(chat_page_html(args.title, blocks, args.project))

    # 2) serve dashboard statically
    dashboard = proj / "dashboard"
    port = 4100 + sum(1 for c in args.project if c.isdigit())
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(dashboard))
    httpd = socketserver.TCPServer(("127.0.0.1", port), handler)
    import threading
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    url = f"http://127.0.0.1:{port}/index.html"
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser = pw.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 950},
                                    device_scale_factor=2)
            page.goto(url, wait_until="networkidle", timeout=45000)
            page.wait_for_timeout(2500)  # settle chart animations
            page.screenshot(path=str(assets / "dashboard.png"), full_page=True)
            print("shot: assets/dashboard.png")

            page.goto(f"file://{session_file.resolve()}")
            page.wait_for_timeout(300)
            page.screenshot(path=str(assets / "chatbot.png"), full_page=True)
            print("shot: assets/chatbot.png")
            browser.close()
    finally:
        httpd.shutdown()
        httpd.server_close()

    # 3) ship chart PNGs + hero into assets for the README/repo
    for png in (proj / "outputs" / "charts").glob("*.png"):
        shutil.copy(png, assets / png.name)
    hero = proj / "outputs" / "linkedin_hero.png"
    if hero.exists():
        shutil.copy(hero, assets / "linkedin_hero.png")
    print("assets:", sorted(p.name for p in assets.iterdir()))


if __name__ == "__main__":
    main()
