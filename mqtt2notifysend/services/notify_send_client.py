"""SERVICES - NOTIFY SEND CLIENT
Notification sender service for most of Linux distributions, using notify-send
"""

# # Native # #
import subprocess

__all__ = ("send_notification",)


def send_notification(title: str, text: str):
    # TODO Add icon option ("-i", "icon.png")
    subprocess.call(("notify-send", title, text))
