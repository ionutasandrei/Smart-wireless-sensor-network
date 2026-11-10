# Smart Wireless Sensor Network Monitoring with Edge AI

## 1. Descriere și scenariu
Proiect pentru disciplina **Tehnici de Programare în IoT**. Simulează o rețea wireless cu șapte noduri de senzori și un gateway edge, utilizând înregistrări reale din datasetul UCI *Room Occupancy Estimation*. Datele sunt redate periodic prin MQTT, analizate local sau centralizat și afișate într-un dashboard web. **Nu necesită hardware fizic.**

## 2. Întrebare de cercetare (RQ1)
**Unde este mai eficient să executăm detecția anomaliilor: pe edge, în cloud sau într-o arhitectură hibridă?**

**Ipoteză H1:** În condiții de rețea degradată, detecția pe edge reduce latența P95 a alertelor față de cloud, cu o posibilă creștere a consumului local CPU.

**Baseline:** detecție centralizată prin reguli fixe. **Abordare propusă:** detecție locală, centralizată și hibridă, cu aceeași regulă/model, evaluată pe aceleași date.

## 3. Dataset și proveniență
- Sursă: [UCI Room Occupancy Estimation](https://archive.ics.uci.edu/dataset/864/room+occupancy+estimation)
- DOI: [10.24432/C5P605](https://doi.org/10.24432/C5P605)
- 10.129 înregistrări; șapte noduri wireless, un nod edge; variabile de temperatură, lumină, sunet, CO₂, PIR; etichetă `Room_Occupancy_Count` (0–3 persoane).
- Licență: **CC BY 4.0**, cu atribuirea autorilor A. P. Singh și S. Chaudhari.
- Datele sunt măsurători istorice, **nu** senzori conectați live. Simulatorul le retransmite ca mesaje MQTT.
- Eticheta de ocupare **nu** este o etichetă de anomalie. Anomaliile introduse experimental vor fi marcate separat.

## 4. Arhitectură
`Dataset UCI → Python replay → MQTT Mosquitto → Gateway/Edge → Backend SQLite → Dashboard Streamlit`

În modul edge, gateway-ul decide local și transmite alertele. În modul cloud, backend-ul decide după recepția măsurătorilor. Modul hibrid combină decizia locală cu verificarea în backend.

## 5. Obiective MVP
- [x] Scenariu și dataset public identificat
- [x] Cod de replay MQTT, ingestie, stocare și dashboard furnizat
- [ ] Validarea rulării integrale în Docker pe calculator
- [ ] Măsurarea latenței, traficului și consumului CPU/RAM
- [ ] Implementarea comparației complete edge/cloud/hibrid
- [ ] Evaluarea precision, recall și F1 pe anomalii etichetate experimental
- [ ] Extensie opțională: asistent LLM ancorat în datele SQLite

## 6. Tehnologii
Python 3.11, pandas, scikit-learn (pentru extindere ML), paho-mqtt, Eclipse Mosquitto, SQLite, Streamlit, Docker Compose.

## 7. Experiment propus
1. Replay fără anomalii.
2. Injectarea unor anomalii etichetate (de exemplu valori CO₂ crescute artificial) în datele de test.
3. Simularea întârzierilor și pierderilor de pachete.
4. Repetarea fiecărui scenariu în modurile edge, cloud și hibrid, cu seed-uri fixe.
5. Compararea latenței P50/P95, traficului în octeți, CPU/RAM, precision/recall/F1 și alarmelor false.

**Important:** rezultatele experimentale nu au fost încă măsurate; nu se pretinde o superioritate a unei metode înaintea testelor.

## 8. Pornire demo
1. Instalează Docker Desktop și pornește Docker Engine.
2. În directorul proiectului rulează `docker compose up --build`.
3. Deschide `http://localhost:8501` pentru dashboard.
4. Simulatorul descarcă datasetul UCI la prima pornire (este necesar internet); apoi redă câte un rând la fiecare 2 secunde.
5. Oprește cu `Ctrl+C` sau `docker compose down`.

Acest pachet reprezintă un **prototip demonstrativ**, nu o implementare complet validată a tuturor experimentelor RQ1.

## 9. API și procesare
Demo-ul folosește MQTT ca transport, un consumer Python pentru stocare și Streamlit pentru vizualizare. Nu include încă un API REST public; acesta poate fi adăugat într-un sprint ulterior.

## 10. Structura repository-ului
- `app/replay.py`: replay date și injectare de anomalii controlate
- `app/consumer.py`: ingestie MQTT, SQLite și reguli
- `app/dashboard.py`: vizualizare date și alerte
- `docker-compose.yml`: pornirea serviciilor
- `requirements.txt`: biblioteci Python
- `docs/PLAN.md`: etape, criterii și limitări

## 11. Riscuri și limitări
Replay-ul datelor istorice nu reproduce toate proprietățile unei rețele radio reale. Datasetul nu include RSL, BER, RSSI sau pierderi de pachete măsurate; degradarea rețelei trebuie simulată și documentată distinct. Pragurile de CO₂ din demo sunt ilustrative, nu recomandări de siguranță.

## 12. Referințe
Singh, A. P. & Chaudhari, S. (2018). *Room Occupancy Estimation*. UCI Machine Learning Repository. https://doi.org/10.24432/C5P605

Model de structură: exemplul Smart Greenhouse Monitoring furnizat la curs; întrebarea RQ1 și metodologia experimentală provin din documentul `RQs(1).pdf` al disciplinei.
## 13. Implementare practică – Full Chain IoT, Edge și Cloud

### 13.1. Descriere

Pe lângă prototipul Docker bazat pe datasetul UCI, a fost realizată o implementare practică independentă, în Python, pe Windows.

Această implementare demonstrează comunicarea completă dintre senzori, Gateway, Backend, baza de date și interfața grafică.

**Arhitectură:**

Senzori virtuali → MQTT Mosquitto → Gateway Edge → Backend → SQLite → Frontend Streamlit

### 13.2. Componente

- `senzor.py` – simulează trei tipuri de senzori: CO₂, temperatură și luminozitate.
- `gateway.py` – recepționează măsurătorile MQTT și detectează spike-uri, date lipsă și depășirea pragului CO₂.
- `backend.py` – salvează măsurătorile în SQLite și detectează tendințele crescătoare (drift).
- `test_drift.py` – transmite o serie controlată de valori CO₂ pentru testarea drift-ului.
- `dashboard.py` – afișează măsurătorile și graficele într-o interfață web Streamlit.
- `sensors.sqlite3` – baza de date generată local în timpul rulării; nu este necesară încărcarea pe GitHub.

### 13.3. Detectarea anomaliilor

**Edge – Spikes:** variațiile absolute ale CO₂ mai mari de 700 ppm față de măsurătoarea precedentă sunt marcate ca spike.

**Edge – Missing Data:** Gateway-ul compară numerele de secvență. În testul demonstrativ, trecerea de la `seq=28` la `seq=10000` a evidențiat 9.971 de secvențe omise intenționat.

**Edge – Alertă CO₂:** valorile mai mari de 1.800 ppm generează o alertă.

**Backend / Cloud – Drift:** ultimele cinci măsurători CO₂ sunt analizate pentru identificarea unei creșteri continue de minimum 400 ppm.

Seria experimentală `600 → 750 → 900 → 1050 → 1200 ppm` a fost detectată și înregistrată cu `drift=1`.

Componenta Cloud este simulată prin Backend-ul executat local. Algoritmii utilizați în această etapă sunt bazați pe reguli, nu pe un model AI antrenat.

### 13.4. Rularea aplicației pe Windows

Se instalează Python, Eclipse Mosquitto și bibliotecile necesare:

```bat
python -m pip install paho-mqtt pandas streamlit
```

Brokerul MQTT trebuie să fie pornit pe `127.0.0.1:1883`.

Din folderul proiectului, în ferestre CMD separate, se execută:

```bat
python gateway.py
python backend.py
python senzor.py co2
python senzor.py temperatura
python senzor.py lumina
```

Pentru interfața grafică:

```bat
python -m streamlit run dashboard.py
```

Dashboard-ul poate fi accesat la:

`http://localhost:8501`

Pentru testarea drift-ului, se poate executa separat:

```bat
python test_drift.py
```

### 13.5. Interfața grafică și rezultate

Dashboard-ul Streamlit afișează grafice pentru:

- CO₂, exprimat în ppm;
- Temperatură, exprimată în °C;
- Luminozitate, exprimată în lux.

Sunt afișate și numărul măsurătorilor, alertele Edge, spike-urile, drift-ul și ultimele înregistrări din SQLite.

Graficele sunt actualizate automat la fiecare trei secunde.

La momentul capturii de ecran au fost afișate 300 de măsurători, 18 alerte Edge, 14 spike-uri și 3 detecții drift. Aceste valori se referă la fereastra de date afișată, nu la totalul istoric.

### 13.6. Documentație experimentală

Au fost realizate următoarele rapoarte PDF:

- `Cerinta_2_Senzori_Gateway.pdf` – transmiterea datelor de la mai multe procese senzor către Gateway.
- `Cerinta_3_Gateway_Backend_SQLite.pdf` – retransmiterea și stocarea datelor.
- `Cerinta_4_Detectie_Anomalii_Edge_CO2.pdf` – detectarea valorilor CO₂ anormale.
- `Raport_Edge_Cloud_Spikes_Date_Lipsa_Drift.pdf` – detectarea datelor lipsă, spike-urilor și drift-ului.
- `Raport_Full_Chain_Senzor_Frontend_Grafice.pdf` – demonstrarea întregului lanț IoT și a graficelor Streamlit.

### 13.7. Concluzie

Implementarea practică demonstrează funcționarea întregului lanț de procesare IoT, de la generarea măsurătorilor până la stocarea, analiza și vizualizarea lor.

Comparația experimentală completă între arhitecturile Edge, Cloud și Hybrid, inclusiv evaluarea latenței și a performanței unui model AI, rămâne o etapă viitoare a proiectului.
