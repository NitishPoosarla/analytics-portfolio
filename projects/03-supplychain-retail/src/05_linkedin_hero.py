"""03-supplychain-retail — 05_linkedin_hero.py — LinkedIn hero slide (1200x675)."""
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
ax.text(0.5, 6.05, "ONLINE RETAIL — WHERE DOES SUPPLY CHAIN RISK CONCENTRATE?",
        fontsize=21, fontweight="bold", color="white")
ax.text(0.5, 5.6, "541,910 rows, 13 months, one UK online retailer (UCI Online Retail II)",
        fontsize=11.5, color="#94a3b8")

cards = [
    (f"{k['top20_sku_revenue_share']:.1%}", "of revenue sits in the\ntop-20 SKUs", "#f97066", 0.5),
    (f"{k['returns_rev_share']:.1%}", "of revenue value comes\nBACK as returns", "#fda29b", 3.25),
    (f"{k['uk_share_revenue']:.0%}", "one-market exposure\n(UK share of revenue)", "#f97066", 6.0),
    (f"${s['scenario_b_export_revenue_gain']/1000:.0f}k", "export-push revenue\ntop-5 non-UK markets", "#32d583", 8.75),
]
for value, label, color, x in cards:
    ax.add_patch(FancyBboxPatch((x, 2.1), 2.75, 2.5, boxstyle="round,pad=0.08",
                                fc="#1d2939", ec="#344054"))
    ax.text(x + 1.375, 3.80, value, fontsize=30, fontweight="bold",
            color=color, ha="center")
    ax.text(x + 1.375, 2.78, label, fontsize=10.5, color="#98a2b3", ha="center",
            va="top")

ax.text(0.5, 1.3, "Dual-sourcing the top-20 SKUs costs +6% landed cost (stated assumption) —\n"
                  "priced against a single-supplier outage. The hedge has a number now.",
        fontsize=13, color="#e4e7ec")
ax.text(0.5, 0.45, "both hedge scenarios recompute from the data - outage cost is priced, not guessed",
        fontsize=10.5, color="#667085")

fig.savefig(OUT / "linkedin_hero.png", dpi=100, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Wrote", OUT / "linkedin_hero.png")
