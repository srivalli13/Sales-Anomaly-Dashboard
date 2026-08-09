import streamlit as st
import pandas as pd
import sqlite3
import plotly.graph_objects as go

# ---------------------------
# Page setup
# ---------------------------
st.set_page_config(page_title="Sales Performance Dashboard", layout="wide")

st.title("Automated Sales Performance Dashboard")
st.caption("Daily KPIs with anomaly detection (Z-score + IQR methods)")

# ---------------------------
# Load data from SQLite
# ---------------------------
conn = sqlite3.connect("superstore.db")
daily = pd.read_sql("SELECT * FROM daily_kpis", conn)
daily["Date"] = pd.to_datetime(daily["Date"])

# Fix: SQLite stores booleans as 0/1 integers, so convert anomaly columns back to bool
bool_cols = [c for c in daily.columns if "anomaly" in c]
daily[bool_cols] = daily[bool_cols].astype(bool)

# ---------------------------
# KPI summary cards
# ---------------------------
latest = daily.iloc[-1]
prev = daily.iloc[-2]

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Revenue (latest day)",
    f"${latest['Revenue']:,.0f}",
    f"{(latest['Revenue'] - prev['Revenue']):,.0f}"
)

col2.metric(
    "Orders (latest day)",
    f"{latest['Orders']:,.0f}",
    f"{(latest['Orders'] - prev['Orders']):,.0f}"
)

col3.metric(
    "AOV (latest day)",
    f"${latest['AOV']:,.2f}",
    f"{(latest['AOV'] - prev['AOV']):,.2f}"
)

col4.metric(
    "Anomaly Days (total)",
    f"{int(daily['is_anomaly'].sum())}"
)

# ---------------------------
# Trend chart with anomalies highlighted
# ---------------------------
st.subheader("Daily Trend")

kpi_choice = st.selectbox(
    "Choose a KPI to view",
    ["Revenue", "Orders", "AOV", "ReturnRate"]
)

fig = go.Figure()

# Main line - the KPI over time
fig.add_trace(go.Scatter(
    x=daily["Date"],
    y=daily[kpi_choice],
    mode="lines",
    name=kpi_choice,
    line=dict(color="steelblue")
))

# Anomaly points - overlaid as red markers
anomaly_days = daily[daily["is_anomaly"]]

fig.add_trace(go.Scatter(
    x=anomaly_days["Date"],
    y=anomaly_days[kpi_choice],
    mode="markers",
    name="Anomaly",
    marker=dict(color="red", size=8, symbol="circle")
))

fig.update_layout(
    xaxis_title="Date",
    yaxis_title=kpi_choice,
    height=500
)

st.plotly_chart(fig, use_container_width=True)

# ---------------------------
# Week-over-Week comparison
# ---------------------------
st.subheader("Week-over-Week Comparison")

daily_sorted = daily.sort_values("Date").reset_index(drop=True)

last_7 = daily_sorted.tail(7)
prev_7 = daily_sorted.tail(14).head(7)

wow_col1, wow_col2, wow_col3 = st.columns(3)


def pct_change(new, old):
    if old == 0:
        return 0
    return (new - old) / old * 100


wow_col1.metric(
    "Revenue (last 7 days)",
    f"${last_7['Revenue'].sum():,.0f}",
    f"{pct_change(last_7['Revenue'].sum(), prev_7['Revenue'].sum()):.1f}%"
)

wow_col2.metric(
    "Orders (last 7 days)",
    f"{last_7['Orders'].sum():,.0f}",
    f"{pct_change(last_7['Orders'].sum(), prev_7['Orders'].sum()):.1f}%"
)

wow_col3.metric(
    "Avg Return Rate (last 7 days)",
    f"{last_7['ReturnRate'].mean() * 100:.1f}%",
    f"{pct_change(last_7['ReturnRate'].mean(), prev_7['ReturnRate'].mean()):.1f}%"
)