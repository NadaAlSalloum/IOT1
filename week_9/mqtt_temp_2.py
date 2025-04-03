import time
import random
import json
from gpiozero import LED
import paho.mqtt.client as mqtt

green = LED(17)
id = 'nada_IOT_2003'
client_name = id + '_temperature_client'

telemetry_topic = id + '/telemetry'
command_topic = id + '/commands'  

mqtt_client = mqtt.Client(client_id=client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

print("MQTT connected and publishing...")

# Handle incoming commands
def handle_command(client, userdata, message):
    try:
        payload = json.loads(message.payload.decode())
        print("Command received:", payload)
        if payload.get('led_on'):
            green.on()
        else:
            green.off()
    except Exception as e:
        print("Error handling command:", e)

mqtt_client.subscribe(command_topic)
mqtt_client.on_message = handle_command

try:
    while True:
        temperature = random.randint(23, 27)

        telemetry = {
            'device_id': id,
            'temperature': temperature,
            'status': 'HIGH' if temperature > 25 else 'NORMAL'
        }

        mqtt_client.publish(telemetry_topic, json.dumps(telemetry))
        print("Sent telemetry:", telemetry)

        time.sleep(3)

except KeyboardInterrupt:
    print("\nDevice stopped.")

finally:
    green.off()
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("Clean shutdown.")
