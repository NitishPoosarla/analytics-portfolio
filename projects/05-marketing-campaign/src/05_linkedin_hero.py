"""05-marketing-campaign — 05_linkedin_hero.py — LinkedIn hero slide (1200x675)."""
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
ax.text(0.5, 6.05, "TELEMARKETING — TARGET SMARTER, DIAL LESS", fontsize=21,
        fontweight="bold", color="white")
ax.text(0.5, 5.6, "45,211 call records from the UCI bank marketing set",
        fontsize=11.5, color="#94a3b8")

cards = [
    (f"{k['conversion_rate']:.1%}", "overall conversion\n— the 'spray' baseline", "#fda29b", 0.5),
    (f"{k['response_rate_prior_success']:.0%}", "conversion when the last\ncampaign succeeded", "#32d583", 3.25),
    (f"{k['campaign_roi']:.1f}x", "campaign ROI\n(stated assumptions)", "#32d583", 6.0),
    ("Top decile", "of the model = 10% of\ncontacts, 61% of\nall conversions", "#f97066", 8.75),
]
for value, label, color, x in cards:
    ax.add_patch(FancyBboxPatch((x, 2.1), 2.75, 2.5, boxstyle="round,pad=0.08",
                                fc="#1d2939", ec="#344054"))
    ax.text(x + 1.375, 3.85, value, fontsize=26, fontweight="bold",
            color=color, ha="center", va="center")
    ax.text(x + 1.375, 2.88, label, fontsize=10, color="#98a2b3", ha="center",
            va="top")

ax.text(0.5, 1.3, "The logistic model ranks every prospect by likelihood to subscribe.\n"
                  "Dial the top decile first — the same 10% of contacts carries 61% of\n"
                  "all conversions (6.1x the baseline hit-rate per call).",
        fontsize=13, color="#e4e7ec")
ax.text(0.5, 0.45, "$2.50/call and $120 margin are stated assumptions, not sourced facts",
        fontsize=10.5, color="#667085")

fig.savefig(OUT / "linkedin_hero.png", dpi=100, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Wrote", OUT / "linkedin_hero.png")
