from enum import Enum


class AdminAnnouncementOEnum(str, Enum):
    ACTIVE_FROM = "active_from"
    ACTIVE_TO = "active_to"
    CREATED = "created"
    NAME = "name"
    TYPE = "type"
    VALUE_0 = "-active_from"
    VALUE_1 = "-active_to"
    VALUE_2 = "-created"
    VALUE_3 = "-name"
    VALUE_4 = "-type"

    def __str__(self) -> str:
        return str(self.value)
