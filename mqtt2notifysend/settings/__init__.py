"""SETTINGS
Settings manager for MQTT connection and the MQTT2NotifySend app
"""

# # Native # #
from uuid import uuid1
from typing import Optional

# # Installed # #
from dotenv import load_dotenv
from dotenv_settings_handler import BaseSettingsHandler

__all__ = ("settings",)


class Settings(BaseSettingsHandler):
    broker: str = "127.0.0.1"
    port: int = 1883
    keepalive: int = 60
    client_id: str = "mqtt2notifysend_{}".format(uuid1())
    topic: str = "mqtt2notifysend/cmd"
    qos_sub: int = 0
    topic_stat: Optional[str]
    set_lwt: bool = False
    stat_retain: bool = True
    payload_online: str = "Online"
    payload_offline: str = "Offline"
    default_title: str = "MQTT2NotifySend"
    json_payload: bool = True
    json_title_key: str = "title"
    json_text_key: str = "text"
    delimited_payload: bool = True
    delimiter: str = ";;;"
    raw_payload: bool = True

    class Config:
        env_prefix = "MQTT2NOTIFY_"
        case_insensitive = True


load_dotenv()
settings = Settings()
