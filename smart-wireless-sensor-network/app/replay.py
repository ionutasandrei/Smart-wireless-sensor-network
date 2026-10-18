import io, json, os, time, random, urllib.request
from datetime import datetime, timezone
import pandas as pd
import paho.mqtt.client as mqtt

URL = "https://archive.ics.uci.edu/static/public/864/room+occupancy+estimation.zip"
HOST = os.getenv("MQTT_HOST", "localhost")

def load():
    import zipfile
    with urllib.request.urlopen(URL, timeout=60) as response:
        raw = response.read()
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        names = [n for n in z.namelist() if n.endswith('Occupancy_Estimation.csv')]
        if not names:
            raise RuntimeError('CSV-ul nu a fost găsit în arhiva UCI')
        return pd.read_csv(z.open(names[0]))

def main():
    df = load()
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    while True:
        try:
            client.connect(HOST, 1883, 60)
            break
        except OSError:
            time.sleep(2)
    client.loop_start()
    rng = random.Random(42)
    for i, (_, row) in enumerate(df.iterrows()):
        data = {k: (v.item() if hasattr(v, 'item') else v) for k, v in row.to_dict().items()}
        injected = i % 50 == 25
        if injected:
            data['S5_CO2'] = 2500
        msg = {'seq': i, 'replay_ts': datetime.now(timezone.utc).isoformat(), 'source': 'UCI-864', 'injected_anomaly': injected, 'sensors': data}
        client.publish('wsn/measurements', json.dumps(msg, default=str), qos=1).wait_for_publish()
        time.sleep(2)
    client.loop_stop()
    client.disconnect()

if __name__ == '__main__':
    main()
