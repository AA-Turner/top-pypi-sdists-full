from abc import ABC, abstractclassmethod
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from wbcore.contrib.notifications.models import Notification


class AbstractNotificationBackend(ABC):
    @abstractclassmethod
    def send_web_notification(cls, notification: "Notification"): ...

    @abstractclassmethod
    def send_mobile_notification(cls, notification: "Notification"): ...

    @abstractclassmethod
    def get_configuration(cls) -> dict: ...
