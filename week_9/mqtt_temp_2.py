# mqtt_temp_2.py
# Sends temperature as JSON to MQTT broker

import time
import random
import json
from gpiozero import LED
import paho.mqtt.client as mqtt

# === Setup green LED ===
green = LED(17)

# === Unique ID + MQTT setup ===
id = 'nada_IOT_2003'  # Replace with your unique ID
client_name = id + '_temperature_client'
telemetry_topic = id + '/telemetry'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")

try:
    while True:
        # Simulated temperature
        temperature = random.randint(23, 27)

        # Build JSON payload
        payload = {
            'device_id': id,
            'temperature': temperature,
            'unit': 'C',
            'status': 'HIGH' if temperature > 25 else 'NORMAL'
        }

        # Convert to JSON string
        json_data = json.dumps(payload)

        # Send it to broker
        mqtt_client.publish(telemetry_topic, json_data)
        print("Sent:", json_data)

        # LED logic
        if temperature > 25:
            green.on()
        else:
            green.off()

        time.sleep(3)

except KeyboardInterrupt:
    print("\n Program stopped by user.")

finally:
    green.off()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print(" MQTT disconnected. Clean exit.")
