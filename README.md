# MQTT2NotifySend

🌉Bridge between MQTT and 🖥️Freedesktop.org Notify-Send desktop notifications (Ubuntu & other distros)🐧, to send notifications to your desktop over MQTT.

## Requirements

- A Linux distro with a desktop compatible with Freedesktop's NotifySend framework (run `notify-send` on your terminal to check it)
- Python 3.x (tested on Python 3.7)
- A working MQTT broker
- Requirements listed on [requirements.txt](requirements.txt)

## Getting started

### Installing

For now the app is not provided through pypi, so clone with git or download manually:

```bash
# Ensure you have a recent compatible version of Python installed, or use a virtual env
git clone https://github.com/David-Lor/MQTT2NotifySend.git
pip install -r MQTT2NotifySend/requirements.txt
python MQTT2NotifySend
```

### Sending notifications!

Just publish a MQTT message to the topic `mqtt2notifysend/cmd`. The payload can be one of the following:

- A JSON string like this (title is optional):
  ```json
  {"title": "My first notification", "payload": "Hello world!"}
  ```
- A string delimited with `;;;`:
  ```
  My first notification;;;Hello world!
  ```
- A simple string (title cannot be defined):
  ```
  Hello world!
  ```

## TODO/Roadmap

- Add CLI interface with [Fire](https://github.com/google/python-fire) or [Click](https://github.com/pallets/click)
- Publish to pypi
- Options to set notification priority/level
- Options to set/customize the notification icon
- Options to set username/password for MQTT connection
- Add tests

## Changelog

- 0.1.0 - Initial new version from scratch (functional)
- _0.2 - (Deprecated) improvements (branch [enhancement](https://github.com/David-Lor/MQTT2NotifySend/tree/enhancement))_
- _0.1 - (Deprecated) Initial version (branch [master](https://github.com/David-Lor/MQTT2NotifySend/tree/master))_

## Settings

For now, settings must be provided through environment variables or a .env file on the project root (alongside `__main__.py`)

- **Main settings**:
    - **MQTT2NOTIFY_BROKER**: MQTT broker host (default: `127.0.0.1`)
    - **MQTT2NOTIFY_PORT**: MQTT broker port (default: `1883`)
    - **MQTT2NOTIFY_TOPIC**: MQTT topic where listen for messages that will be converted to desktop notifications (default: `mqtt2notifysend/cmd`)
    - **MQTT2NOTIFY_DEFAULT_TITLE**: default title for notifications when no title provided on the MQTT message (default: `MQTT2NotifySend`)
- **Additional settings**:
    - **MQTT2NOTIFY_KEEPALIVE**: MQTT keepalive time (default: `60`)
    - **MQTT2NOTIFY_CLIENT_ID**: MQTT client id (default: `mqtt2notifysend_{uuid1}`, being `{uuid1}` generated with `uuid.uuid1()`)
    - **MQTT2NOTIFY_QOS_SUB**: MQTT QoS for the `MQTT2NOTIFY_TOPIC` (default: `0`)
    - **MQTT2NOTIFY_TOPIC_STAT**: MQTT topic where the Stat messages (app Online/Offline) are published (optional, if not set, won't publish stat messages)
    - **MQTT2NOTIFY_SET_LWT**: `true`/`false`; if `true`, set Last Will message on Topic stat (default: `false`; ignored if no topic stat set)
    - **MQTT2NOTIFY_STAT_RETAIN**: `true`/`false`; if `true`, publish Stat messages with the Retain flag (default: `true`; ignored if no topic stat set)
    - **MQTT2NOTIFY_PAYLOAD_ONLINE**: payload to publish on stat topic when the app connects to MQTT (default: `Online`; ignored if no topic stat set)
    - **MQTT2NOTIFY_PAYLOAD_ONLINE**: payload to publish on stat topic as the Last Will message (default: `Offline`; ignored if no topic stat set)
- **Payload settings** define how the app will parse the payloads received, having 3 parsers:
    - **JSON parser** (payload is send as a JSON string):
        - **MQTT2NOTIFY_JSON_PAYLOAD**: `true`/`false`; if `true`, expect JSON payloads (default: `true`)
        - **MQTT2NOTIFY_JSON_TITLE_KEY**: key of the title field on the JSON (default: `title`)
        - **MQTT2NOTIFY_JSON_TEXT_KEY**: key of the text field on the JSON (default: `text`)
    - **Delimited parser** (payload is send as a string with the title and payload split by a delimiter):
        - **MQTT2NOTIFY_DELIMITED_PAYLOAD**: `true`/`false`; if `true`, expect delimited payloads (default: `true`)
        - **MQTT2NOTIFY_DELIMITER**: delimiter character/s (default: `;;;`)
    - **Raw payload** (the payload received is printed as the text notification - title cannot be set):
        - **MQTT2NOTIFY_RAW_PAYLOAD**: `true`/`false`; if `true`, expect raw payloads (default: `true`)
    - If more than one parser is enabled, their priority will be: JSON, Delimited, Raw (if one fails, the next is used)
