from enum import Enum


class NotifySystemEnum(str, Enum):
    ADMINANNOUNCEMENT = "AdminAnnouncement"
    BROADCASTMESSAGE = "BroadcastMessage"

    def __str__(self) -> str:
        return str(self.value)
