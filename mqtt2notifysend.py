#!/usr/bin/python3

import os
import subprocess
import paho.mqtt.client as mqtt

# The CLIENT_NAME must be unique on the broker.
# USERNAME, PASSWORD and 8883 port are for secure connection with the Broker.
# If you do not use SSL/TLS connection, change the port to 1883.

BROKER = "192.168.X.XXX"
CLIENT_NAME = "your_computer_name"
USERNAME = "your_username"
PASSWORD = "ypur_password"
CLEAN_SESSION = True
USER_DATA = None
PROTOCOL = mqtt.MQTTv311
TOPIC_SUB = "dev/"+CLIENT_NAME+"/toast"
TOPIC_STAT = "dev/"+CLIENT_NAME+"/stat"
PORT = 8883
KEEPALIVE = 60
PAYLOAD_ON = "Online"
PAYLOAD_OFF = "Offline"
DELIMITER = ";;;"
DEFAULT_TITLE = "MQTT"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(CURRENT_DIR, "icon.png")


def on_connect(mqtt_client: mqtt.Client, userdata, flags, rc):
    mqtt_client.subscribe(TOPIC_SUB)
    mqtt_client.publish(TOPIC_STAT, PAYLOAD_ON, retain=True)
    mqttClient.will_set(TOPIC_STAT, PAYLOAD_OFF, retain=True)
    # Comment the following line if you do not use SSL/TLS connection with the Broker
    mqttClient.username_pw_set(USERNAME, PASSWORD)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
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

mqttClient.loop_forever()
