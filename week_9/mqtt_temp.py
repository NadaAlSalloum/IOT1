# mqtt_temp.py
# Simulates temperature readings and turns on a green LED if temp > 25
# Sends temp over MQTT

import time
import random
from gpiozero import LED
import paho.mqtt.client as mqtt

# === Setup green LED ===
green = LED(17)  # Connect long leg to GPIO17 (through resistor), short leg to GND

# === Unique MQTT client ID ===
id = 'nada_IOT_2003'  # Replace with your own unique ID
client_name = id + 'temperature_client'
telemetry_topic = id + '/telemetry'

# === MQTT setup ===
mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()
print("MQTT connected!")

# === Main loop ===
try:
    while True:
        # Simulate random temperature between 23 and 26
        temperature = random.randrange(23, 27)
        print('Light level:', temperature)

        # Send the temperature to the MQTT broker
        mqtt_client.publish(telemetry_topic, str(temperature))

        # LED logic: ON if temperature > 25
        if temperature > 25:
            green.on()
        else:
            green.off()

        time.sleep(3)

except KeyboardInterrupt:
    print("\nProgram stopped by user.")

finally:
    green.off()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("Clean exit.")
