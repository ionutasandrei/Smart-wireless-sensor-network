# Plan de implementare și evaluare

## Sprint 0 – Propunere
Repository public, README, RQ1, dataset și arhitectură.

## Sprint 1 – Flux demonstrativ
Validare Docker, descărcare dataset, replay MQTT, consumator și dashboard. Verificare integritate și reconectare.

## Sprint 2 – Edge / Cloud / Hibrid
Implementarea celor trei moduri, folosind aceeași regulă sau același model, astfel încât comparația să fie echitabilă. Logarea timestampurilor în fiecare etapă.

## Sprint 3 – Evaluare
Scenarii: normal, anomalie injectată, rețea degradată. Metrici: latență P50/P95, octeți transmiși, CPU/RAM, precision, recall, F1, alarme false. Minimum trei rulări cu seed-uri diferite.

## Sprint 4 – Extensii
Model ML pentru clasificarea ocupării, explicații ale alertelor, teste automate, capturi de ecran și prezentare.

## Limitări
Pragul din prototip este orientativ; unele măsurători reale pot depăși pragul fără injectare, astfel evaluarea F1 necesită o strategie de etichetare distinctă și un set de test bine definit. Nu declara rezultate fără măsurători.
