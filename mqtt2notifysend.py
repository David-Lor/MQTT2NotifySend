#!/usr/bin/python3

import os
import subprocess
import paho.mqtt.client as mqtt


# BROKER must be the IP/Host where the MQTT Broker is running
# Default MQTT port is 1883 (8883 for SSL/TLS enabled broker)
BROKER = "127.0.0.1"
PORT = 1883

# The CLIENT_NAME must be unique on the broker.
CLIENT_NAME = "your_computer_name"

# Topics where to listen and publish messages
# TOPIC_SUB is where the script will listen to messages, showing them as notifications on the desktop
# TOPIC_STAT is where the script will publish the computer ON/OFF status
# {client_name} is replaced by the CLIENT_NAME variable
TOPIC_SUB = "dev/{client_name}/toast"
TOPIC_STAT = "dev/{client_name}/stat"

# The delimiter is used on incoming MQTT messages to split the notification title and text.
# If no delimiter is provided, notification will show DEFAULT_TITLE as the title
DELIMITER = ";;;"
DEFAULT_TITLE = "MQTT"

# Payloads are the message text to be sent through the TOPIC_STAT topic
PAYLOAD_ON = "Online"
PAYLOAD_OFF = "Offline"

# If authentication is enabled on the broker, set your username and password
USERNAME = None
PASSWORD = None

# Misc MQTT settings
CLEAN_SESSION = True
USER_DATA = None
PROTOCOL = mqtt.MQTTv311
KEEPALIVE = 60

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(CURRENT_DIR, "icon.png")


def on_connect(mqtt_client: mqtt.Client, userdata, flags, rc):
    mqtt_client.subscribe(TOPIC_SUB.format(client_name=CLIENT_NAME))
    mqtt_client.publish(TOPIC_STAT.format(client_name=CLIENT_NAME), PAYLOAD_ON, retain=True)
    mqttClient.will_set(TOPIC_STAT.format(client_name=CLIENT_NAME), PAYLOAD_OFF, retain=True)
    if USERNAME is not None and PASSWORD is not None:
        mqttClient.username_pw_set(USERNAME, PASSWORD)


def on_message(mqtt_client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    payload = msg.payload.decode()
    if DELIMITER in payload:
        title, text = payload.split(DELIMITER)
    else:
        title = DEFAULT_TITLE
        text = payload
    subprocess.call(("notify-send", "-i", ICON, title, text))


mqttClient = mqtt.Client(CLIENT_NAME, CLEAN_SESSION, USER_DATA, PROTOCOL)
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.connect(BROKER, PORT, KEEPALIVE)

if __name__ == "__main__":
    try:
        mqttClient.loop_forever()
    except KeyboardInterrupt:
        mqttClient.loop_stop()
