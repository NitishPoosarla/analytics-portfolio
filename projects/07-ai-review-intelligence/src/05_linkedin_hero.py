"""07-ai-review-intelligence — 05_linkedin_hero.py — LinkedIn hero slide (1200x675)."""
from pathlib import Path
import json

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

PROJECT = Path(__file__).resolve().parent.parent
OUT = PROJECT / "outputs"

m = json.loads((OUT / "model_eval.json").read_text())
a = json.loads((OUT / "ai_eval.json").read_text())
best_corpus = max(m["by_corpus"], key=lambda c: m["by_corpus"][c]["acc"])

fig, ax = plt.subplots(figsize=(12, 6.75), dpi=100)
ax.set_xlim(0, 12); ax.set_ylim(0, 6.75)
ax.axis("off")
fig.patch.set_facecolor("#101828")
ax.add_patch(plt.Rectangle((0, 5.3), 12, 1.45, color="#1d2939"))
ax.text(0.5, 6.05, "DOES THE LLM BEAT THE $0 BASELINE? MEASURED, NOT VIBED.", fontsize=21,
        fontweight="bold", color="white")
ax.text(0.5, 5.6, "3,000 labelled reviews (Amazon / IMDB / Yelp) · both classifiers on identical ground truth",
        fontsize=11.5, color="#94a3b8")

cards = [
    (f"{m['baseline_acc_holdout']:.1%}", "baseline accuracy\nTF-IDF + LogReg, held-out", "#32d583", 0.5),
    (f"{a['ai_acc_sampled']:.1%}", "LLM-lexicon fallback\non a sampled test set", "#fda29b", 3.25),
    (f"{m['by_corpus'][best_corpus]['acc']:.0%}", f"best corpus\n({best_corpus})", "#32d583", 6.0),
    ("+receipts", f"latency, chars processed,\nmajority floor {m['majority_class_acc']:.0%}", "#98a2b3", 8.75),
]
for value, label, color, x in cards:
    ax.add_patch(FancyBboxPatch((x, 2.1), 2.75, 2.5, boxstyle="round,pad=0.08",
                                fc="#1d2939", ec="#344054"))
    ax.text(x + 1.375, 3.82, value, fontsize=27, fontweight="bold",
            color=color, ha="center")
    ax.text(x + 1.375, 2.80, label, fontsize=10.5, color="#98a2b3", ha="center",
            va="top")

ax.text(0.5, 1.3, "The honest finding: at 150 sampled keys the lexicon fallback loses to the held-out\n"
                  "baseline — so the pipeline ships the BASELINE to production and keeps the AI lane\n"
                  "behind an eval gate. Add an API key and 02_llm_classifier.py re-runs the receipt.",
        fontsize=12.5, color="#e4e7ec")
ax.text(0.5, 0.45, "Project 7 of 9 · built end-to-end: data → baseline → LLM lane → eval receipts → dashboard",
        fontsize=10.5, color="#667085")

fig.savefig(OUT / "linkedin_hero.png", dpi=100, bbox_inches="tight",
            facecolor=fig.get_facecolor())
print("Wrote", OUT / "linkedin_hero.png")
