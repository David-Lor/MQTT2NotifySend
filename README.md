# MQTT2NotifySend

🌉Bridge between MQTT and 🖥️Freedesktop.org Notify-Send desktop notifications (Ubuntu &amp; other distros)🐧, to send notifications to your desktop over MQTT.

## Getting started

```bash
# Dependencies are: libnotify-bin, mosquitto-clients, jq, coreutils
sudo apt install libnotify-bin mosquitto-clients jq coreutils

# Download the script & set as executable (optional)
curl -O https://raw.githubusercontent.com/David-Lor/MQTT2NotifySend/master/mqtt2notifysend.sh
chmod u+x mqtt2notifysend.sh

# Run!
./mqtt2notifysend.sh -h localhost -t notifications

# Send a message to the broker from other terminal window
mosquitto_pub -h localhost -t notifications -m "{\"title\": \"Custom notification\", \"text\": \"Hello world\"}"
```

- Script arguments for MQTT connection are the same used with the `mosquitto_sub` command (run `./mqt2notifysend.sh --help` to know more).
- The script expects a JSON string as payload, with the following tags:
    - `title`: notification title (optional)
    - `text`: notification body (required)
    - `level`: notification urgency level (optional; one of: `low`, `normal`, `critical`; default: `normal`)
    - `iconB64`: notification icon image, encoded as Base64 string (optional)

### Environment variables

Certain settings can be tweaked using the following environment variables:

- `RECONNECTION_DELAY`: time to wait between connection attempts, in seconds (default: `5`)
- `DEFAULT_TITLE`: default title for notifications sent without title (default: `MQTT2NotifySend`)
- `DEFAULT_LEVEL`: default notify-send level for notifications sent without level (default: `normal`)
- `LOG_ENABLE`: if `true` or `1`, enable script logs (default: `false`)
- `ICON_BASE_PATH`: where the notification icon file is downloaded, for each notification. This is an absolute/relative path of the file, used as prefix (default: `/tmp/mqtt2notifysend-icon`)
- `ICON_DELETE_DELAY`: seconds to wait between the icon is decoded and deleted. Cannot be zero, as notifysend command may delay a bit and the icon may be removed when the notification pops up, not showing the icon (default: `5`)

Usage:

```bash
LOG_ENABLE=true RECONNECTION_DELAY=1 DEFAULT_TITLE="Very important notification" DEFAULT_LEVEL=critical \
    bash mqtt2notifysend.sh -h localhost -t notifications
```

## Changelog

- 0.3.0 - Support sending icon for notifications, as base64-encoded string
- 0.2.1 - Allow to disable logs; logs disabled by default; amends on script syntax; describe environment variables on README
- 0.2.0 - Initial new Bash version from scratch
- _v0.1.0 - (Deprecated) Initial new version from scratch (branch [python/develop](https://github.com/David-Lor/MQTT2NotifySend/tree/python/develop))_
- _v0.1 - (Deprecated) Initial version (branch [python/master](https://github.com/David-Lor/MQTT2NotifySend/tree/python/master))_

## TODO

- Support non-JSON payloads (only text and title-text split by delimiter)
- Identify when mosquitto_sub fails due to connection error or user input (args) error
- Validate dependencies installed before connecting
- Support icons sent by URL
