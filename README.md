# MQTT2NotifySend

🌉Bridge between MQTT and 🖥️Freedesktop.org Notify-Send desktop notifications (Ubuntu &amp; other distros)🐧, to send notifications to your desktop over MQTT.

## Objective

This Python script will subscribe to a MQTT topic and show any incoming message as a popup message on most common Linux desktops, compatible with the NotifySend framework from Freedesktop.org (using the `notify-send` command).

It also sends retained messages to another topic when the script starts and stops, so the computer ON/OFF status is sent over MQTT.

## Requirements

- A Linux distro with a desktop compatible with Freedesktop's NotifySend framework (run `notify-send` on your terminal to check it)
- Python 3.x (tested on 3.7, should work with any modern Python 3)
- A working MQTT broker
- [paho-mqtt](https://pypi.org/project/paho-mqtt/)

## TODO

- Options to set notification priority/level
- More options to customize notification icon
- Possibility to send JSON strings over MQTT

## How to start?

1. Make sure to have the MQTT broker working properly
2. Change the required settings on the script (at least the BROKER HOST if it is not running on your computer)
3. Send a MQTT message to `dev/pc/toast` (or your own TOPIC_SUB if you changed it) - it should be published on your computer!

## Available options

All options are available as variables on the Python script:

- **BROKER**: the MQTT broker host
- **PORT**: the MQTT broker port (1883 by default on vanilla brokers, 8883 by default on SSL/TLS enabled brokers)
- **CLIENT_NAME**: the Client name on the broker (must be unique on the broker)
- **TOPIC_SUB**: MQTT topic to listen for messages that will be published 
- **TOPIC_STAT**: MQTT topic to send computer ON/OFF status. If empty or set to None, no STAT messages will be published. The placeholder `{client_name}` can be used to replace with the CLIENT_NAME
- **PAYLOAD_ON**: payload sent over TOPIC_STAT when the script stats
- **PAYLOAD_OFF**: payload sent over TOPIC_STAT when the script ends
- **DELIMITER**: delimiter on the payload (MQTT message) to split the notification title and message
- **DEFAULT_TITLE**: notification title when no title is provided
- **USERNAME**: username for broker authentication (if empty or set to None, no authentication will be used)
- **PASSWORD**: password for broker authentication
- **CLEAN_SESION**: If True, the broker will remove all information about this client when it disconnects. If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.
- **USER_DATA**: user defined data of any type that is passed as the userdata parameter to callbacks. It may be updated at a later point with the user_data_set() function.
- **PROTOCOL**: the version of the MQTT protocol to use for this client. Can be either mqtt.MQTTv31 or mqtt.MQTTv311
- **KEEPALIVE**: the MQTT Keepalive time


## Customizing the notifications

You can send the payloads (messages) over MQTT with just text, or a title and the text of the notification.

- For text only: send the message text as the payload. The notification will use the DEFAULT_TITLE as title
- For title and text: send the title and the message with the DELIMITER in between. In example, if the delimiter is `;;;`, send:
`My Notification Title;;;The door was opened!`
Important: dollar symbols `$` and maybe other special characters might not be available to send over MQTT. The proposed example works fine.

The notifications can show an icon. The script will always look for a image called `icon.png` at the same level (location) as the Python script. If this file does not exist, no icon will be shown.

## Auto-start

Depending on your distro and desktop, they can be different ways to add this script at startup. Remember that it does not require special permissions, just the required Python version and library installed.

For example, using Ubuntu, you can add the script graphically to startup on user login, using the native Startup Applications tool. You need to:
1. Change the script header (`#!/usr/bin/python3`) to the location of your Python version (when using the Python on the system, you probably don't need to change this; but when using a virtualenv, you must put the absolute path to the Python bin of that virtualenv).
2. Give the .py script execution permissions (`chmod +x mqtt2notifysend.py` or do it graphically).
3. Add the absolute route to the script when creating a new entry on the Startup Applications tool.
