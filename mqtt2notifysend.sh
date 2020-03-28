#!/bin/bash

# USAGE: mqtt2notify.send.sh [mosquitto_sub args]
# Expected to receive a message with the following JSON:
# {"title": "Notification title", "text": "Notification body", "level": "Notification urgency"}
#   - text: only required key
#   - title: if not set, using DEFAULT_TITLE
#   - level: notify-send urgency, one of: low, normal, critical

if [[ $1 == "--help" ]]
then
    mosquitto_sub --help
    exit 0
fi

RECONNECTION_DELAY=${RECONNECTION_DELAY:=5}
DEFAULT_TITLE=${DEFAULT_TITLE:="MQTT2NotifySend"}
DEFAULT_LEVEL=${DEFAULT_LEVEL:="normal"}
LOG_ENABLE={$LOG_ENABLE:="true"}

log_counter=0

function log() {
    if [[ "${LOG_ENABLE}" == "true" || "${LOG_ENABLE}" == "1" ]]
    then
        echo "[#$log_counter] $1"
    fi
}

while true
do
    # TODO Identify when mosquitto_sub fails due to connection error or user input (args) error
    mosquitto_sub $@ | while read -r payload
    do
        log_counter=$(( $log_counter + 1))

        log "Received message with payload=\"${payload}\""
        title=$(echo "${payload}" | jq -r ".title")
        text=$(echo "${payload}" | jq -r ".text")
        level=$(echo "${payload}" | jq -r ".level")

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

        log "Sending notification with title=\"${title}\" - text=\"${text}\""
        set -x
        notify-send --urgency=${level} "${title}" "${text}"
        set +x
    done

    sleep $RECONNECTION_DELAY
done
