"""02-operations-311 — 05_linkedin_hero.py — LinkedIn hero slide (1200x675)."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "outputs"

k = json.loads((OUT / "kpis.json").read_text())
s = json.loads((OUT / "scenarios.json").read_text())

fig, ax = plt.subplots(figsize=(12, 6.75), dpi=100)
ax.set_xlim(0, 12); ax.set_ylim(0, 6.75)
ax.axis("off")
fig.patch.set_facecolor("#101828")
ax.add_patch(plt.Rectangle((0, 5.3), 12, 1.45, color="#1d2939"))
ax.text(0.5, 6.05, "NYC 311 — WHERE DOES SERVICE DELIVERY LOSE TIME?", fontsize=21,
        fontweight="bold", color="white")
ax.text(0.5, 5.6, "150,000 cases, one quarter of NYC 311 (public Socrata data)",
        fontsize=11.5, color="#94a3b8")

cards = [
    (f"{k['median_resolve_h']:.1f}h", "median resolution\ncity-wide", "#32d583", 0.5),
    (f"{k['share_over_72h']:.1%}", "cases blowing the\n72-hour SLA", "#f97066", 3.25),
    (f"{k['worst_agency_med_h']/24:.0f}d", "slowest agency:\nmedian to close", "#fda29b", 6.0),
    (f"${s['a_redeploy_value_per_quarter']/1000:.0f}k", "capacity freed\nper quarter (Scenario A)", "#32d583", 8.75),
]
for value, label, color, x in cards:
    ax.add_patch(FancyBboxPatch((x, 2.1), 2.75, 2.5, boxstyle="round,pad=0.08",
                                fc="#1d2939", ec="#344054"))
    ax.text(x + 1.375, 3.80, value, fontsize=30, fontweight="bold",
            color=color, ha="center")
    ax.text(x + 1.375, 2.78, label, fontsize=10.5, color="#98a2b3", ha="center",
            va="top")

ax.text(0.5, 1.3, "Re-deploy 12% of intake capacity to the 5 slowest heavy-volume case\n"
                  "types → $527k of staff capacity per quarter (assumptions on file).",
        fontsize=13, color="#e4e7ec")
ax.text(0.5, 0.45, "assumptions: $45/staff-hr and 1.6 labor-hrs per case, both on file",
        fontsize=10.5, color="#667085")

fig.savefig(OUT / "linkedin_hero.png", dpi=100, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Wrote", OUT / "linkedin_hero.png")
