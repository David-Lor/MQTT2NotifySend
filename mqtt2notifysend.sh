#!/bin/bash

# USAGE: mqtt2notify.send.sh [mosquitto_sub args]
# Expected to receive a message with the following JSON:
# {"title": "Notification title", "text": "Notification body", "level": "Notification urgency"}
#   - text: only required key
#   - title: if not set, using DEFAULT_TITLE
#   - level: notify-send urgency, one of: low, normal, critical; if not set, using DEFAULT_LEVEL
#   - iconB64: notify-send icon (image file encoded as base64 string)

if [[ $1 == "--help" ]]
then
    mosquitto_sub --help
    exit 0
fi

RECONNECTION_DELAY=${RECONNECTION_DELAY:=5}
DEFAULT_TITLE=${DEFAULT_TITLE:="MQTT2NotifySend"}
DEFAULT_LEVEL=${DEFAULT_LEVEL:="normal"}
LOG_ENABLE=${LOG_ENABLE:="false"}
ICON_BASE_PATH=${ICON_BASE_PATH:="/tmp/mqtt2notifysend-icon"}
ICON_DELETE_DELAY=${ICON_DELETE_DELAY:=5}


function log() {
    if [[ "${LOG_ENABLE}" == "true" || "${LOG_ENABLE}" == "1" ]]
    then
        echo "[#$loop_counter] $1"
    fi
}

function getRandomID() {
    echo $(head /dev/urandom | tr -dc A-Za-z0-9 | head -c10)
}

function loadIconFromB64() {
    log "Decoding base64 icon..."
    b64data="$1"
    icon_path="$ICON_BASE_PATH-$session_id-$(getRandomID)"
    echo "$b64data" | base64 --decode - > "$icon_path"
    (sleep $ICON_DELETE_DELAY && rm "$icon_path") &
}

function mqtt2notifysendMain() {
    session_id=$(getRandomID)
    loop_counter=0

    while true
    do
        # TODO Identify when mosquitto_sub fails due to connection error or user input (args) error
        mosquitto_sub "$@" | while read -r payload
        do
            loop_counter=$(( loop_counter + 1))

            log "Received message with payload=\"${payload}\""
            title=$(echo "${payload}" | jq -r ".title")
            text=$(echo "${payload}" | jq -r ".text")
            level=$(echo "${payload}" | jq -r ".level")
            icon_b64=$(echo "${payload}" | jq -r ".iconB64")

            if [[ "${text}" == "null" || -z "${text}" ]]
            then
                log "The payload was empty - notification will not be send"
                continue
            fi

            if [[ "${title}" == "null" || -z "${title}" ]]
            then
                log "Title not set - using default"
                title="${DEFAULT_TITLE}"
            fi

            if [[ "${level}" == "null" || -z "${level}" ]]
            then
                log "Level (urgency) not set - using default"
                level="${DEFAULT_LEVEL}"
            fi

            icon_path=""
            if [[ "${icon_b64}" != "null" && ! -z "${icon_b64}" ]]
            then
                loadIconFromB64 "${icon_b64}"
            fi

            log "Sending notification with title=\"${title}\" - text=\"${text}\""
            set -x
            notify-send --urgency=${level} --icon="${icon_path}" "${title}" "${text}"
            set +x
        done

        sleep $RECONNECTION_DELAY
    done
}

mqtt2notifysendMain "$@"
