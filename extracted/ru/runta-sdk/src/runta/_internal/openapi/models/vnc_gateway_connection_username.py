from enum import Enum


class VncGatewayConnectionUsername(str, Enum):
    RUNTA = "runta"

    def __str__(self) -> str:
        return str(self.value)
