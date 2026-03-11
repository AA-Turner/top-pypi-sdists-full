import sys
import threading
from contextlib import suppress

from ...models import Notification
from ..abstract_backend import AbstractNotificationBackend


class NotificationBackend(AbstractNotificationBackend):
    @classmethod
    def send_web_notification(cls, notification):
        """Write the notification to the stream in a thread-safe way."""

        _lock = threading.RLock()
        stream = sys.stdout
        with _lock:
            with suppress(Exception):
                stream.write("%s\n" % notification.title)
                stream.write("%s\n" % notification.body or "")
                stream.write("-" * 79)
                stream.write("\n")
                stream.flush()  # flush after each message

    @classmethod
    def send_mobile_notification(cls, notification: Notification):
        cls.send_web_notification(notification)

    @classmethod
    def get_configuration(cls) -> dict:
        return {}
