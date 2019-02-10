# MQTT2NotifySend

🌉Bridge between MQTT and 🖥️Freedesktop.org Notify-Send desktop notifications (Ubuntu &amp; other distros)🐧

## Objective

This Python script will subscribe to a MQTT topic and show any incoming message as a popup message on certain Linux desktops, compatible with the NotifySend framework from Freedesktop.org (using the `notify-send` command).

It also sends retained messages to another topic when the script starts and stops, so the computer ON/OFF status is sent over MQTT.

## Requirements

- A Linux distro with a desktop compatible with Freedesktop's NotifySend framework (run `notify-send` on your terminal to check it)
- Python 3.x (tested on 3.7, should work with any modern Python 3)
- A working MQTT broker
- [paho-mqtt](https://pypi.org/project/paho-mqtt/)

## TODO

- Update this README.md with the new options included
- Options to set notification priority/level
- More options to customize notification icon

## How to start?

- Make sure to have the MQTT broker working properly
- Change the required settings on the script (at least the BROKER HOST)
- Send a MQTT message to `dev/pc/toast` - it should be published on your computer!

## Available options

All options are available as variables on the Python script:

- BROKER: the MQTT broker host
- CLIENT NAME: the Client name on the broker (must be unique)
- USERNAME: username for broker authentication
- PASSWORD: password for broker authentication
- CLEAN_SESION: If True, the broker will remove all information about this client when it disconnects. If False, the client is a durable client and subscription information and queued messages will be retained when the client disconnects.
- USER_DATA: user defined data of any type that is passed as the userdata parameter to callbacks. It may be updated at a later point with the user_data_set() function.
- PROTOCOL: the version of the MQTT protocol to use for this client. Can be either MQTTv31 or MQTTv311
- PORT: the MQTT broker port
- KEEPALIVE: the MQTT Keepalive time
- TOPIC_SUB: MQTT topic to listen for messages that will be published 
- TOPIC_STAT: MQTT topic to send computer ON/OFF status
- PAYLOAD_ON: payload sent over TOPIC_STAT when the script stats
- PAYLOAD_OFF: payload sent over TOPIC_STAT when the script ends
- DELIMITER: delimiter on the payload (MQTT message) to split the notification title and message
- DEFAULT_TITLE: notification title when no title is provided

## Customizing the notifications

You can send the payloads (messages) over MQTT with just text, or a title and the text of the notification.

- For text only: send the message text as the payload. The notification will use the DEFAULT_TITLE as title
- For title and text: send the title and the message with the DELIMITER in between. In example, if the delimiter is `;;;`, send:
`My Notification Title;;;The door was opened!`
Important: dollar symbols `$` and maybe other special characters might not be available to send over MQTT. The proposed example works fine.

The notifications always show an icon. The script will always look for a image called `icon.png` at the same level (location) as the Python script. If this file does not exist, no icon will be shown.

## Auto-start

Depending on your distro and desktop, they can be different ways to add this script at startup. Remember that it does not require special permissions, just the required Python version and library installed.
