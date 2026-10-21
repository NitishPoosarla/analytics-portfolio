"""09-management-attrition — 05_linkedin_hero.py — LinkedIn hero slide (1200x675)."""
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
ax.text(0.5, 6.05, "WHY DO PEOPLE LEAVE? THREE MEASURED LEVERS.", fontsize=21,
        fontweight="bold", color="white")
ax.text(0.5, 5.6, "1,470 employees · IBM HR dataset (public) · every number verified in Python",
        fontsize=11.5, color="#94a3b8")

cards = [
    (f"{k['attrition_rate']:.1%}", "attrition rate\nbaseline", "#fda29b", 0.5),
    (f"{k['overtime_flag']:.0%}", "attrition when\novertime = yes", "#f97066", 3.25),
    (f"{k['new_hire_drop']:.0%}", "attrition inside\nthe first stretch", "#f97066", 6.0),
    ("2 nearby\nlevers", f"low satisfaction:\n{k['low_sat_rate']:.0%} vs\n{k['high_sat_rate']:.0%} engaged", "#fda29b", 8.75),
]
for value, label, color, x in cards:
    ax.add_patch(FancyBboxPatch((x, 2.1), 2.75, 2.5, boxstyle="round,pad=0.08",
                                fc="#1d2939", ec="#344054"))
    ax.text(x + 1.375, 3.78, value, fontsize=25, fontweight="bold",
            color=color, ha="center", va="center")
    ax.text(x + 1.375, 2.86, label, fontsize=10, color="#98a2b3", ha="center",
            va="top")

ax.text(0.5, 1.3, "Overtime, low satisfaction, and the early-tenure cliff — modeled per employee\n"
                  "into a ranked watch-list, so 1:1s start with the top rows, not the org chart.",
        fontsize=13, color="#e4e7ec")
ax.text(0.5, 0.45, "Project 9 of 9 · built end-to-end: data → model → ranked watch-list → AI narration → dashboard",
        fontsize=10.5, color="#667085")

fig.savefig(OUT / "linkedin_hero.png", dpi=100, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Wrote", OUT / "linkedin_hero.png")
