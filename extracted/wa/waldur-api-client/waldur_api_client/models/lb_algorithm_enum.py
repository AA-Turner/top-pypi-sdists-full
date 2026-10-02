from enum import Enum


class LbAlgorithmEnum(str, Enum):
    LEAST_CONNECTIONS = "LEAST_CONNECTIONS"
    ROUND_ROBIN = "ROUND_ROBIN"
    SOURCE_IP = "SOURCE_IP"
    SOURCE_IP_PORT = "SOURCE_IP_PORT"

    def __str__(self) -> str:
        return str(self.value)
