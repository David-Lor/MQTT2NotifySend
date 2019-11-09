"""SERVICES - MQTT CLIENT
MQTT client to subscribe to notifications topic
"""

# # Native # #
from threading import Event

# # Installed # #
from paho.mqtt.client import Client, MQTTMessage

# # Project # #
from ..settings import *

# # Package # #
from .message_handler import *

__all__ = ("MQTTClient", "MQTTMessage")


class MQTTClient(Client):
    connected_event: Event

    def __init__(self, **kwargs):
        super().__init__(client_id=settings.client_id, **kwargs)
        self.connected_event = Event()

    def on_connect(self, *args):
        if settings.topic_stat:
            self.publish(settings.topic_stat, settings.payload_online, retain=settings.stat_retain)
            if settings.set_lwt:
                self.will_set(topic=settings.topic_stat, payload=settings.payload_offline, retain=settings.stat_retain)
        self.subscribe(settings.topic, qos=settings.qos_sub)
        self.connected_event.set()

    def on_message(self, *args):
        message = next(a for a in args if isinstance(a, MQTTMessage))
        payload = message.payload.decode()
        handle_payload(payload)

    def on_disconnect(self):
        self.connected_event.clear()

    def connect(self, *args, **kwargs):
        super().connect(host=settings.broker, port=settings.port, keepalive=settings.keepalive, *args, **kwargs)

    def run(self):
        self.connect()
        self.loop_forever(retry_first_connection=True)

    def stop(self, force=False):
        self.disconnect()
        self.loop_stop(force)
