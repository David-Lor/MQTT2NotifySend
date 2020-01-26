# MQTT2NotifySend

🌉Bridge between MQTT and 🖥️Freedesktop.org Notify-Send desktop notifications (Ubuntu &amp; other distros)🐧, to send notifications to your desktop over MQTT.

## Getting started

```bash
# Dependencies are: mosquitto-clients, jq
sudo apt install mosquitto-clients jq

# Download the script & set as executable (optional)
curl -O https://raw.githubusercontent.com/David-Lor/MQTT2NotifySend/master/mqtt2notifysend.sh
chmod u+x mqtt2notifysend.sh

# Run!
./mqtt2notifysend.sh -h localhost -t notifications -m "{\"title\": \"Custom notification\", \"text\": \"Hello world!\"}"
```

- Script arguments for MQTT connection are the same used with the `mosquitto_sub` command (run `./mqt2notifysend.sh --help` to know more).
- The script expects a JSON string as payload, with the following tags:
    - `title`: notification title (optional)
    - `text`: notification body (required)
    - `level`: notification urgency level (one of: `low`, `normal`, `critical`)

## Changelog

- 0.2.0 - Initial new Bash version from scratch
- _0.1.0 - (Deprecated) Initial new version from scratch (branch [python/develop](https://github.com/David-Lor/MQTT2NotifySend/tree/python/develop))_
- _0.1 - (Deprecated) Initial version (branch [python/master](https://github.com/David-Lor/MQTT2NotifySend/tree/python/master))_

## TODO

- Support icons
- Support non-JSON payloads (only text and title-text split by delimiter)
- Allow to disable internal echo log
- Describe environment variable arguments on README
