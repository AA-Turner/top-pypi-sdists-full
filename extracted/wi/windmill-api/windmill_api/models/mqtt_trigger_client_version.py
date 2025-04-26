from enum import Enum


class MqttTriggerClientVersion(str, Enum):
    V3 = "v3"
    V5 = "v5"

    def __str__(self) -> str:
        return str(self.value)
