# LinkedIn post — Project 03 (Supply Chain)

---

One supplier outage on the top-20 SKUs would hit ~40% of this retailer's revenue.
I quantified that risk — and priced the hedge. 📦

Dataset: 525,000 transactions from a real UK online retailer (UCI Online Retail II, public).

What stands out:
→ SKU concentration: the top-20 SKUs carry a revenue share large enough that "notify
   procurement" isn't a plan — dual-sourcing them costs +6% landed cost (stated assumption)
→ One-market exposure: ~90% of revenue sits in the UK; an export push into the top-5
   non-UK markets is costed at ~$123k incremental revenue
→ 9% of revenue value keeps coming BACK as returns — returns capacity belongs in the
   same S&OP plan as forward orders
→ The holiday surge shows up like clockwork in the monthly pipeline — the capacity
   calendar is not a mystery, it's a chart

Every number above was computed and verified in Python. The AI layer narrates the
story from those verified metrics only — it never invents a KPI.

Dashboard link + full repo in the comments.

#supplychain #procurement #inventorymanagement #businessanalytics #python #SOP

---

**Post tips**
- Replace "~40%" with the exact top-20 share from kpis.json before posting.
- Lead image: SKU concentration curve — it tells the whole story in one glance.
