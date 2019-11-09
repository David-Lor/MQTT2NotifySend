"""ENTRYPOINT
"""

# # Package # #
from .services import *

__all__ = ("run",)


def run():
    client = MQTTClient()

    try:
        client.run()
    except (KeyboardInterrupt, InterruptedError):
        pass

    client.stop()


if __name__ == '__main__':
    run()
