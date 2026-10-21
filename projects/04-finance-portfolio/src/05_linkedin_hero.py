"""04-finance-portfolio — 05_linkedin_hero.py — LinkedIn hero slide (1200x675)."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "outputs"

k = json.loads((OUT / "kpis.json").read_text())

fig, ax = plt.subplots(figsize=(12, 6.75), dpi=100)
ax.set_xlim(0, 12); ax.set_ylim(0, 6.75)
ax.axis("off")
fig.patch.set_facecolor("#101828")
ax.add_patch(plt.Rectangle((0, 5.3), 12, 1.45, color="#1d2939"))
ax.text(0.5, 6.05, "S&P 500 — THE RETURN IS REAL. SO IS THE WAIT.", fontsize=21,
        fontweight="bold", color="white")
ax.text(0.5, 5.6, "150 years of Shiller data (1871→) · every number verified in Python",
        fontsize=11.5, color="#94a3b8")

cards = [
    (f"{k['ann_return_50y']:.1%}", "annualized return\n(last 50 years)", "#32d583", 0.5),
    (f"{k['deepest_dd_pct']:.0%}", "deepest drawdown\n(peak→trough)", "#f97066", 3.25),
    (f"{k['avg_months_to_recover_top10']/12:.0f} yrs", "average time underwater\nafter a top-10 crash", "#fda29b", 6.0),
    (f"{k['real_cagr_since1871']:.1%}", "inflation-adjusted CAGR\nsince 1871", "#32d583", 8.75),
]
for value, label, color, x in cards:
    ax.add_patch(FancyBboxPatch((x, 2.1), 2.75, 2.5, boxstyle="round,pad=0.08",
                                fc="#1d2939", ec="#344054"))
    ax.text(x + 1.375, 3.80, value, fontsize=29, fontweight="bold",
            color=color, ha="center")
    ax.text(x + 1.375, 2.78, label, fontsize=10.5, color="#98a2b3", ha="center",
            va="top")

ax.text(0.5, 1.3, "A 9% nominal annual return still hid droughts measured in years:\n"
                  "worst rolling 20-year real outcome was negative. Plan cash flows, not feelings.",
        fontsize=13, color="#e4e7ec")
ax.text(0.5, 0.45, "Project 4 of 9 · built end-to-end: data → drawdown analysis → AI narration → dashboard",
        fontsize=10.5, color="#667085")

fig.savefig(OUT / "linkedin_hero.png", dpi=100, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Wrote", OUT / "linkedin_hero.png")
