#!/usr/bin/python3

import os
import subprocess
import paho.mqtt.client as mqtt

BROKER = "192.168.0.90"
TOPIC_SUB = "dev/pc/toast"
TOPIC_STAT = "dev/pc/stat"
PORT = 1883
KEEPALIVE = 60
PAYLOAD_ON = "Client Online"
PAYLOAD_OFF = "Client Offline"
DELIMITER = ";;;"
DEFAULT_TITLE = "MQTT"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
ICON = os.path.join(CURRENT_DIR, "icon.png")


def on_connect(client: mqtt.Client, userdata, flags, rc):
    client.subscribe(TOPIC_SUB)
    client.publish(TOPIC_STAT, PAYLOAD_ON, retain=True)


def on_message(client: mqtt.Client, userdata, msg: mqtt.MQTTMessage):
    payload = msg.payload.decode()
    if DELIMITER in payload:
        title, text = payload.split(DELIMITER)
    else:
        title = DEFAULT_TITLE
        text = payload
    subprocess.call((
        "notify-send",
        "-i",
        ICON,
        title,
        text
    ), shell=False)


mqttClient = mqtt.Client()
mqttClient.on_connect = on_connect
mqttClient.on_message = on_message
mqttClient.will_set(TOPIC_STAT, PAYLOAD_OFF, retain=True)
mqttClient.connect(BROKER, PORT, KEEPALIVE)

if __name__ == "__main__":
    try:
        mqttClient.loop_forever()
    except KeyboardInterrupt:
        mqttClient.loop_stop()
