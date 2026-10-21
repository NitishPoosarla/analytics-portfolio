"""Insert the visual kit (hero + dashboard + chatbot shots) and a chatbot
section into a project README — idempotent, run after tools/capture.py.

Run:  python tools/patch_readme.py --project 02-operations-311 \
        --chat "Answers slowest agencies, top case types, backlog/SLA, and the
        capacity scenarios (A: redeploy, B: SLA sweep)."
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

VISUALS = """
![](assets/linkedin_hero.png)

![](assets/dashboard.png)

*The interactive dashboard — single-file HTML, opens by double-click, PDF-export button included.*

![](assets/chatbot.png)

*The ask-the-data chatbot (`src/06_chat.py`) — answers computed live from the data; a real session.*
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--project", required=True)
    ap.add_argument("--chat", required=True)
    args = ap.parse_args()

    readme = REPO / "projects" / args.project / "README.md"
    text = readme.read_text()

    changed = False
    if "assets/linkedin_hero.png" not in text:
        lines = text.splitlines(keepends=True)
        # insert after the leading title line (and optional blank line)
        i = 1
        while i < len(lines) and lines[i].strip() == "":
            i += 1
        # skip a leading blockquote (business question) if present
        if i < len(lines) and lines[i].lstrip().startswith(">"):
            i += 1
            while i < len(lines) and (lines[i].lstrip().startswith(">") or lines[i].strip() == ""):
                if lines[i].strip() == "" and i + 1 < len(lines) and not lines[i + 1].lstrip().startswith(">"):
                    i += 1
                    break
                i += 1
        lines.insert(i, VISUALS)
        text = "".join(lines)
        changed = True

    if "## Chatbot (ask the data)" not in text:
        chat_sec = (
            "\n## Chatbot (ask the data)\n\n"
            "```bash\n"
            ".venv/bin/python src/06_chat.py                      # interactive REPL\n"
            '.venv/bin/python src/06_chat.py "<one of the questions below>"   # one-shot\n'
            "```\n\n"
            f"{args.chat.strip()}\n\n"
            "**Every number is computed live from the project's data files at question time.** "
            "With `GROQ_API_KEY` in `.env` the LLM narrates those verified facts only "
            "(it is instructed never to compute or invent); no key → the deterministic "
            "offline engine answers with the same numbers. Nothing hallucinates either way.\n"
        )
        m = re.search(r"^## Limitations", text, flags=re.M)
        if m:
            text = text[: m.start()] + chat_sec.lstrip("\n") + "\n" + text[m.start() :]
        else:
            text = text.rstrip() + "\n\n" + chat_sec
        changed = True

    if changed:
        readme.write_text(text)
        print(f"README patched: {readme}")
    else:
        print("README already up to date")


if __name__ == "__main__":
    main()
