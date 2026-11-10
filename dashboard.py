
import sqlite3
from pathlib import Path

import pandas as pd
import streamlit as st

DB = Path(__file__).resolve().parent / "sensors.sqlite3"

st.set_page_config(
    page_title="Smart Wireless Sensor Network",
    page_icon="📡",
    layout="wide"
)

st.title("📡 Smart Wireless Sensor Network")
st.subheader("Monitorizare IoT - Edge si Cloud")

st.caption(
    "Senzori virtuali → MQTT → Gateway Edge → "
    "Backend → SQLite → Frontend"
)

# Actualizare automata la fiecare 3 secunde
@st.fragment(run_every="3s")
def afiseaza_dashboard():
    if not DB.exists():
        st.warning("Baza de date nu exista inca.")
        return

    with sqlite3.connect(DB) as conn:
        df = pd.read_sql_query(
            """
            SELECT id, senzor, seq, valoare, unitate,
                   timestamp, alerta, status, injected,
                   spike, date_lipsa, drift
            FROM measurements
            ORDER BY id DESC
            LIMIT 300
            """,
            conn
        )

    if df.empty:
        st.info("Asteptam masuratori de la senzori...")
        return

    df = df.sort_values("id")
    df["timestamp"] = pd.to_datetime(
        df["timestamp"], utc=True, errors="coerce"
    )

    total = len(df)
    alerte = int(df["alerta"].fillna(0).sum())
    spikes = int(df["spike"].fillna(0).sum())
    drift = int(df["drift"].fillna(0).sum())

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Masuratori afisate", total)
    c2.metric("Alerte Edge", alerte)
    c3.metric("Spikes", spikes)
    c4.metric("Drift Cloud", drift)

    st.divider()

    senzori = [
        ("co2", "CO2 (ppm)"),
        ("temperatura", "Temperatura (°C)"),
        ("lumina", "Luminozitate (lux)")
    ]

    for tip, titlu in senzori:
        date_senzor = df[
            (df["senzor"] == tip) &
            (df["timestamp"].notna())
        ].copy()

        st.subheader(titlu)

        if date_senzor.empty:
            st.info(f"Nu exista date pentru {tip}.")
        else:
            date_senzor = date_senzor.sort_values(
                ["timestamp", "id"]
            )
            st.line_chart(
                date_senzor,
                x="timestamp",
                y="valoare",
                x_label="Timp",
                y_label=titlu
            )

    st.divider()
    st.subheader("Ultimele masuratori")

    st.dataframe(
        df.sort_values("id", ascending=False).head(20),
        use_container_width=True,
        hide_index=True
    )

    st.caption(
        "Graficele se actualizeaza automat la fiecare 3 secunde."
    )


afiseaza_dashboard()
