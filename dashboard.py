import sqlite3, time
import pandas as pd
import streamlit as st
st.set_page_config(page_title='Smart WSN Monitor', layout='wide')
st.title('📡 Smart Wireless Sensor Network Monitoring')
st.caption('Replay UCI Room Occupancy Estimation · prototip demonstrativ')
try:
    with sqlite3.connect('/data/sensors.sqlite3', timeout=10) as db:
        df = pd.read_sql_query('SELECT * FROM measurements ORDER BY seq DESC LIMIT 300', db)
except sqlite3.OperationalError:
    df = pd.DataFrame()
if df.empty:
    st.info('Se așteaptă date MQTT. Actualizează pagina în câteva secunde.')
else:
    last = df.iloc[0]
    a,b,c,d = st.columns(4)
    a.metric('CO₂ (ppm)', f"{last.co2:.0f}")
    b.metric('Temperatură (°C)', f"{last.temp:.1f}")
    c.metric('Lumină (lux)', f"{last.light:.0f}")
    d.metric('Ocupare reală', str(last.occupancy))
    st.subheader('Istoric CO₂ și temperatură')
    st.line_chart(df.sort_values('seq').set_index('seq')[['co2','temp']])
    st.subheader('Alerte (prag demonstrativ CO₂ > 1800 ppm)')
    st.dataframe(df[df.alert == 1][['seq','ts','co2','injected']], use_container_width=True)
    st.caption(f'Înregistrări vizibile: {len(df)} · alerte: {int(df.alert.sum())}')
if st.button('Actualizează'):
    st.rerun()
