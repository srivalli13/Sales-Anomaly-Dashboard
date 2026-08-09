# 📊 Automated Sales Performance Dashboard with Anomaly Detection

> **A live, self-monitoring analytics system** — not a static report. It ingests raw
> transaction data, computes daily KPIs, statistically flags the days that don't fit the
> pattern, and emails a human when something's off. Built end-to-end: pipeline → detection →
> dashboard → alerting → deployment.

**🔗 Live dashboard:** [https://sales-anomaly-dashboard.streamlit.app/] — click it, it's real, it's running.

---

## Why this isn't just another portfolio chart

Most "data analyst portfolio projects" are a Jupyter notebook and a screenshot. This one is a
**deployed product**: open the URL, filter the KPI, watch the anomaly points light up in real
time. It's the difference between *telling* someone you can find signal in noise, and *showing*
them a system that does it automatically.

## By the numbers

| | |
|---|---|
| 📦 Orders processed | **51,290** across 4 years, 3 global markets |
| 📅 Days aggregated into KPIs | **~1,430** |
| 🚨 Anomalous days detected | **191**, flagged by two independent statistical methods |
| 🔁 Manual work required to run it daily | **Zero** — pipeline, detection, and alerting are fully automated |

## What it actually does

1. **Pipeline** — raw order-level data → daily Revenue, Orders, AOV, and Return Rate,
   stored in a SQLite database.
2. **Anomaly detection, done properly** — not one method, but two run in parallel:
   a rolling 30-day **Z-score** (catches sudden spikes/drops) and a rolling 30-day **IQR**
   test (catches skewed, non-normal shifts the Z-score can miss). A day only needs to fail
   *one* to get flagged — belt and suspenders.
3. **Dashboard** — Streamlit + Plotly, with live KPI cards, week-over-week deltas, and an
   interactive trend line where every anomaly is a red flag you can hover over.
4. **Alerting** — a standalone script checks the latest day and fires an email the moment
   something crosses the line. This is the part that turns "analysis" into "monitoring."

## Tech stack

`Python` · `pandas` · `NumPy` · `Streamlit` · `Plotly` · `SQLite` · `smtplib` · `GitHub`

## Project structure

```
├── app.py              # Streamlit dashboard — the live product
├── alert.py             # Anomaly → email alert script
├── requirements.txt     # One-command deploy dependencies
├── superstore.db         # Daily KPI database (built by the pipeline)
└── notebook.ipynb        # Full pipeline: aggregation → anomaly detection
```

## Run it yourself

```bash
pip install -r requirements.txt
streamlit run app.py
```

## What I'd build next

- Slack/webhook alerts alongside email
- Per-region and per-category anomaly breakdowns
- A configurable sensitivity slider in the dashboard itself, so the threshold isn't buried in code

---

*Built as a demonstration of end-to-end data product thinking — from raw CSV to a live,
self-monitoring system. Questions about the approach or the code? Open an issue or reach out.*
