import json, os, sqlite3, time
import paho.mqtt.client as mqtt
DB = '/data/sensors.sqlite3'

def init():
    with sqlite3.connect(DB) as db:
        db.execute('CREATE TABLE IF NOT EXISTS measurements (seq INTEGER PRIMARY KEY, ts TEXT, co2 REAL, temp REAL, light REAL, occupancy INTEGER, injected INTEGER, alert INTEGER, payload TEXT)')

def on_message(client, userdata, msg):
    try:
        event = json.loads(msg.payload)
        s = event['sensors']
        co2 = float(s['S5_CO2'])
        alert = int(co2 > 1800)  # prag demonstrativ, nu limită de siguranță
        with sqlite3.connect(DB, timeout=15) as db:
            db.execute('INSERT OR REPLACE INTO measurements VALUES (?,?,?,?,?,?,?,?,?)', (
                event['seq'], event['replay_ts'], co2, float(s['S1_Temp']),
                float(s['S1_Light']), int(s['Room_Occupancy_Count']),
                int(event['injected_anomaly']), alert, json.dumps(event)))
    except (KeyError, ValueError, TypeError, sqlite3.Error) as exc:
        print('Mesaj invalid:', exc, flush=True)

def main():
    init()
    c = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    c.on_message = on_message
    while True:
        try:
            c.connect(os.getenv('MQTT_HOST','localhost'), 1883, 60)
            break
        except OSError:
            time.sleep(2)
    c.subscribe('wsn/measurements', qos=1)
    c.loop_forever()

if __name__ == '__main__':
    main()
