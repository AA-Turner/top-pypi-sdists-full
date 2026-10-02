from enum import Enum


class BookingResourceOEnum(str, Enum):
    CREATED = "created"
    NAME = "name"
    SCHEDULES = "schedules"
    TYPE = "type"
    VALUE_0 = "-created"
    VALUE_1 = "-name"
    VALUE_2 = "-schedules"
    VALUE_3 = "-type"

    def __str__(self) -> str:
        return str(self.value)
