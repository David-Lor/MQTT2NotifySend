"""SERVICES - MESSAGE HANDLER
Handle incoming message payloads from MQTT, calling the Notification service if the message is valid
"""

# # Native # #
import json
from typing import Tuple, Optional

# # Project # #
from ..settings import *

# # Package # #
from .notify_send_client import *

__all__ = ("handle_payload",)


def parse_payload(payload: str) -> Tuple[Optional[str], Optional[str]]:
    """Parse the payload to extract title and text, based on settings and payload received.
    The order of the parsers are: JSON, Delimited, Raw.
    If one parser fails, the next one is used, if active on settings.
    :returns: title, text
    """
    if settings.json_payload:
        try:
            json_payload = json.loads(payload)
            title = json_payload.get(settings.json_title_key)
            text = json_payload[settings.json_text_key]
            return title, text
        except json.JSONDecodeError:
            pass

    if settings.delimited_payload:
        split = payload.split(settings.delimiter)
        if len(split) == 2:
            return split[0], split[1]

    if settings.raw_payload:
        return None, payload

    return None, None


def handle_payload(payload: str):
    """Handle the MQTT payload and send the notification.
    """
    title, text = parse_payload(payload)
    if text:
        if title is None:
            title = settings.default_title
        send_notification(title=title, text=text)
