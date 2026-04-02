from enum import Enum


class OpenStackInstanceOEnum(str, Enum):
    START_TIME = "start_time"
    VALUE_1 = "-start_time"

    def __str__(self) -> str:
        return str(self.value)
