"""01-telco-churn — 05_linkedin_hero.py — LinkedIn hero slide (1200x675)."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "outputs"

k = json.loads((OUT / "kpis.json").read_text())
e = json.loads((OUT / "model_eval.json").read_text())

fig, ax = plt.subplots(figsize=(12, 6.75), dpi=100)
ax.set_xlim(0, 12); ax.set_ylim(0, 6.75)
ax.axis("off")
fig.patch.set_facecolor("#101828")
ax.add_patch(plt.Rectangle((0, 5.3), 12, 1.45, color="#1d2939"))
ax.text(0.5, 6.05, "TELCO CHURN — WHO DO WE PAY TO KEEP?", fontsize=21,
        fontweight="bold", color="white")
ax.text(0.5, 5.6, "7,043 customers · IBM Telco churn (public) · numbers recomputed from the csv",
        fontsize=11.5, color="#94a3b8")

cards = [
    (f"{k['churn_rate']:.1%}", "churn rate", "#f97066", 0.5),
    (f"${k['mrr_at_risk_usd']/1000:.0f}k", "monthly revenue at risk", "#f97066", 3.25),
    ("42.7%", "month-to-month churn\n(vs 2.8% two-year)", "#fda29b", 6.0),
    (f"{e['roi_12m']:.1f}x", "12-mo program ROI\n(stated assumptions)", "#32d583", 8.75),
]
for value, label, color, x in cards:
    ax.add_patch(FancyBboxPatch((x, 2.1), 2.75, 2.5, boxstyle="round,pad=0.08",
                                fc="#1d2939", ec="#344054"))
    ax.text(x + 1.375, 3.65, value, fontsize=30, fontweight="bold",
            color=color, ha="center")
    ax.text(x + 1.375, 2.75, label, fontsize=10.5, color="#98a2b3", ha="center",
            va="top")

ax.text(0.5, 1.3, "Model AUC 0.84 ranks every customer by dollars at risk →\n"
                  "the save-list, not a chart.", fontsize=13, color="#e4e7ec")
ax.text(0.5, 0.45, "model ranks every customer by dollars at risk; outreach assumptions written down",
        fontsize=10.5, color="#667085")

fig.savefig(OUT / "linkedin_hero.png", dpi=100, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Wrote", OUT / "linkedin_hero.png")


if __name__ == "__main__":
    pass
else:  # allow both import styles
    main = None
