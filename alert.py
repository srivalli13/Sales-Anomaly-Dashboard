import os
import smtplib
import sqlite3
import pandas as pd
from email.mime.text import MIMEText

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
# Check the latest day for anomalies
# ---------------------------
latest = daily.iloc[-1]

if latest["is_anomaly"]:
    lines = [f"Anomaly detected on {latest['Date'].date()}:"]

    for col in ["Revenue", "Orders", "AOV", "ReturnRate"]:
        if latest[f"{col}_anomaly_z"] or latest[f"{col}_anomaly_iqr"]:
            lines.append(f"- {col}: {latest[col]:.2f} (z-score: {latest[f'{col}_zscore']:.2f})")

    body = "\n".join(lines)

    sender = os.environ["GMAIL_ADDRESS"]
    password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEText(body)
    msg["Subject"] = f"Sales Anomaly Alert - {latest['Date'].date()}"
    msg["From"] = sender
    msg["To"] = sender

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

    print("Alert email sent.")
else:
    print("No anomaly today. No email sent.")