# LinkedIn post — Project 07 (AI)

---

"A GenAI classifier gets 92% on sentiment." — OK. Against WHAT?

The question every AI project should answer, and the one mine is built around:
**what did the cheap baseline score, and what did the AI actually add?** 📑

3,000 labelled reviews (Amazon/IMDB/Yelp, public data):
→ Costed baseline: TF-IDF + logistic regression — near-instant, free at inference
→ Same holdout rules for the AI classifier — same accuracy/F1, PLUS latency and
   characters processed (AI isn't free; measure it)
→ An explicit verdict field: does AI beat the baseline on the same data?
→ A human-audit sample (every prediction with its source text) so a reviewer can
   spot-check in seconds

That's the difference between an AI demo and an AI system: the receipts are the
product. Dashboard + evaluation code in the repo (first comment).

#artificialintelligence #genai #machinelearning #dataanalytics #monitoring #evaluation

---

**Post tips**
- Attach the comparison bar chart (majority vs baseline vs AI).
- This is the project to talk about in interviews for "data + AI" roles — you control
  the narrative: skepticism → receipts → decision.
