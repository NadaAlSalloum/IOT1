import json
import time
import paho.mqtt.client as mqtt

id = 'nada_IOT_2003'
client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'  

client_name = id + 'temperature_server'
mqtt_client = mqtt.Client(client_id=client_name)
mqtt_client.connect('test.mosquitto.org')
mqtt_client.loop_start()

def handle_telemetry(client, userdata, message):
    print("Raw MQTT message received:", message.payload.decode())
    try:
        payload = json.loads(message.payload.decode())
        print("Parsed payload:", payload)

        command = {'led_on': payload['temperature'] < 25}
        print("Sending command:", command)
        mqtt_client.publish(server_command_topic, json.dumps(command))

    except Exception as e:
        print("Error decoding or processing message:", e)

mqtt_client.subscribe(client_telemetry_topic)
print(f" Subscribed to: {client_telemetry_topic}")
mqtt_client.on_message = handle_telemetry

try:
    while True:
        time.sleep(2)

except KeyboardInterrupt:
    print("\n Server stopped.")

finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
    print("Server disconnected cleanly.")
