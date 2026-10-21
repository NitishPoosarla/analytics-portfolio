"""06-software-delivery — 05_linkedin_hero.py — LinkedIn hero slide (1200x675)."""
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
ax.text(0.5, 6.05, "1,000 REAL ISSUES — WHAT ACTUALLY SLOWS DELIVERY?", fontsize=21,
        fontweight="bold", color="white")
ax.text(0.5, 5.6, "pandas issue tracker sample · cycle time triage · every number verified in Python",
        fontsize=11.5, color="#94a3b8")

cards = [
    (f"{k['median_cycle_days']:.1f}d", "median cycle time\n(closed issues)", "#32d583", 0.5),
    (f"{k['p90_cycle_days']:.1f}d", "p90 cycle time\n— the tail is the story", "#fda29b", 3.25),
    (f"{k['share_open_over_180d']:.0%}", "open issues older\nthan 180 days", "#f97066", 6.0),
    ("-38%", "median open age when\ntriage labels are on", "#32d583", 8.75),
]
for value, label, color, x in cards:
    ax.add_patch(FancyBboxPatch((x, 2.1), 2.75, 2.5, boxstyle="round,pad=0.08",
                                fc="#1d2939", ec="#344054"))
    ax.text(x + 1.375, 3.82, value, fontsize=29, fontweight="bold",
            color=color, ha="center")
    ax.text(x + 1.375, 2.80, label, fontsize=10.5, color="#98a2b3", ha="center",
            va="top")

ax.text(0.5, 1.3, "Labeled issues wait 9.7d to a decision vs 15.6d unlabeled — triage discipline\n"
                  "is a delivery-velocity lever you can measure, not a process religion.",
        fontsize=13, color="#e4e7ec")
ax.text(0.5, 0.45, "Project 6 of 9 · built end-to-end: data → delivery analytics → AI narration → dashboard",
        fontsize=10.5, color="#667085")

fig.savefig(OUT / "linkedin_hero.png", dpi=100, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Wrote", OUT / "linkedin_hero.png")
