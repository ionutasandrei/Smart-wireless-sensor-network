
import os
import sqlite3
import numpy as np
from edge_ai import EdgeAI

DB = "/data/sensors.sqlite3"

def main():
    if not os.path.exists(DB):
        print("Baza de date nu exista.")
        return

    with sqlite3.connect(DB) as conn:
        rows = conn.execute("""
            SELECT co2, temp, light
            FROM measurements
            WHERE injected = 0
            ORDER BY seq
        """).fetchall()

    if len(rows) < 50:
        print("Sunt necesare minimum 50 de masuratori normale.")
        return

    X = np.array(rows, dtype=float)

    model = EdgeAI()
    model.train(X)

    print("Model Edge AI antrenat cu", len(X), "masuratori.")

    for co2, temp, light in [
        (550, 25.5, 155),
        (2500, 25.5, 155)
    ]:
        result = model.detect(co2, temp, light)
        print(
            f"CO2={co2}, Temp={temp}, Lumina={light}"
            f" -> {'ANOMALIE' if result else 'NORMAL'}"
        )

if __name__ == "__main__":
    main()
