"""08-technology-jobs — 05_linkedin_hero.py — LinkedIn hero slide (1200x675)."""
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
ax.text(0.5, 6.05, "AI/DS SALARY MARKET — WHAT THE JOBS DATA ACTUALLY SAYS", fontsize=21,
        fontweight="bold", color="white")
ax.text(0.5, 5.6, f"{k['records']} salary records · {k['years']} years · every number verified in Python",
        fontsize=11.5, color="#94a3b8")

cards = [
    (f"${k['median_salary_usd']/1000:.0f}k", "global median salary", "#32d583", 0.5),
    (f"${k['us_row']['median']/1000:.0f}k", f"US median ({k['us_row']['records']} records)\n— the top market", "#32d583", 3.25),
    (f"+{(k['remote_median']/k['onsite_median']-1):.0%}", "remote premium\nover on-site", "#f97066", 6.0),
    (f"{k['exp_impact']:.1f}x", "experience multiplier\n(senior vs junior)", "#fda29b", 8.75),
]
for value, label, color, x in cards:
    ax.add_patch(FancyBboxPatch((x, 2.1), 2.75, 2.5, boxstyle="round,pad=0.08",
                                fc="#1d2939", ec="#344054"))
    ax.text(x + 1.375, 3.82, value, fontsize=27, fontweight="bold",
            color=color, ha="center")
    ax.text(x + 1.375, 2.80, label, fontsize=10.5, color="#98a2b3", ha="center",
            va="top")

ax.text(0.5, 1.3, "Same title, different market: geo-adjusted medians, remote premiums and\n"
                  "role-level spreads from public filings — not vibes. Job-lever, not glass-ceiling.",
        fontsize=13, color="#e4e7ec")
ax.text(0.5, 0.45, "Project 8 of 9 · built end-to-end: data → market read → AI narration → dashboard",
        fontsize=10.5, color="#667085")

fig.savefig(OUT / "linkedin_hero.png", dpi=100, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Wrote", OUT / "linkedin_hero.png")
